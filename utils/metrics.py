def calcular_metricas(procesos, tiempo_total):

    total_espera = sum(p.espera for p in procesos)
    total_retorno = sum(p.retorno for p in procesos)
    total_rafagas = sum(p.rafaga for p in procesos)

    n = len(procesos)

    tiempo_promedio_espera = total_espera / n if n > 0 else 0
    tiempo_promedio_retorno = total_retorno / n if n > 0 else 0

    utilizacion_cpu = (total_rafagas / tiempo_total) * 100 if tiempo_total > 0 else 0

    return {
        "tiempo_promedio_espera": round(tiempo_promedio_espera, 2),
        "tiempo_promedio_retorno": round(tiempo_promedio_retorno, 2),
        "utilizacion_cpu": round(utilizacion_cpu, 2)
    }
