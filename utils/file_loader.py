from models.proceso import Proceso

TIPOS_CLIENTE_VALIDOS = [
    "VIP",
    "AdultoMayor",
    "Embarazada",
    "Regular",
    "Foraneo"
]

def cargar_procesos_txt(ruta_archivo):
    procesos = []

    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
    except FileNotFoundError:
        raise Exception("No se encontró el archivo especificado.")

    numero_linea = 0
    for linea in lineas:
        numero_linea += 1
        linea = linea.strip()

        # Ignorar líneas vacías o comentarios
        if not linea or linea.startswith("#"):
            continue

        partes = linea.split(",")

        if len(partes) < 3:
            raise Exception(f"Error en línea {numero_linea}: formato inválido (ID, Llegada, Ráfaga).")

        id_proceso = partes[0].strip()

        # Validar números
        try:
            llegada = int(partes[1].strip())
            rafaga = int(partes[2].strip())
        except ValueError:
            raise Exception(f"Error en línea {numero_linea}: llegada y ráfaga deben ser números enteros.")

        if llegada < 0 or rafaga <= 0:
            raise Exception(f"Error en línea {numero_linea}: llegada >= 0 y ráfaga > 0.")

        # Tipo cliente opcional (por defecto Regular)
        tipo_cliente = "Regular"
        if len(partes) >= 4:
            tipo_cliente = partes[3].strip()
            if tipo_cliente not in TIPOS_CLIENTE_VALIDOS:
                raise Exception(f"Error en línea {numero_linea}: tipo '{tipo_cliente}' no reconocido.")

        # CORRECCIÓN: Instanciación por posición para evitar TypeError
        # El orden debe ser: ID, Tiempo Llegada, Ráfaga, Tipo Cliente
        proceso = Proceso(
            id_proceso,
            llegada,
            rafaga,
            tipo_cliente=tipo_cliente
        )

        procesos.append(proceso)

    if not procesos:
        raise Exception("El archivo no contiene procesos válidos.")

    return procesos
