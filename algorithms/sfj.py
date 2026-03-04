from utils.metrics import calcular_metricas

def ejecutar_sfj(procesos):
    """
    Ejecuta sfj no apropiativo
    """

    for p in procesos:
        p.reiniciar()

    tiempo_actual = 0
    gantt = []
    procesos_pendientes = procesos.copy()
    procesos_completados = []

    while procesos_pendientes:
        #Procesos que ya llegaron

        disponibles = [p for p in procesos_pendientes if p.tiempo_llegada <= tiempo_actual]

        if not disponibles:
            # Si nadie ha llegado, avanzar el tiempo
            tiempo_actual = min(p.tiempo_llegada for p in procesos_pendientes)
            continue

        #Elegir el de menor rafaga

        proceso = min(disponibles, key=lambda p: p.rafaga)

        inicio = tiempo_actual
        fin = inicio + proceso.rafaga

        gantt.append({
            "proceso": proceso.id,
            "inicio": inicio,
            "fin": fin
        })

        proceso.tiempo_finalizacion = fin
        proceso.tiempo_retorno = fin - proceso.tiempo_llegada
        proceso.tiempo_espera = proceso.tiempo_retorno - proceso.rafaga

        tiempo_actual = fin
        procesos_pendientes.remove(proceso)
        procesos_completados.append(proceso)
    metricas = calcular_metricas(procesos_completados, tiempo_actual)

    return{
        "gantt": gantt,
        "metricas": metricas
    }
