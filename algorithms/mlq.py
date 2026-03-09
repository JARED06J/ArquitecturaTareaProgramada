from collections import deque

def ejecutar_mlq(procesos, configuracion_colas):
    # Preparación inicial de los tiquetes
    for p in procesos:
        p.reiniciar()
        p.inicio = None 
        p.fin = 0

    tiempo_actual = 0
    completados = []
    n = len(procesos)

    while len(completados) < n:
        disponibles = [
            p for p in procesos
            if p.tiempo_llegada <= tiempo_actual and p.tiempo_restante > 0
        ]

        if not disponibles:
            tiempo_actual += 1
            continue

        prioridad_minima = min(configuracion_colas[p.tipo_cliente]["prioridad"] for p in disponibles)
        
        # Filtramos solo los procesos que pertenecen a esa prioridad más alta disponible
        procesos_prioritarios = [
            p for p in disponibles 
            if configuracion_colas[p.tipo_cliente]["prioridad"] == prioridad_minima
        ]

        # Selección del proceso según el algoritmo de su cola
        proceso = procesos_prioritarios[0] 
        config = configuracion_colas[proceso.tipo_cliente]

        if config["algoritmo"] == "FIFO":
            proceso = sorted(procesos_prioritarios, key=lambda x: x.tiempo_llegada)[0]
            tiempo_ejecucion = proceso.tiempo_restante

        elif config["algoritmo"] == "SJF":
            # Shortest Job First dentro de la cola de prioridad
            proceso = sorted(procesos_prioritarios, key=lambda x: x.tiempo_restante)[0]
            tiempo_ejecucion = proceso.tiempo_restante

        elif config["algoritmo"] == "RR":
            # Round Robin: usa el quantum definido en el formulario
            quantum = config.get("quantum", 2)
            tiempo_ejecucion = min(quantum, proceso.tiempo_restante)
        else:
            # Por defecto tratamos como FIFO si no se reconoce el algoritmo
            tiempo_ejecucion = proceso.tiempo_restante

        # Registro de tiempos para el Diagrama de Gantt
        if proceso.inicio is None:
            proceso.inicio = tiempo_actual
        
        tiempo_actual += tiempo_ejecucion
        proceso.tiempo_restante -= tiempo_ejecucion

        # Finalización del proceso y cálculo de métricas
        if proceso.tiempo_restante <= 0:
            proceso.fin = tiempo_actual
            proceso.retorno = proceso.fin - proceso.tiempo_llegada
            proceso.espera = proceso.retorno - proceso.rafaga
            completados.append(proceso)

    return procesos
