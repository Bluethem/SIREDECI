from django.utils import timezone
from django.db.models import Count, Avg
from django.db.models.functions import TruncWeek, TruncDate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.denuncias.models import Denuncia, Resolucion, Ubicacion
from apps.reportes.models import Indicador, RankingDesempeno


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_summary(request):
    """
    Resumen para el dashboard ejecutivo de admin.
    Devuelve totales y métricas básicas para tarjetas y barras.
    """
    # Totales
    total_denuncias = Denuncia.objects.count()

    # Denuncias hoy (por fecha_registro)
    today = timezone.now().date()
    denuncias_hoy = Denuncia.objects.filter(fecha_registro__date=today).count()

    # Pendientes de validación
    pendientes_validacion = Denuncia.objects.filter(requiere_validacion=True).count()

    # Distribución por estado - simplificado
    estados_counts = {}
    try:
        estados_qs = (
            Denuncia.objects.values('estado')
            .annotate(count=Count('id_denuncia'))
        )
        estados_counts = {row['estado']: row['count'] for row in estados_qs}
    except Exception as e:
        print(f"Error en estados_qs: {e}")
        estados_counts = {}

    data = {
        'total': total_denuncias,
        'hoy': {
            'denuncias_hoy': denuncias_hoy,
            'pendientes_validacion': pendientes_validacion,
        },
        'estados': estados_counts,
    }

    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_categorias(request):
    """
    Distribución de denuncias por categoría (top 6)
    """
    qs = (
        Denuncia.objects.values('id_categoria__nombre')
        .annotate(count=Count('id_denuncia'))
        .order_by('-count')[:6]
    )
    total = Denuncia.objects.count() or 1
    items = []
    for row in qs:
        nombre = row['id_categoria__nombre'] or 'Sin categoría'
        count = row['count']
        perc = round(count * 100.0 / total, 2)
        items.append({'nombre': nombre, 'count': count, 'porcentaje': perc})
    return Response({'total': total, 'categorias': items})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_temporal(request):
    """
    Serie temporal semanal (últimas 4 semanas): registradas vs resueltas
    """
    now = timezone.now()
    start = now - timezone.timedelta(weeks=4)
    # Registradas por semana
    reg = (
        Denuncia.objects.filter(fecha_registro__gte=start)
        .annotate(week=TruncWeek('fecha_registro'))
        .values('week')
        .annotate(count=Count('id_denuncia'))
        .order_by('week')
    )
    # Resueltas por semana (por fecha_resolucion)
    res = (
        Resolucion.objects.filter(fecha_resolucion__gte=start)
        .annotate(week=TruncWeek('fecha_resolucion'))
        .values('week')
        .annotate(count=Count('id_resolucion'))
        .order_by('week')
    )
    # Normalizar a 4 semanas
    weeks = []
    for i in range(4, 0, -1):
        wk_start = (now - timezone.timedelta(weeks=i)).date()
        weeks.append(wk_start.isocalendar())  # (year, week, weekday)
    def to_map(qs):
        m = {}
        for row in qs:
            wk = row['week'].date().isocalendar() if row['week'] else None
            if wk:
                key = f"{wk[0]}-W{wk[1]}"
                m[key] = row['count']
        return m
    reg_map = to_map(reg)
    res_map = to_map(res)
    series = []
    for i in range(4, 0, -1):
        wk_date = (now - timezone.timedelta(weeks=i)).date()
        y, w, _ = wk_date.isocalendar()
        key = f"{y}-W{w}"
        series.append({
            'label': key,
            'registradas': reg_map.get(key, 0),
            'resueltas': res_map.get(key, 0),
        })
    return Response({'series': series})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def dashboard_alerts(request):
    """
    Alertas simples para panel derecho.
    """
    try:
        # Urgentes sin asignar
        urgentes_sin_asignar = Denuncia.objects.filter(
            prioridad='Urgente'
        ).exclude(
            estado__in=['Asignado', 'En proceso', 'Resuelta', 'Cerrada']
        ).count()

        # Próximas a vencer (24h)
        hace_24h = timezone.now() - timezone.timedelta(hours=24)
        proximas_vencer = Denuncia.objects.filter(
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
