from models.proceso import Proceso
from algorithms.fifo import ejecutar_fifo
from algorithms.sfj import ejecutar_sfj

procesos = [
    Proceso("P1", 0, 8),
    Proceso("P2", 1, 4),
    Proceso("P3", 2, 2)
]

resultado = ejecutar_sfj(procesos)

print(resultado)