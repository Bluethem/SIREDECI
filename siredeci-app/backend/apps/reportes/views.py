from django.utils import timezone
from django.db.models import Count, Avg
from django.db.models.functions import TruncWeek, TruncDate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
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
