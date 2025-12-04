from django.utils import timezone
from django.db.models import Count, Avg
from django.db.models.functions import TruncWeek, TruncDate
from datetime import datetime, time as time_cls
import os
import csv

from django.conf import settings
from django.http import FileResponse, Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.usuarios.permissions import IsStaffLike
from rest_framework.response import Response

from apps.denuncias.models import Denuncia, Resolucion, Ubicacion
from apps.reportes.models import (
    Reporte,
    Estadistica,
    Indicador,
    Dashboard,
    DashboardIndicador,
    TendenciaGeografica,
    RankingDesempeno,
)
from apps.denuncias.models import Denuncia, Ubicacion
from apps.personal.models import Tramitacion
from apps.denuncias.models import Resolucion


def _get_date_range_from_request(request):
    """Devuelve (start, end) en base al parámetro 'range'.

    Soporta:
    - day, week, month, year (como antes)
    - custom: usa parámetros GET 'from' y 'to' (YYYY-MM-DD)
    """
    r = (request.GET.get('range') or '').lower()
    now = timezone.now()

    if r == 'custom':
        from_str = request.GET.get('from')
        to_str = request.GET.get('to')
        try:
            if from_str and to_str:
                from_date = datetime.strptime(from_str, '%Y-%m-%d').date()
                to_date = datetime.strptime(to_str, '%Y-%m-%d').date()
                start_dt = datetime.combine(from_date, time_cls.min)
                end_dt = datetime.combine(to_date, time_cls.max)
                start = timezone.make_aware(start_dt) if timezone.is_naive(start_dt) else start_dt
                end = timezone.make_aware(end_dt) if timezone.is_naive(end_dt) else end_dt
                return start, end
        except Exception:
            # si hay error en el parseo, caemos al comportamiento por defecto
            pass

    if r == 'day':
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif r == 'week':
        start = now - timezone.timedelta(days=7)
    elif r == 'month':
        start = now - timezone.timedelta(days=30)
    elif r == 'year':
        start = now - timezone.timedelta(days=365)
    else:
        # por defecto últimos 30 días
        start = now - timezone.timedelta(days=30)
    return start, now


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStaffLike])
def dashboard_summary(request):
    """Resumen para el dashboard ejecutivo de admin.

    Devuelve:
    - total_denuncias
    - avg_tiempo_atencion_horas (promedio de tiempo_total_horas en Resolucion)
    - tasa_resolucion (% de denuncias en estado 'Resuelta')
    - avg_satisfaccion (promedio de calificacion_ciudadano)
    - estados (conteo por estado de Denuncia)
    - hoy (denuncias de hoy y pendientes de validación)
    """

    # Rango de fechas para el análisis principal
    start, end = _get_date_range_from_request(request)

    base_qs = Denuncia.objects.filter(fecha_registro__range=(start, end))

    # Totales generales de denuncias en el rango
    total_denuncias = base_qs.count()

    # Denuncias hoy (por fecha_registro, independiente del rango)
    today = timezone.now().date()
    denuncias_hoy = Denuncia.objects.filter(fecha_registro__date=today).count()

    # Pendientes de validación (independiente del rango)
    pendientes_validacion = Denuncia.objects.filter(requiere_validacion=True).count()

    # Distribución por estado
    estados_counts = {}
    try:
        estados_qs = (
            base_qs.values('estado')
            .annotate(count=Count('id_denuncia'))
        )
        estados_counts = {row['estado']: row['count'] for row in estados_qs}
    except Exception as e:
        print(f"Error en estados_qs: {e}")
        estados_counts = {}

    # Métricas de resolución (tabla Resolucion)
    avg_tiempo = Resolucion.objects.aggregate(avg=Avg('tiempo_total_horas'))['avg'] or 0
    avg_satisf = Resolucion.objects.aggregate(avg=Avg('calificacion_ciudadano'))['avg'] or 0

    # Tasa de resolución: denuncias en estado 'Resuelta' sobre total en el rango
    resueltas = base_qs.filter(estado='Resuelta').count()
    tasa_resolucion = 0.0
    if total_denuncias > 0:
        tasa_resolucion = round(resueltas * 100.0 / total_denuncias, 2)

    data = {
        'total_denuncias': total_denuncias,
        'avg_tiempo_atencion_horas': float(avg_tiempo),
        'tasa_resolucion': float(tasa_resolucion),
        'avg_satisfaccion': float(avg_satisf),
        'hoy': {
            'denuncias_hoy': denuncias_hoy,
            'pendientes_validacion': pendientes_validacion,
        },
        'estados': estados_counts,
    }

    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStaffLike])
def dashboard_categorias(request):
    """
    Distribución de denuncias por categoría (top 6)
    """
    start, end = _get_date_range_from_request(request)

    qs = (
        Denuncia.objects.filter(fecha_registro__range=(start, end))
        .values('id_categoria__nombre')
        .annotate(count=Count('id_denuncia'))
        .order_by('-count')[:6]
    )
    total = Denuncia.objects.filter(fecha_registro__range=(start, end)).count() or 1
    items = []
    for row in qs:
        nombre = row['id_categoria__nombre'] or 'Sin categoría'
        count = row['count']
        perc = round(count * 100.0 / total, 2)
        items.append({'nombre': nombre, 'count': count, 'porcentaje': perc})
    return Response({'total': total, 'categorias': items})


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStaffLike])
def dashboard_temporal(request):
    """Serie temporal de denuncias registradas vs resueltas.

    Param:
      - granularity: 'day' | 'week' | 'month' (default 'week')
    """
    now = timezone.now()
    gran = (request.GET.get('granularity') or 'week').lower()

    # rango base: reusamos helper pero aseguramos una ventana mínima razonable
    start, _ = _get_date_range_from_request(request)
    if gran == 'day':
        min_start = now - timezone.timedelta(days=7)
    elif gran == 'month':
        min_start = now - timezone.timedelta(days=365)
    else:  # week
        min_start = now - timezone.timedelta(weeks=4)
    if start > min_start:
        start = min_start

    # Seleccionar función de truncado y construcción de key/label
    def build_qs_denuncia(field_name):
        if gran == 'day':
            return (
                Denuncia.objects.filter(fecha_registro__gte=start)
                .annotate(bucket=TruncDate(field_name))
                .values('bucket')
                .annotate(count=Count('id_denuncia'))
                .order_by('bucket')
            )
        elif gran == 'month':
            return (
                Denuncia.objects.filter(fecha_registro__gte=start)
                .annotate(bucket=TruncDate(field_name))
                .values('bucket__year', 'bucket__month')
                .annotate(count=Count('id_denuncia'))
                .order_by('bucket__year', 'bucket__month')
            )
        else:  # week
            return (
                Denuncia.objects.filter(fecha_registro__gte=start)
                .annotate(bucket=TruncWeek(field_name))
                .values('bucket')
                .annotate(count=Count('id_denuncia'))
                .order_by('bucket')
            )

    def build_qs_resolucion(field_name):
        if gran == 'day':
            return (
                Resolucion.objects.filter(fecha_resolucion__gte=start)
                .annotate(bucket=TruncDate(field_name))
                .values('bucket')
                .annotate(count=Count('id_resolucion'))
                .order_by('bucket')
            )
        elif gran == 'month':
            return (
                Resolucion.objects.filter(fecha_resolucion__gte=start)
                .annotate(bucket=TruncDate(field_name))
                .values('bucket__year', 'bucket__month')
                .annotate(count=Count('id_resolucion'))
                .order_by('bucket__year', 'bucket__month')
            )
        else:
            return (
                Resolucion.objects.filter(fecha_resolucion__gte=start)
                .annotate(bucket=TruncWeek(field_name))
                .values('bucket')
                .annotate(count=Count('id_resolucion'))
                .order_by('bucket')
            )

    reg = build_qs_denuncia('fecha_registro')
    res = build_qs_resolucion('fecha_resolucion')

    def to_key_and_label(row):
        if gran == 'day':
            d = row['bucket']
            if not d:
                return None, None
            label = d.strftime('%d/%m')
            key = d.isoformat()
            return key, label
        elif gran == 'month':
            y = row.get('bucket__year')
            m = row.get('bucket__month')
            if not (y and m):
                return None, None
            key = f"{y}-{m:02d}"
            label = f"{m:02d}/{y}"
            return key, label
        else:  # week
            d = row['bucket']
            if not d:
                return None, None
            y, w, _ = d.date().isocalendar()
            key = f"{y}-W{w}"
            label = f"Sem {w}"
            return key, label

    def to_map(qs):
        m = {}
        labels = {}
        for row in qs:
            key, label = to_key_and_label(row)
            if not key:
                continue
            m[key] = row['count']
            labels[key] = label
        return m, labels

    reg_map, reg_labels = to_map(reg)
    res_map, res_labels = to_map(res)

    # Unificar claves y ordenar por clave alfabética (que coincide con orden temporal en todos los casos)
    all_keys = sorted(set(reg_map.keys()) | set(res_map.keys()))
    series = []
    for key in all_keys:
        label = reg_labels.get(key) or res_labels.get(key) or key
        series.append({
            'label': label,
            'registradas': reg_map.get(key, 0),
            'resueltas': res_map.get(key, 0),
        })

    return Response({'series': series})


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStaffLike])
def dashboard_prioridades(request):
    """
    Conteos por prioridad por semana (últimas 4 semanas) para columnas apiladas
    """
    now = timezone.now()
    start = now - timezone.timedelta(weeks=4)
    qs = (
        Denuncia.objects.filter(fecha_registro__gte=start)
        .annotate(week=TruncWeek('fecha_registro'))
        .values('week', 'prioridad')
        .annotate(count=Count('id_denuncia'))
        .order_by('week')
    )
    # Armar mapa week -> prioridad -> count
    data = {}
    for row in qs:
        wk = row['week'].date().isocalendar()
        key = f"{wk[0]}-W{wk[1]}"
        pr = row['prioridad']
        data.setdefault(key, {}).setdefault(pr, 0)
        data[key][pr] += row['count']
    series = []
    for i in range(4, 0, -1):
        wk_date = (now - timezone.timedelta(weeks=i)).date()
        y, w, _ = wk_date.isocalendar()
        key = f"{y}-W{w}"
        prio = data.get(key, {})
        series.append({
            'label': key,
            'Urgente': prio.get('Urgente', 0),
            'Alta': prio.get('Alta', 0),
            'Media': prio.get('Media', 0),
            'Baja': prio.get('Baja', 0),
        })
    return Response({'series': series})


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStaffLike])
def dashboard_alerts(request):
    """
    Alertas simples para panel derecho.
    """
    try:
        start, end = _get_date_range_from_request(request)

        base_qs = Denuncia.objects.filter(fecha_registro__range=(start, end))

        # Urgentes sin asignar en el rango
        urgentes_sin_asignar = base_qs.filter(
            prioridad='Urgente'
        ).exclude(
            estado__in=['Asignado', 'En proceso', 'Resuelta', 'Cerrada']
        ).count()

        # Próximas a vencer (24h) dentro del rango
        hace_24h = timezone.now() - timezone.timedelta(hours=24)
        proximas_vencer = base_qs.filter(
            estado='En proceso',
            fecha_registro__lte=hace_24h
        ).count()

        return Response({
            'urgentes_sin_asignar': urgentes_sin_asignar,
            'proximas_vencer_24h': proximas_vencer,
        })
    except Exception as e:
        print(f"Error en dashboard_alerts: {e}")
        return Response({
            'urgentes_sin_asignar': 0,
            'proximas_vencer_24h': 0,
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStaffLike])
def geo_points(request):
    qs = Denuncia.objects.select_related('id_ubicacion', 'id_categoria')
    f_from = request.GET.get('from')
    f_to = request.GET.get('to')
    distrito = request.GET.get('district')
    categoria = request.GET.get('categoria')
    estado = request.GET.get('estado')
    prioridad = request.GET.get('prioridad')
    code = request.GET.get('code')

    if f_from:
        qs = qs.filter(fecha_registro__date__gte=f_from)
    if f_to:
        qs = qs.filter(fecha_registro__date__lte=f_to)
    if distrito:
        qs = qs.filter(id_ubicacion__distrito=distrito)
    if categoria:
        qs = qs.filter(id_categoria__nombre=categoria)
    if estado:
        qs = qs.filter(estado=estado)
    if prioridad:
        qs = qs.filter(prioridad=prioridad)
    if code:
        qs = qs.filter(codigo_denuncia__icontains=code)

    data = []
    for d in qs:
        ubi = d.id_ubicacion
        if not ubi:
            continue
        data.append({
            'id': d.id_denuncia,
            'codigo': d.codigo_denuncia,
            'lat': float(ubi.latitud),
            'lng': float(ubi.longitud),
            'titulo': d.titulo,
            'categoria': getattr(d.id_categoria, 'nombre', None),
            'estado': d.estado,
            'prioridad': d.prioridad,
            'fecha': d.fecha_registro.isoformat(),
            'distrito': ubi.distrito,
        })
    return Response({'points': data})


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStaffLike])
def geo_top_zonas(request):
    qs = Denuncia.objects.select_related('id_ubicacion')
    f_from = request.GET.get('from')
    f_to = request.GET.get('to')
    if f_from:
        qs = qs.filter(fecha_registro__date__gte=f_from)
    if f_to:
        qs = qs.filter(fecha_registro__date__lte=f_to)

    agg = (
        qs.values('id_ubicacion__distrito')
        .annotate(count=Count('id_denuncia'))
        .order_by('-count')[:10]
    )
    items = [{'zona': row['id_ubicacion__distrito'] or 'Sin distrito', 'denuncias': row['count']} for row in agg]
    return Response({'top_zonas': items})


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStaffLike])
def geo_evolucion(request):
    now = timezone.now()
    days = int(request.GET.get('days', '7'))
    start = now - timezone.timedelta(days=days)
    qs = (
        Denuncia.objects.filter(fecha_registro__gte=start)
        .select_related('id_ubicacion')
        .annotate(day=TruncDate('fecha_registro'))
        .values('day', 'id_ubicacion__distrito')
        .annotate(count=Count('id_denuncia'))
        .order_by('day')
    )
    series = {}
    labels = []
    for row in qs:
        label = row['day'].isoformat()
        if label not in labels:
            labels.append(label)
        dist = row['id_ubicacion__distrito'] or 'Sin distrito'
        series.setdefault(dist, {})[label] = row['count']
    # Normalize series per label order
    datasets = []
    for dist, m in series.items():
        data = [m.get(lb, 0) for lb in labels]
        datasets.append({'label': dist, 'data': data})
    return Response({'labels': labels, 'datasets': datasets})


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStaffLike])
def indicators_list(request):
    """
    Lista de indicadores con filtros básicos.
    Params opcionales:
      - q: texto a buscar en nombre/descripcion
      - type: tipo de visualización (barchart, gauge, number, piechart, linechart)
      - freq: frecuencia (tiempo_real, diario, semanal, mensual)
    """
    qs = Indicador.objects.all()

    q = request.GET.get('q')
    if q:
        qs = qs.filter(nombre__icontains=q) | qs.filter(descripcion__icontains=q)

    type_map = {
        'barchart': 'BarChart',
        'gauge': 'Gauge',
        'number': 'Number',
        'piechart': 'PieChart',
        'linechart': 'LineChart',
    }
    req_type = request.GET.get('type')
    if req_type and req_type in type_map:
        qs = qs.filter(tipo_visualizacion=type_map[req_type])

    freq_map = {
        'tiempo_real': 'Tiempo real',
        'diaria': 'Diario',
        'semanal': 'Semanal',
        'mensual': 'Mensual',
    }
    req_freq = request.GET.get('freq')
    if req_freq and req_freq in freq_map:
        qs = qs.filter(frecuencia_actualizacion=freq_map[req_freq])

    def to_slug_vis(v):
        return {
            'BarChart': 'barchart',
            'Gauge': 'gauge',
            'Number': 'number',
            'PieChart': 'piechart',
            'LineChart': 'linechart',
        }.get(v, 'number')

    def to_slug_freq(v):
        return {
            'Tiempo real': 'tiempo_real',
            'Diario': 'diaria',
            'Semanal': 'semanal',
            'Mensual': 'mensual',
        }.get(v, 'diaria')

    items = []
    for ind in qs[:60]:
        items.append({
            'codigo': ind.codigo_indicador,
            'nombre': ind.nombre,
            'descripcion': ind.descripcion,
            'tipo': to_slug_vis(ind.tipo_visualizacion),
            'frecuencia': to_slug_freq(ind.frecuencia_actualizacion),
            'valor_min': float(ind.valor_minimo) if ind.valor_minimo is not None else None,
            'valor_max': float(ind.valor_maximo) if ind.valor_maximo is not None else None,
            'valor_actual': float(ind.valor_actual) if ind.valor_actual is not None else None,
            'ultima_actualizacion': None,
        })

    return Response({'results': items})


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStaffLike])
def ranking_desempeno(request):
    """
    Ranking de desempeño por área responsable.
    Params:
      - periodo (opcional): Diario/Semanal/Mensual/Trimestral/Anual
      - limit (opcional): default 50
      - offset (opcional): default 0
    """
    qs = RankingDesempeno.objects.select_related('id_area_responsable')
    periodo = request.GET.get('periodo')
    if periodo:
        qs = qs.filter(periodo_evaluacion=periodo)

    # Ordering by posicion asc (as per model ordering)
    offset = int(request.GET.get('offset', '0'))
    limit = int(request.GET.get('limit', '50'))
    total = qs.count()
    rows = qs[offset:offset+limit]

    results = []
    for r in rows:
        results.append({
            'rank': r.posicion,
            'area': getattr(r.id_area_responsable, 'nombre', 'Área'),
            'puntaje': float(r.puntaje_total),
            'denuncias': r.denuncias_atendidas,
            'tasa': float(r.tasa_resolucion_area),
            'tiempo': float(r.tiempo_promedio_area),
            'calificacion': float(r.calificacion_promedio) if r.calificacion_promedio is not None else None,
        })

    return Response({
        'count': total,
        'offset': offset,
        'limit': limit,
        'results': results,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStaffLike])
def admin_reportes_list(request):
    """Listado de reportes generados por el usuario autenticado.

    Filtros opcionales por tipo_reporte, formato_exportacion, estado_generacion.
    """
    qs = Reporte.objects.filter(id_usuario_generador=request.user)

    tipo = request.GET.get('tipo_reporte')
    if tipo:
        qs = qs.filter(tipo_reporte=tipo)

    formato = request.GET.get('formato')
    if formato:
        qs = qs.filter(formato_exportacion=formato)

    estado = request.GET.get('estado')
    if estado:
        qs = qs.filter(estado_generacion=estado)

    data = []
    for rpt in qs.order_by('-fecha_generacion')[:200]:
        data.append({
            'codigo_reporte': rpt.codigo_reporte,
            'tipo_reporte': rpt.tipo_reporte,
            'nombre': rpt.nombre,
            'descripcion': rpt.descripcion,
            'fecha_generacion': rpt.fecha_generacion.isoformat() if rpt.fecha_generacion else None,
            'fecha_inicio': rpt.fecha_inicio.isoformat() if rpt.fecha_inicio else None,
            'fecha_fin': rpt.fecha_fin.isoformat() if rpt.fecha_fin else None,
            'formato_exportacion': rpt.formato_exportacion,
            'estado_generacion': rpt.estado_generacion,
            'es_publico': rpt.es_publico,
        })

    return Response({'results': data})


def _parse_iso_date(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value).date()
    except Exception:
        return None


def _normalize_tipo_reporte(value):
    if not value:
        return 'Ejecutivo'
    mapping = {
        'ejecutivo': 'Ejecutivo',
        'operativo': 'Operativo',
        'estadistico': 'Estadístico',
        'estadístico': 'Estadístico',
        'auditoria': 'Auditoria',
        'auditoría': 'Auditoria',
    }
    return mapping.get(value.lower(), 'Ejecutivo')


def _normalize_formato_exportacion(value):
    if not value:
        return 'CSV'
    mapping = {
        'csv': 'CSV',
        'excel': 'Excel',
        'pdf': 'PDF',
        'json': 'JSON',
    }
    return mapping.get(value.lower(), 'CSV')


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsStaffLike])
def admin_reportes_generate(request):
    """Crea y genera un reporte sencillo en CSV sobre denuncias.

    Espera en el body:
      - nombre (str)
      - descripcion (str, opcional)
      - tipo_reporte (slug como 'ejecutivo', 'operativo', etc.)
      - fecha_inicio, fecha_fin (YYYY-MM-DD)
      - formato_exportacion (por ahora se soporta CSV, otros se aceptan pero
        se generan igual como CSV de ejemplo)
      - parametros_configuracion (JSON opcional) con claves:
          * filtros: {
              categorias: [nombres],
              estados: [estados],
              prioridades: [prioridades]
            }
    """
    payload = request.data or {}

    nombre = (payload.get('nombre') or '').strip()
    if not nombre:
        return Response({'detail': 'El nombre del reporte es obligatorio.'}, status=400)

    descripcion = (payload.get('descripcion') or '').strip()
    tipo = _normalize_tipo_reporte(payload.get('tipo_reporte') or payload.get('tipo'))
    formato = _normalize_formato_exportacion(payload.get('formato_exportacion') or payload.get('formato'))

    fecha_inicio = _parse_iso_date(payload.get('fecha_inicio'))
    fecha_fin = _parse_iso_date(payload.get('fecha_fin'))
    if not fecha_inicio or not fecha_fin:
        return Response({'detail': 'fecha_inicio y fecha_fin son obligatorias y deben tener formato YYYY-MM-DD.'}, status=400)

    if fecha_fin < fecha_inicio:
        return Response({'detail': 'fecha_fin no puede ser anterior a fecha_inicio.'}, status=400)

    parametros = payload.get('parametros_configuracion') or {}
    filtros = parametros.get('filtros') or {}

    # Crear instancia de reporte en estado En progreso
    rpt = Reporte(
        nombre=nombre,
        descripcion=descripcion,
        tipo_reporte=tipo,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        formato_exportacion=formato,
        id_usuario_generador=request.user,
        estado_generacion='En progreso',
        parametros_configuracion=parametros,
    )
    rpt.save()

    try:
        # Construir queryset base de denuncias
        qs = Denuncia.objects.select_related('id_categoria', 'id_ubicacion').filter(
            fecha_registro__date__range=(fecha_inicio, fecha_fin)
        )

        categorias = filtros.get('categorias') or []
        if categorias:
            qs = qs.filter(id_categoria__nombre__in=categorias)

        estados = filtros.get('estados') or []
        if estados:
            qs = qs.filter(estado__in=estados)

        prioridades = filtros.get('prioridades') or []
        if prioridades:
            qs = qs.filter(prioridad__in=prioridades)

        # Asegurar carpeta de salida
        media_root = getattr(settings, 'MEDIA_ROOT', None) or ''
        out_dir = os.path.join(media_root, 'reportes')
        os.makedirs(out_dir, exist_ok=True)

        filename = f"{rpt.codigo_reporte}.csv"
        abs_path = os.path.join(out_dir, filename)

        # Generar CSV sencillo
        with open(abs_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Código', 'Título', 'Descripción', 'Fecha registro',
                'Estado', 'Prioridad', 'Categoría', 'Distrito', 'Dirección',
            ])
            for d in qs.iterator():
                ubi = getattr(d, 'id_ubicacion', None)
                cat = getattr(d, 'id_categoria', None)
                writer.writerow([
                    d.codigo_denuncia,
                    d.titulo,
                    (d.descripcion or '')[:200],
                    d.fecha_registro.isoformat() if d.fecha_registro else '',
                    d.estado,
                    d.prioridad,
                    getattr(cat, 'nombre', ''),
                    getattr(ubi, 'distrito', ''),
                    getattr(ubi, 'direccion', ''),
                ])

        # Guardar ruta relativa en el modelo y marcar como completado
        rpt.ruta_archivo = os.path.join('reportes', filename)
        rpt.estado_generacion = 'Completado'
        rpt.save(update_fields=['ruta_archivo', 'estado_generacion'])

    except Exception as exc:
        rpt.estado_generacion = 'Fallido'
        rpt.save(update_fields=['estado_generacion'])
        return Response({'detail': f'Error generando el reporte: {exc}'}, status=500)

    data = {
        'codigo_reporte': rpt.codigo_reporte,
        'tipo_reporte': rpt.tipo_reporte,
        'nombre': rpt.nombre,
        'descripcion': rpt.descripcion,
        'fecha_generacion': rpt.fecha_generacion.isoformat() if rpt.fecha_generacion else None,
        'fecha_inicio': rpt.fecha_inicio.isoformat() if rpt.fecha_inicio else None,
        'fecha_fin': rpt.fecha_fin.isoformat() if rpt.fecha_fin else None,
        'formato_exportacion': rpt.formato_exportacion,
        'estado_generacion': rpt.estado_generacion,
        'ruta_archivo': rpt.ruta_archivo,
    }
    return Response(data, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStaffLike])
def admin_reportes_download(request, codigo_reporte):
    """Devuelve el archivo físico de un reporte generado por el usuario."""
    try:
        rpt = Reporte.objects.get(codigo_reporte=codigo_reporte, id_usuario_generador=request.user)
    except Reporte.DoesNotExist:
        raise Http404("Reporte no encontrado o sin permisos.")

    if rpt.estado_generacion != 'Completado' or not rpt.ruta_archivo:
        return Response({'detail': 'El reporte aún no está disponible para descargar.'}, status=400)

    media_root = getattr(settings, 'MEDIA_ROOT', None) or ''
    abs_path = os.path.join(media_root, rpt.ruta_archivo)
    if not os.path.isfile(abs_path):
        raise Http404("Archivo de reporte no encontrado.")

    filename = os.path.basename(abs_path)
    f = open(abs_path, 'rb')
    return FileResponse(f, as_attachment=True, filename=filename, content_type='text/csv')

# =============================
# Endpoints públicos de reportes
# =============================

@api_view(['GET'])
@permission_classes([AllowAny])
def public_reportes_list(request):
    """Listado de reportes públicos (solo es_publico = True)."""
    qs = Reporte.objects.filter(es_publico=True)

    tipo = request.GET.get('tipo_reporte')
    if tipo:
        qs = qs.filter(tipo_reporte=tipo)

    formato = request.GET.get('formato')
    if formato:
        qs = qs.filter(formato_exportacion=formato)

    fecha_inicio = request.GET.get('fecha_inicio')
    if fecha_inicio:
        qs = qs.filter(fecha_inicio__gte=fecha_inicio)

    fecha_fin = request.GET.get('fecha_fin')
    if fecha_fin:
        qs = qs.filter(fecha_fin__lte=fecha_fin)

    data = []
    for rpt in qs.order_by('-fecha_generacion')[:100]:
        data.append({
            'codigo_reporte': rpt.codigo_reporte,
            'tipo_reporte': rpt.tipo_reporte,
            'nombre': rpt.nombre,
            'descripcion': rpt.descripcion,
            'fecha_generacion': rpt.fecha_generacion.isoformat() if rpt.fecha_generacion else None,
            'fecha_inicio': rpt.fecha_inicio.isoformat() if rpt.fecha_inicio else None,
            'fecha_fin': rpt.fecha_fin.isoformat() if rpt.fecha_fin else None,
            'formato_exportacion': rpt.formato_exportacion,
        })

    return Response({'results': data})

@api_view(['GET'])
@permission_classes([AllowAny])
def public_reporte_detail(request, codigo_reporte):
    """Metadatos de un reporte público específico."""
    try:
        rpt = Reporte.objects.get(codigo_reporte=codigo_reporte, es_publico=True)
    except Reporte.DoesNotExist:
        return Response({'detail': 'Reporte no encontrado'}, status=404)

    data = {
        'codigo_reporte': rpt.codigo_reporte,
        'tipo_reporte': rpt.tipo_reporte,
        'nombre': rpt.nombre,
        'descripcion': rpt.descripcion,
        'fecha_generacion': rpt.fecha_generacion.isoformat() if rpt.fecha_generacion else None,
        'fecha_inicio': rpt.fecha_inicio.isoformat() if rpt.fecha_inicio else None,
        'fecha_fin': rpt.fecha_fin.isoformat() if rpt.fecha_fin else None,
        'formato_exportacion': rpt.formato_exportacion,
        'es_publico': rpt.es_publico,
    }
    return Response(data)

@api_view(['GET'])
@permission_classes([AllowAny])
def public_dashboards_list(request):
    """Listado de dashboards públicos para ciudadanía."""
    qs = Dashboard.objects.filter(es_publico=True)

    tipo = request.GET.get('tipo_dashboard')
    if tipo:
        qs = qs.filter(tipo_dashboard=tipo)

    data = []
    for db in qs.order_by('orden_visualizacion', 'nombre')[:50]:
        data.append({
            'codigo_dashboard': db.codigo_dashboard,
            'nombre': db.nombre,
            'descripcion': db.descripcion,
            'tipo_dashboard': db.tipo_dashboard,
            'frecuencia_actualizacion': db.frecuencia_actualizacion,
            'es_publico': db.es_publico,
        })

    return Response({'results': data})

@api_view(['GET'])
@permission_classes([AllowAny])
def public_dashboard_detail(request, codigo_dashboard):
    """Detalle de un dashboard público con sus indicadores asociados."""
    try:
        db = Dashboard.objects.get(codigo_dashboard=codigo_dashboard, es_publico=True)
    except Dashboard.DoesNotExist:
        return Response({'detail': 'Dashboard no encontrado'}, status=404)

    asignaciones = (
        DashboardIndicador.objects
        .filter(id_dashboard=db)
        .select_related('id_indicador')
        .order_by('orden')
    )

    indicadores_data = []
    for asg in asignaciones:
        ind = asg.id_indicador
        indicadores_data.append({
            'codigo_indicador': ind.codigo_indicador,
            'nombre': ind.nombre,
            'descripcion': ind.descripcion,
            'tipo_visualizacion': ind.tipo_visualizacion,
            'frecuencia_actualizacion': ind.frecuencia_actualizacion,
            'valor_minimo': float(ind.valor_minimo) if ind.valor_minimo is not None else None,
            'valor_maximo': float(ind.valor_maximo) if ind.valor_maximo is not None else None,
            'valor_actual': float(ind.valor_actual) if ind.valor_actual is not None else None,
            'orden': asg.orden,
        })

    data = {
        'codigo_dashboard': db.codigo_dashboard,
        'nombre': db.nombre,
        'descripcion': db.descripcion,
        'tipo_dashboard': db.tipo_dashboard,
        'frecuencia_actualizacion': db.frecuencia_actualizacion,
        'es_publico': db.es_publico,
        'indicadores': indicadores_data,
    }
    return Response(data)

@api_view(['GET'])
@permission_classes([AllowAny])
def public_indicador_detail(request, codigo_indicador):
    """Detalle público de un indicador (definición + valor_actual)."""
    try:
        ind = Indicador.objects.get(codigo_indicador=codigo_indicador)
    except Indicador.DoesNotExist:
        return Response({'detail': 'Indicador no encontrado'}, status=404)

    data = {
        'codigo_indicador': ind.codigo_indicador,
        'nombre': ind.nombre,
        'descripcion': ind.descripcion,
        'formula': ind.formula,
        'tipo_visualizacion': ind.tipo_visualizacion,
        'frecuencia_actualizacion': ind.frecuencia_actualizacion,
        'valor_minimo': float(ind.valor_minimo) if ind.valor_minimo is not None else None,
        'valor_maximo': float(ind.valor_maximo) if ind.valor_maximo is not None else None,
        'valor_actual': float(ind.valor_actual) if ind.valor_actual is not None else None,
    }
    return Response(data)

@api_view(['GET'])
@permission_classes([AllowAny])
def public_indicador_serie(request, codigo_indicador):
    """Serie temporal de un indicador a partir de la tabla Estadistica."""
    periodo = request.GET.get('periodo')
    qs = Estadistica.objects.filter(tipo_metrica=codigo_indicador)
    if periodo:
        qs = qs.filter(periodo=periodo)

    qs = qs.order_by('fecha_calculo')
    series = []
    for est in qs[:365]:
        series.append({
            'codigo_estadistica': est.codigo_estadistica,
            'valor': float(est.valor),
            'unidad_medida': est.unidad_medida,
            'periodo': est.periodo,
            'fecha_calculo': est.fecha_calculo.isoformat() if est.fecha_calculo else None,
            'categoria': est.categoria,
            'area': est.area,
            'zona': est.zona,
        })

    return Response({'results': series})

@api_view(['GET'])
@permission_classes([AllowAny])
def public_tendencias_geograficas(request):
    """Listado público de tendencias geográficas agregadas."""
    qs = TendenciaGeografica.objects.all()

    periodo = request.GET.get('periodo_analisis')
    if periodo:
        qs = qs.filter(periodo_analisis=periodo)

    nivel = request.GET.get('nivel_criticidad')
    if nivel:
        qs = qs.filter(nivel_criticidad=nivel)

    distrito = request.GET.get('distrito')
    if distrito:
        qs = qs.filter(distrito=distrito)

    data = []
    for t in qs.order_by('-cantidad_denuncias')[:200]:
        data.append({
            'codigo_tendencia': t.codigo_tendencia,
            'zona': t.zona,
            'distrito': t.distrito,
            'cantidad_denuncias': t.cantidad_denuncias,
            'categoria_mas_frecuente': t.categoria_mas_frecuente,
            'tasa_resolucion': float(t.tasa_resolucion),
            'tiempo_promedio_atencion': float(t.tiempo_promedio_atencion),
            'periodo_analisis': t.periodo_analisis,
            'nivel_criticidad': t.nivel_criticidad,
        })

    return Response({'results': data})

@api_view(['GET'])
@permission_classes([AllowAny])
def public_ranking_areas(request):
    """Ranking público de desempeño por área responsable."""
    qs = RankingDesempeno.objects.select_related('id_area_responsable')

    periodo = request.GET.get('periodo_evaluacion')
    if periodo:
        qs = qs.filter(periodo_evaluacion=periodo)

    qs = qs.order_by('posicion')

    results = []
    for r in qs[:100]:
        results.append({
            'codigo_ranking': r.codigo_ranking,
            'periodo_evaluacion': r.periodo_evaluacion,
            'posicion': r.posicion,
            'area': getattr(r.id_area_responsable, 'nombre', 'Área'),
            'puntaje_total': float(r.puntaje_total),
            'denuncias_atendidas': r.denuncias_atendidas,
            'tasa_resolucion_area': float(r.tasa_resolucion_area),
            'tiempo_promedio_area': float(r.tiempo_promedio_area),
            'calificacion_promedio': float(r.calificacion_promedio) if r.calificacion_promedio is not None else None,
        })

    return Response({'results': results})


@api_view(['GET'])
@permission_classes([AllowAny])
def public_estadisticas_denuncias_resumen(request):
    """Resumen público de estadísticas de denuncias para la ciudadanía.

    Devuelve un payload adaptado a la vista EstadisticasPublicas.vue:
    - stats: total, resueltas, en_proceso, tiempo_promedio_horas
    - categorias: top categorías con cantidad
    - estados: conteo por estado
    - distritos: conteo por distrito y tasa de resolución
    """

    # Base queryset de denuncias (todas las públicas del sistema)
    denuncias_qs = Denuncia.objects.select_related('id_ubicacion', 'id_categoria')

    # Filtro opcional por rango de fechas (fecha_registro)
    from_date = request.GET.get('from')
    to_date = request.GET.get('to')
    if from_date:
        denuncias_qs = denuncias_qs.filter(fecha_registro__date__gte=from_date)
    if to_date:
        denuncias_qs = denuncias_qs.filter(fecha_registro__date__lte=to_date)

    total = denuncias_qs.count()

    # Conteos por estado
    por_estado = (
        denuncias_qs.values('estado')
        .annotate(cantidad=Count('id_denuncia'))
        .order_by('estado')
    )

    resueltas = next((e['cantidad'] for e in por_estado if e['estado'] == 'Resuelta'), 0)
    en_proceso = sum(
        e['cantidad']
        for e in por_estado
        if e['estado'] in ['En proceso', 'Asignado', 'En revisión']
    )

    # Tiempo promedio de resolución (en horas) a partir de Resolucion
    resoluciones_qs = Resolucion.objects.all()
    if from_date:
        resoluciones_qs = resoluciones_qs.filter(fecha_resolucion__date__gte=from_date)
    if to_date:
        resoluciones_qs = resoluciones_qs.filter(fecha_resolucion__date__lte=to_date)
    tiempo_promedio = resoluciones_qs.aggregate(promedio=Avg('tiempo_total_horas'))['promedio'] or 0

    # Top categorías por cantidad de denuncias
    categorias_qs = (
        denuncias_qs.values('id_categoria__nombre')
        .annotate(cantidad=Count('id_denuncia'))
        .order_by('-cantidad')[:5]
    )

    categorias_data = []
    for cat in categorias_qs:
        nombre = cat['id_categoria__nombre'] or 'Sin categoría'
        cantidad = cat['cantidad']
        porcentaje = (cantidad / total * 100) if total > 0 else 0
        categorias_data.append({
            'nombre': nombre,
            'cantidad': cantidad,
            'porcentaje': round(porcentaje, 1),
        })

    # Estados en formato sencillo para la UI
    estados_data = [
        {
            'nombre': e['estado'],
            'cantidad': e['cantidad'],
        }
        for e in por_estado
    ]

    # Denuncias por distrito
    distritos_qs = (
        denuncias_qs.values('id_ubicacion__distrito')
        .annotate(
            cantidad=Count('id_denuncia'),
        )
        .order_by('-cantidad')[:10]
    )

    # Para tasa de resolución por distrito usamos Resolucion + Tramitacion + Denuncia + Ubicacion
    # Esta parte puede ser costosa, así que la mantenemos simple.
    distritos_data = []
    for d in distritos_qs:
        nombre = d['id_ubicacion__distrito'] or 'Sin distrito'
        cantidad = d['cantidad']

        # Total denuncias del distrito
        distrito_denuncias = denuncias_qs.filter(id_ubicacion__distrito=nombre)
        total_distrito = distrito_denuncias.count()

        # Denuncias resueltas en este distrito via Resolucion/Tramitacion
        resueltas_distrito = (
            Resolucion.objects
            .filter(
                id_tramitacion__id_asignacion__id_denuncia__in=distrito_denuncias,
                tipo_resolucion='Resuelta',
            )
            .count()
        )

        tasa_resolucion = (
            resueltas_distrito / total_distrito * 100 if total_distrito > 0 else 0
        )

        distritos_data.append({
            'nombre': nombre,
            'cantidad': cantidad,
            'tasa_resolucion': round(tasa_resolucion, 1),
        })

    payload = {
        'stats': {
            'total': total,
            'resueltas': resueltas,
            'en_proceso': en_proceso,
            'tiempo_promedio_horas': round(tiempo_promedio, 1) if tiempo_promedio else 0,
        },
        'categorias': categorias_data,
        'estados': estados_data,
        'distritos': distritos_data,
    }

    return Response(payload)
