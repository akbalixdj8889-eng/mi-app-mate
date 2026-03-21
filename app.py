import streamlit as st
import random
import time
import matplotlib.pyplot as plt
import io
import requests

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Misión Funciones", layout="centered")

# --- 2. CSS PERSONALIZADO ---
st.markdown("""
    <style>
    .main { background-color: #2d0b2a; color: white; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; font-weight: bold; }
    .question-card { background-color: white; padding: 20px; border-radius: 15px; color: #2d0b2a; margin-bottom: 20px; }
    .status-panel { background: rgba(255,255,255,0.1); padding: 10px; border-radius: 10px; text-align: center; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

       # --- 3. BANCO DE PREGUNTAS ACTUALIZADO Y HUMANIZADO ---

if 'banco_completo' not in st.session_state:
    st.session_state.banco_completo = [
        # ================= TEMA A =================
        {"id": "A1", "mision": 1, "pregunta": "Un dron de vigilancia vuela en línea recta pasando por A=(-4,8) y B=(4,2). ¿Cuál es su pendiente (m) y su altura inicial (b)?", "opciones": ["m = 5, b = -3/4", "m = 3/4, b = -5", "m = -3/4, b = -5", "m = -3/4, b = 5"], "correcta_texto": "m = -3/4, b = 5", "t_max": 75},
        {"id": "A2", "mision": 1, "pregunta": "En un mapa de coordenadas, una carretera une A(1, 3) con B(2, 10). ¿Cuál es la ecuación que describe esta ruta?", "opciones": ["y = 3/7x + 4", "y = 2/7x - 4", "y = -2/7x - 4", "y = 7x - 4"], "correcta_texto": "y = 7x - 4", "t_max": 75},
        {"id": "A3", "mision": 1, "pregunta": "Un rayo láser se dispara desde P(-6, 2) con una inclinación m = -2/3. ¿Cuál es su fórmula de trayectoria?", "opciones": ["y = -2/3x - 2", "y = -2/3x - 3", "y = -3/2x - 3", "y = -3/2x - 2"], "correcta_texto": "y = -2/3x - 2", "t_max": 75},
        {"id": "A4", "mision": 1, "pregunta": "La trayectoria de un barco es y = -4/5x - 3. ¿Cuál de estas rutas es PARALELA a la del barco?", "opciones": ["y = -4/5x + 3", "y = 5/4x + 2", "y = 4/5x + 10", "y = -5/4x - 7"], "correcta_texto": "y = -4/5x + 3", "t_max": 60},
        {"id": "A5", "mision": 1, "pregunta": "Para cruzar un río de forma PERPENDICULAR a la corriente (y = 2/3x + 1), ¿qué trayectoria debe seguir el bote?", "opciones": ["y = 2/3x - 5", "y = 3/2x + 2", "y = -2/3x + 4", "y = -3/2x + 5"], "correcta_texto": "y = -3/2x + 5", "t_max": 60},
        {"id": "A6", "mision": 1, "pregunta": "Una pendiente de m = -5/4 pasa por el punto (4,2). ¿Qué ecuación la representa y por qué otro punto pasa?", "opciones": ["y = -4/5x + 5 (9,-2)", "y = -5/4x + 7 (8,-3)", "y = -5/4x + 7 (8,2)", "y = -4/5x + 5 (0,5)"], "correcta_texto": "y = -5/4x + 7 (8,-3)", "t_max": 80},
        {"id": "A7", "mision": 2, "pregunta": "Un horno inicia a 15°C y sube 10°C cada 3 min. ¿Qué función representa su temperatura 'y' tras 'x' minutos?", "opciones": ["y = 15x + 3/10", "y = 3/10x + 15", "y = 15x + 10/3", "y = 10/3x + 15"], "correcta_texto": "y = 10/3x + 15", "t_max": 90},
        {"id": "A8", "mision": 2, "pregunta": "Un taxi cobra $7 de base y $2 por cada 3 km. ¿Cuál es el costo total por un viaje de 15 km?", "opciones": ["$10", "$23", "$17", "$15"], "correcta_texto": "$17", "t_max": 90},
        {"id": "A9", "mision": 2, "pregunta": "Tanque A (en 2 min tiene 10L, en 8 min tiene 40L). Tanque B (en 1 min tiene 50L, en 11 min tiene 10L). ¿En qué minuto se igualan?", "opciones": ["4", "6", "8", "10"], "correcta_texto": "6", "t_max": 120},
        {"id": "A10", "mision": 2, "pregunta": "Andrés tiene $150 y ahorra $50 por semana. Beatriz tiene $950 y gasta $150 por semana. ¿En qué semana tendrán lo mismo?", "opciones": ["2", "3", "4", "5"], "correcta_texto": "4", "t_max": 120},

        # ================= TEMA B =================
        {"id": "B1", "mision": 1, "pregunta": "Una rampa pasa por A=(-3, 5) y B=(3, 1). Calcula su pendiente (m) y su punto de corte (b):", "opciones": ["m = 2/3, b = 3", "m = -2/3, b = 3", "m = -3/2, b = -3", "m = 3/2, b = 3"], "correcta_texto": "m = -2/3, b = 3", "t_max": 75},
        {"id": "B2", "mision": 1, "pregunta": "Halla la ecuación de la recta que une los puntos A(-2, -5) y B(5, -7):", "opciones": ["y = -2/7x - 39/7", "y = 2/7x + 39/7", "y = -7/2x - 4", "y = 7/2x + 4"], "correcta_texto": "y = -2/7x - 39/7", "t_max": 75},
        {"id": "B3", "mision": 1, "pregunta": "Una antena transmite desde P(5, -2) con m = -4/5. ¿Cuál es su modelo matemático?", "opciones": ["y = -4/5x + 2", "y = -4/5x - 6", "y = 4/5x + 2", "y = -5/4x + 2"], "correcta_texto": "y = -4/5x + 2", "t_max": 75},
        {"id": "B4", "mision": 1, "pregunta": "Si una cerca sigue la línea y = 3/7x + 5, ¿cuál de estas opciones es una línea PARALELA?", "opciones": ["y = -3/7x + 5", "y = 7/3x - 1", "y = 3/7x - 8", "y = -7/3x + 2"], "correcta_texto": "y = 3/7x - 8", "t_max": 60},
        {"id": "B5", "mision": 1, "pregunta": "Una tubería (y = -5/2x - 4) debe cruzarse con otra de forma PERPENDICULAR. ¿Cuál es la ecuación de la segunda?", "opciones": ["y = 5/2x + 1", "y = 2/5x + 10", "y = -2/5x - 4", "y = -5/2x + 3"], "correcta_texto": "y = 2/5x + 10", "t_max": 60},
        {"id": "B6", "mision": 1, "pregunta": "Halla la recta con m = 1/3 que pasa por P(6, 4) e identifica otro punto por donde pase:", "opciones": ["y = 1/3x + 2 (Punto 0, 2)", "y = 3x - 2 (Punto 1, 1)", "y = 1/3x + 4 (Punto 3, 5)", "y = -1/3x + 2 (Punto 6, 0)"], "correcta_texto": "y = 1/3x + 2 (Punto 0, 2)", "t_max": 80},
        {"id": "B7", "mision": 2, "pregunta": "Un enfriador está a 20°C y baja 4°C cada 3 min. ¿Qué función describe su temperatura?", "opciones": ["y = 3/4x + 20", "y = -4/3x + 20", "y = 4/3x - 20", "y = -3/4x + 20"], "correcta_texto": "y = -4/3x + 20", "t_max": 90},
        {"id": "B8", "mision": 2, "pregunta": "Mensajería: $10 de cargo básico más $3 por cada 4 km recorridos. ¿Cuánto cuesta un envío a 20 km?", "opciones": ["$15", "$20", "$25", "$30"], "correcta_texto": "$25", "t_max": 90},
        {"id": "B9", "mision": 2, "pregunta": "Tanque A (15L inicial, sube 3L c/2 min). Tanque B (45L inicial, baja 5L c/2 min). ¿En qué minuto tienen igual nivel?", "opciones": ["6", "7.5", "10", "15"], "correcta_texto": "7.5", "t_max": 120},
        {"id": "B10", "mision": 2, "pregunta": "Camilo tiene $400 y gasta $25 cada 2 semanas. Sara tiene $100 y ahorra $75 cada 2 semanas. ¿En qué semana se igualan?", "opciones": ["4", "6", "8", "10"], "correcta_texto": "6", "t_max": 120},

        # ================= TEMA C =================
        {"id": "C1", "mision": 1, "pregunta": "Una tirolesa une A=(-5, 7) con B=(5, 3). Calcula su pendiente (m) y su punto de corte (b):", "opciones": ["m = 2/5, b = 5", "m = -5/2, b = 5", "m = -2/5, b = 5", "m = 5/2, b = -5"], "correcta_texto": "m = -2/5, b = 5", "t_max": 75},
        {"id": "C2", "mision": 1, "pregunta": "Ecuación de la recta que pasa por los puntos de control A(-3, 1) y B(6, 7):", "opciones": ["y = 2/3x + 3", "y = -2/3x + 3", "y = 3/2x - 1", "y = 2/3x - 3"], "correcta_texto": "y = 2/3x + 3", "t_max": 75},
        {"id": "C3", "mision": 1, "pregunta": "Desde P(-4, 2) sale un cable con pendiente m = 3/4. ¿Cuál es su ecuación?", "opciones": ["y = 3/4x - 5", "y = 3/4x + 5", "y = -3/4x + 5", "y = 4/3x + 5"], "correcta_texto": "y = 3/4x + 5", "t_max": 75},
        {"id": "C4", "mision": 1, "pregunta": "Una pista es y = -2/9x + 10. ¿Cuál de estas opciones representa una pista PARALELA?", "opciones": ["y = 9/2x + 10", "y = -2/9x - 4", "y = 2/9x + 4", "y = -9/2x + 1"], "correcta_texto": "y = -2/9x - 4", "t_max": 60},
        {"id": "C5", "mision": 1, "pregunta": "Una viga (y = 7/3x - 2) debe sostenerse con otra PERPENDICULAR. ¿Qué ecuación tiene la segunda viga?", "opciones": ["y = -3/7x + 6", "y = 3/7x + 6", "y = -7/3x - 2", "y = 7/3x + 4"], "correcta_texto": "y = -3/7x + 6", "t_max": 60},
        {"id": "C6", "mision": 1, "pregunta": "Halla la recta con m = -3/2 que pasa por P(4, -1) y señala otro punto de su trayectoria:", "opciones": ["y = -3/2x + 5 (Punto 0, 5)", "y = 3/2x - 7 (Punto 2, -4)", "y = -3/2x + 5 (Punto 2, 1)", "y = 2/3x + 1 (Punto 3, 3)"], "correcta_texto": "y = -3/2x + 5 (Punto 0, 5)", "t_max": 80},
        {"id": "C7", "mision": 2, "pregunta": "Un vehículo con 40L consume 5L cada 4 km. ¿Qué función modela el combustible restante según los km recorridos?", "opciones": ["y = 4/5x + 40", "y = -5/4x + 40", "y = 5/4x - 40", "y = -4/5x + 40"], "correcta_texto": "y = -5/4x + 40", "t_max": 90},
        {"id": "C8", "mision": 2, "pregunta": "Un servicio técnico cobra $15 base y $5 por cada 2 horas de labor. ¿Cuánto cuesta una reparación de 7 horas?", "opciones": ["$30.0", "$32.5", "$35.0", "$17.5"], "correcta_texto": "$32.5", "t_max": 90},
        {"id": "C9", "mision": 2, "pregunta": "Tanque A (100L inicial, pierde 10L c/3 min). Tanque B (20L inicial, gana 10L c/3 min). ¿En qué minuto se cruzan?", "opciones": ["10", "12", "15", "18"], "correcta_texto": "12", "t_max": 120},
        {"id": "C10", "mision": 2, "pregunta": "Marta tiene $600 y gasta $40 cada 3 semanas. Luis tiene $1000 y gasta $120 cada 3 semanas. ¿En qué semana se igualan?", "opciones": ["Semana 12", "Semana 15", "Semana 18", "Semana 20"], "correcta_texto": "Semana 15", "t_max": 120},

        # ================= TEMA D =================
        {"id": "D1", "mision": 1, "pregunta": "Un puente recto une A=(-6, 1) con B=(6, 6). Halla su pendiente (m) y su intercepto (b):", "opciones": ["m = 5/12, b = 3.5", "m = -5/12, b = 3.5", "m = 12/5, b = -3", "m = 5/12, b = -3.5"], "correcta_texto": "m = 5/12, b = 3.5", "t_max": 75},
        {"id": "D2", "mision": 1, "pregunta": "Determina la ecuación de la recta que pasa por los puntos de anclaje A(-4, 8) y B(2, -1):", "opciones": ["y = 3/2x + 2", "y = -3/2x + 2", "y = -2/3x + 2", "y = 3/2x - 2"], "correcta_texto": "y = -3/2x + 2", "t_max": 75},
        {"id": "D3", "mision": 1, "pregunta": "Una rampa inicia en P(3, -4) con inclinación m = -1/3. ¿Cuál es su fórmula?", "opciones": ["y = -1/3x - 3", "y = -1/3x + 3", "y = 1/3x - 3", "y = -3x - 3"], "correcta_texto": "y = -1/3x - 3", "t_max": 75},
        {"id": "D4", "mision": 1, "pregunta": "Si un cable sigue la línea y = -5/6x - 1, ¿cuál de estas opciones es PARALELA?", "opciones": ["y = 6/5x + 4", "y = 5/6x - 1", "y = -5/6x + 9", "y = -6/5x + 2"], "correcta_texto": "y = -5/6x + 9", "t_max": 60},
        {"id": "D5", "mision": 1, "pregunta": "Una calle (y = -1/4x + 5) cruza con otra de forma PERPENDICULAR. ¿Cuál es la ecuación de la segunda calle?", "opciones": ["y = -4x + 2", "y = 1/4x - 5", "y = 4x - 8", "y = -4/1x + 3"], "correcta_texto": "y = 4x - 8", "t_max": 60},
        {"id": "D6", "mision": 1, "pregunta": "Halla la recta con m = 4/5 que pasa por P(5, 7) e indica su punto de corte con el eje Y:", "opciones": ["y = 4/5x + 3 (Corta en 3)", "y = -4/5x + 3 (Corta en 3)", "y = 4/5x - 3 (Corta en -3)", "y = 5/4x + 3 (Corta en 3)"], "correcta_texto": "y = 4/5x + 3 (Corta en 3)", "t_max": 80},
        {"id": "D7", "mision": 2, "pregunta": "Un depósito de 80 galones pierde 3 galones cada 2 horas por una fuga. ¿Qué función describe el agua restante?", "opciones": ["y = 3/2x + 80", "y = -2/3x + 80", "y = -3/2x + 80", "y = -3/2x - 80"], "correcta_texto": "y = -3/2x + 80", "t_max": 90},
        {"id": "D8", "mision": 2, "pregunta": "Un carpintero cobra $20 base y $15 por cada 4 horas de trabajo. ¿Cuánto cobrará por un proyecto de 12 horas?", "opciones": ["$45", "$65", "$35", "$70"], "correcta_texto": "$65", "t_max": 90},
        {"id": "D9", "mision": 2, "pregunta": "Globo A (10m de altura, sube 5m cada 4 seg). Globo B (40m de altura, baja 7m cada 4 seg). ¿En qué segundo se cruzan?", "opciones": ["8", "10", "12", "15"], "correcta_texto": "10", "t_max": 120},
        {"id": "D10", "mision": 2, "pregunta": "Daniel tiene $500 y gasta $30 cada 2 semanas. Sofía tiene $800 y gasta $80 cada 2 semanas. ¿En qué semana tendrán lo mismo?", "opciones": ["6", "10", "12", "14"], "correcta_texto": "12", "t_max": 120}
    ]


# --- 4. FUNCIONES DE APOYO ---
def enviar_a_google(nombre, curso, mision, aciertos):
    url_script = "TU_URL_DE_APPS_SCRIPT" # REEMPLAZA ESTO
    datos = {"nombre": nombre, "curso": curso, "mision": mision, "aciertos": aciertos}
    try: requests.post(url_script, json=datos)
    except: pass

def crear_imagen(texto, opciones, ocultas=[]):
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('white')
    letras = ["A)", "B)", "C)", "D)"]
    finales = []
    for i, opt in enumerate(opciones):
        if letras[i][0] in ocultas: finales.append(f"{letras[i]} [ ELIMINADA ]")
        else: finales.append(f"{letras[i]} {opt}")
    
    cuerpo = f"{texto}\n\n" + "\n".join(finales)
    ax.text(0.05, 0.9, cuerpo, fontsize=15, fontweight='bold', wrap=True, va='top', ha='left', linespacing=1.6)
    ax.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=120)
    plt.close(fig)
    return buf

def preparar_mision(n_mision):
    pool = [p for p in st.session_state.banco_completo if p['mision'] == n_mision]
    st.session_state.lista_examen = random.sample(pool, min(5, len(pool)))
    st.session_state.n_pregunta = 0
    st.session_state.aciertos = 0
    st.session_state.t_inicio_pregunta = time.time()
    st.session_state.ocultar = []

# --- 5. LÓGICA DE NAVEGACIÓN ---
if 'paso' not in st.session_state:
    st.session_state.update({'paso': 'registro', 'mision': 1, 'n_pregunta': 0, 'aciertos': 0, 'power_5050': True})

if st.session_state.paso == 'registro':
    st.title("🚀 MISIÓN: FUNCIONES")
    st.session_state.nombre = st.text_input("Nombre del Cadete:")
    st.session_state.curso = st.selectbox("Grado:", ["901", "902", "903", "904"])
    if st.button("INICIAR MISIÓN") and st.session_state.nombre:
        preparar_mision(1)
        st.session_state.paso = 'examen'
        st.rerun()

elif st.session_state.paso == 'examen':
    idx = st.session_state.n_pregunta
    pregunta_actual = st.session_state.lista_examen[idx]
    
    st.markdown(f"<div class='status-panel'>Misión: {st.session_state.mision} | Pregunta: {idx+1}/5 | Aciertos: {st.session_state.aciertos}</div>", unsafe_allow_html=True)
    
    t_transcurrido = time.time() - st.session_state.t_inicio_pregunta
    porcentaje = max(0.0, (pregunta_actual['t_max'] - t_transcurrido) / pregunta_actual['t_max'])
    st.progress(porcentaje)

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.session_state.power_5050:
            if st.button("⚡ 50/50"):
                correcta = pregunta_actual['correcta_texto']
                incorrectas = [l for i, l in enumerate(["A","B","C","D"]) if pregunta_actual['opciones'][i] != correcta]
                st.session_state.ocultar = random.sample(incorrectas, 2)
                st.session_state.power_5050 = False
                st.rerun()

    ocultas = st.session_state.get('ocultar', [])
    st.image(crear_imagen(pregunta_actual['pregunta'], pregunta_actual['opciones'], ocultas))
    
    ans = st.radio("TU ELECCIÓN:", ["A", "B", "C", "D"], index=None, horizontal=True, key=f"q_{st.session_state.mision}_{idx}")

    if st.button("ENVIAR RESPUESTA ➡️") or porcentaje <= 0:
        if ans:
            elegida = pregunta_actual['opciones'][["A","B","C","D"].index(ans)]
            if elegida == pregunta_actual['correcta_texto']:
                st.session_state.aciertos += 1
                st.toast("¡Correcto!", icon="🔥")
        
        st.session_state.n_pregunta += 1
        st.session_state.ocultar = []
        st.session_state.t_inicio_pregunta = time.time()

        if st.session_state.n_pregunta >= 5:
            if st.session_state.mision == 1 and st.session_state.aciertos >= 3:
                enviar_a_google(st.session_state.nombre, st.session_state.curso, 1, st.session_state.aciertos)
                st.success("¡MISIÓN 1 COMPLETADA! Preparando Misión 2...")
                time.sleep(2)
                st.session_state.mision = 2
                preparar_mision(2)
            else:
                enviar_a_google(st.session_state.nombre, st.session_state.curso, st.session_state.mision, st.session_state.aciertos)
                st.session_state.paso = 'feedback'
        st.rerun()

    if porcentaje > 0:
        time.sleep(1)
        st.rerun()

elif st.session_state.paso == 'feedback':
    st.title("RESULTADOS")
    st.metric("Aciertos Finales", f"{st.session_state.aciertos}/5")
    if st.button("VOLVER AL INICIO"):
        st.session_state.update({'paso': 'registro', 'mision': 1, 'power_5050': True})
        st.rerun()
