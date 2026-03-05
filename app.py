


from utils.file_loader import cargar_procesos_txt
from services.scheduler_services import ejecutar_planificacion

procesos = cargar_procesos_txt("procesos.txt")

resultado = ejecutar_planificacion("FIFO", procesos)

print(resultado)