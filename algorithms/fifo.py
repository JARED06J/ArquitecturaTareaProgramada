from utils.metrics import calcular_metricas

def ejecutar_fifo(procesos):

    """
        Ejecuta el algoritmo FIFO(First In, First Out) segun lo que pidio el profe en el PDF.
        :param procesos: Lista de objetos Proceso con los atributos necesarios para el algoritmo.
        :return: dict con gantt y metricas para UI.
    """
    #Reiniciar procesos(por si vienen de otra simulacion)
    for p in procesos:
        p.reiniciar()

    #Ordenar procesos por orden de llegada

    procesos_ordenados = sorted(procesos, key=lambda p: p.tiempo_llegada)

    tiempo_actual = 0
    gantt = []
    for proceso in procesos_ordenados:
        #Si el cpu esta vacio y el proceso aun no ha llegado:
        if tiempo_actual < proceso.tiempo_llegada:
            tiempo_actual = proceso.tiempo_llegada

        inicio = tiempo_actual
        fin = inicio + proceso.rafaga

        #Registar en Gantt

        gantt.append({
            "proceso": proceso.id,
            "inicio": inicio,
            "fin": fin
        })

        #Actualizar tiempos

        proceso.tiempo_finalizacion = fin
        proceso.tiempo_retorno = fin - proceso.tiempo_llegada
        proceso.tiempo_espera = proceso.tiempo_retorno - proceso.rafaga

        tiempo_actual = fin

    #Calcular metricas

    metricas = calcular_metricas(procesos_ordenados, tiempo_actual)

    return{
        "gantt": gantt,
        "metricas": metricas
    }
