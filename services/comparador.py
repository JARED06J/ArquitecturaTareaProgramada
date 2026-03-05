from services.scheduler_services import ejecutar_planificacion

def comparar_algoritmos(procesos, quantum=2, configuracion_colas=None):

    resultados = {}

    resultados["FIFO"] = ejecutar_planificacion("FIFO", procesos)
    resultados["SJF"] = ejecutar_planificacion("SJF", procesos)
    resultados["RR"] = ejecutar_planificacion("RR", procesos, quantum=quantum)

    if configuracion_colas:
        resultados["MLQ"] = ejecutar_planificacion("MLQ", procesos, configuracion_colas=configuracion_colas) 

    return resultados