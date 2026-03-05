from algorithms.fifo import ejecutar_fifo
from algorithms.sfj import ejecutar_sfj
from algorithms.round_robin import ejecutar_rr
from algorithms.mlq import ejecutar_mlq

def ejecutar_planificacion(tipo, procesos,quantum=None, configuracion_colas=None):
    if tipo == 'FIFO':
        return ejecutar_fifo(procesos)
    elif tipo == 'SJF':
        return ejecutar_sfj(procesos)
    elif tipo == 'RR':
        if quantum is None:
            raise ValueError("El quantum es requerido para el algoritmo Round Robin")
        return ejecutar_rr(procesos, quantum)
    elif tipo == 'MLQ':
        if configuracion_colas is None:
            raise ValueError("La configuración de colas es requerida para el algoritmo MLQ")
        return ejecutar_mlq(procesos, configuracion_colas)
    else:
        raise ValueError("Tipo de planificación no reconocido")
    