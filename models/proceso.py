class Proceso:
    def __init__(self, id, tiempo_llegada, rafaga, prioridad=0, tipo_cliente="Regular"):
        self.id = id
        self.tiempo_llegada = tiempo_llegada
        self.rafaga = rafaga
        self.prioridad = prioridad
        self.tipo_cliente = tipo_cliente
        
        self.tiempo_restante = rafaga
        self.tiempo_finalizacion = 0
        self.tiempo_espera = 0
        self.tiempo_retorno = 0

    def reiniciar(self):
        self.tiempo_restante = self.rafaga
        self.tiempo_finalizacion = 0
        self.tiempo_espera = 0
        self.tiempo_retorno = 0