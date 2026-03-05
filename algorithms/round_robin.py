from collections import deque
from utils.detalle_procesos import generar_detalle_procesos
from utils.metrics import calcular_metricas

def ejecutar_rr(procesos, quantum):
    """
    Ejecuta Round Robin
    """

    for p in procesos:
        p.reiniciar()

    tiempo_actual = 0
    gantt = []
    cola = deque()
    procesos_pendientes = sorted(procesos, key=lambda x: x.tiempo_llegada)
    completados = []

    i = 0 #Indice  para agregar los procesos que van llegando

    while cola or i < len(procesos_pendientes):
        #Agregar procesos que ya llegaron
        while i < len(procesos_pendientes) and procesos_pendientes[i].tiempo_llegada <= tiempo_actual:
            cola.append(procesos_pendientes[i])
            i += 1
        if not cola:
            #Si no hay procesos listos, avanzar el tiempo
            tiempo_actual = procesos_pendientes[i].tiempo_llegada
            continue
        proceso = cola.popleft()

        inicio = tiempo_actual
        tiempo_ejecucion = min(quantum, proceso.tiempo_restante)
        fin = inicio + tiempo_ejecucion


        gantt.append({
            "proceso": proceso.id,
            "inicio": inicio,
            "fin": fin
        })

        proceso.tiempo_restante -= tiempo_ejecucion
        tiempo_actual = fin

        #Ver si llegaron nuevos procesos durante la ejecucion

        while i < len(procesos_pendientes) and procesos_pendientes[i].tiempo_llegada <= tiempo_actual:
            cola.append(procesos_pendientes[i])
            i += 1

        if proceso.tiempo_restante > 0:
            cola.append(proceso)

        else:
            proceso.tiempo_finalizacion = tiempo_actual
            proceso.tiempo_retorno = proceso.tiempo_finalizacion - proceso.tiempo_llegada
            proceso.tiempo_espera = proceso.tiempo_retorno - proceso.rafaga
            completados.append(proceso)
    metricas = calcular_metricas(completados, tiempo_actual)

    detalle = generar_detalle_procesos(completados)

    return {
        "gantt": gantt,
        "metricas": metricas,
        "procesos": detalle
    }

