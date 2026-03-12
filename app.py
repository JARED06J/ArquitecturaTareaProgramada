from flask import Flask, render_template, request, send_file
import os
from models.proceso import Proceso
from utils.file_loader import cargar_procesos_txt
from algorithms.mlq import ejecutar_mlq
from utils.metrics import calcular_metricas  
from datetime import datetime

app = Flask(__name__)

# Configuración de archivos y carpetas
UPLOAD_FOLDER = 'uploads'
HISTORIAL_FILE = 'historial_simulaciones.txt' 

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def bienvenida():
    return render_template("bienvenida.html")

@app.route("/simulador")
def index():
    return render_template("index.html")

@app.route('/simular', methods=['POST'])
def simular():
    lista_procesos = []
    
    # --- Carga de Datos ---
    if 'archivo' in request.files and request.files['archivo'].filename != '':
        archivo = request.files['archivo']
        ruta = os.path.join(UPLOAD_FOLDER, archivo.filename)
        archivo.save(ruta)
        try:
            lista_procesos = cargar_procesos_txt(ruta)
        except Exception as e:
            return f"Error al cargar archivo: {str(e)}"
    else:
        ids = request.form.getlist('id[]')
        llegadas = request.form.getlist('llegada[]')
        rafagas = request.form.getlist('rafaga[]')
        tipos = request.form.getlist('tipo_cliente[]')

        for i in range(len(ids)):
            if ids[i].strip():
                p = Proceso(ids[i], int(llegadas[i]), int(rafagas[i]), tipo_cliente=tipos[i])
                lista_procesos.append(p)

    if not lista_procesos:
        return "No se ingresaron procesos para simular."

    # --- configuración de Algoritmos MLQ ---
    configuracion_colas = {
        "VIP": {"prioridad": 1, "algoritmo": request.form.get('alg_alta'), "quantum": int(request.form.get('q_alta', 2))},
        "AdultoMayor": {"prioridad": 1, "algoritmo": request.form.get('alg_alta'), "quantum": int(request.form.get('q_alta', 2))},
        "Embarazada": {"prioridad": 1, "algoritmo": request.form.get('alg_alta'), "quantum": int(request.form.get('q_alta', 2))},
        "Regular": {"prioridad": 2, "algoritmo": request.form.get('alg_baja'), "quantum": int(request.form.get('q_baja', 2))},
        "Foraneo": {"prioridad": 2, "algoritmo": request.form.get('alg_baja'), "quantum": int(request.form.get('q_baja', 2))}
    }

    resultado = ejecutar_mlq(lista_procesos, configuracion_colas)
    
    # --- Cálculo de Métricas ---
    tiempo_total_simulacion = max(p.fin for p in resultado) if resultado else 0
    
    metricas = calcular_metricas(resultado, tiempo_total_simulacion)
    
    procesos_json = []
    modulos = ["Módulo 1", "Módulo 2", "Módulo 3", "Módulo 4"]

    for i, p in enumerate(resultado):
        # Asignamos cajero/módulo
        p.cajero = modulos[i % len(modulos)]
        
        # Clasificamos cola para la tabla
        p.cola = "COLA 1" if p.tipo_cliente in ['VIP', 'AdultoMayor', 'Embarazada'] else "COLA 2"
        
        procesos_json.append({
            'id': p.id, 
            'inicio': p.inicio, 
            'fin': p.fin,
            'tipo': p.tipo_cliente, 
            'espera': p.espera, 
            'retorno': p.retorno,
            'cajero': p.cajero
        })

    # --- Guardar en Historial ---
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    es_nuevo = not os.path.exists(HISTORIAL_FILE)

    with open(HISTORIAL_FILE, "a", encoding="utf-8") as f:
        if es_nuevo:
            f.write("Fecha_Hora,Total_Tiquetes,Promedio_Espera,Promedio_Retorno,Eficiencia\n")
        f.write(f"{ahora},{len(resultado)},{metricas['tiempo_promedio_espera']},{metricas['tiempo_promedio_retorno']},{metricas['utilizacion_cpu']}%\n")

    # --- Renderizado de Resultados ---
    return render_template(
        "results.html", 
        procesos=resultado, 
        procesos_js=procesos_json, 
        promedio_espera=metricas['tiempo_promedio_espera'], 
        promedio_retorno=metricas['tiempo_promedio_retorno'],
        utilizacion=metricas['utilizacion_cpu']
    )

@app.route('/descargar')
def descargar():
    return send_file(HISTORIAL_FILE, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
