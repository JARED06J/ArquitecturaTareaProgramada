def generar_detalle_procesos(procesos):
    """
    Genera lista detallada de tiempos por proceso
    """

    detalle = []

    for p in procesos:
        detalle.append({
            "id": p.id,
            "tiempo_llegada": p.tiempo_llegada,
            "rafaga": p.rafaga,
            "tiempo_finalizacion": p.tiempo_finalizacion,
            "tiempo_espera": p.tiempo_espera,
            "tiempo_retorno": p.tiempo_retorno
        })

    return detalle