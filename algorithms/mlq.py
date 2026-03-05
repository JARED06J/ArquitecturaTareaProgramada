from collections import deque
from utils.detalle_procesos import generar_detalle_procesos
from utils.metrics import calcular_metricas

def ejecutar_mlq(procesos, configuracion_colas):
    for p in procesos:
        p.reiniciar()

    tiempo_actual = 0
    gantt = []
    completados = []


    while len(completados) < len(procesos):
        #Procesos disponibles en ese tiempo
        disponibles = [
            p for p in procesos
            if p.tiempo_llegada <= tiempo_actual and p.tiempo_restante > 0
        ]

        if not disponibles:
            tiempo_actual += 1
            continue

        #Determinar cola de mayor prioridad disponible
        cola_activa = min(disponibles, key=lambda x: configuracion_colas[p.tipo_cliente]["prioridad"]).tipo_cliente
        config = configuracion_colas[cola_activa]
        procesos_cola = [p for p in disponibles if p.tipo_cliente == cola_activa]

        #=== FIFO ===
        if config["algoritmo"] == "FIFO":
            proceso = sorted(procesos_cola, key=lambda x: x.tiempo_llegada)[0]
            tiempo_ejecucion = proceso.tiempo_restante

        #=== SJF ===
        elif config["algoritmo"] == "SJF":
            proceso = sorted(procesos_cola, key=lambda x: x.tiempo_restante)
            tiempo_ejecucion = proceso.tiempo_restante

        #=== RR ===
        elif config["algoritmo"] == "RR":
            proceso = procesos_cola[0]
            quantum = config["quantum"]
            tiempo_ejecucion = min(quantum, proceso.tiempo_restante)

        inicio = tiempo_actual
        fin = inicio + tiempo_ejecucion

        gantt.append({
            "proceso": proceso.id,
            "inicio": inicio,
            "fin": fin
        })

        proceso.tiempo_restante -= tiempo_ejecucion
        tiempo_actual = fin

        if proceso.tiempo_restante == 0:
            proceso.tiempo_finalizacion = tiempo_actual
            proceso.tiempo_retorno = proceso.tiempo_finalizacion - proceso.tiempo_llegada
            proceso.tiempo_espera = proceso.tiempo_retorno - proceso.rafaga
            completados.append(proceso)
    metricas = calcular_metricas(procesos, tiempo_actual)

    detalle = generar_detalle_procesos(procesos)

    return {
        "gantt": gantt,
        "metricas": metricas,
        "procesos": detalle
    }
