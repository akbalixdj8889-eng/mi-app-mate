import streamlit as st
import random
import time
import requests
import matplotlib.pyplot as plt
import io

# 1. Configuración de la pestaña del navegador y disposición de la página
st.set_page_config(
    page_title="Math Quest Pro", 
    page_icon="⚡", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)
# 2. CSS REFORZADO (ESTILO Y VISIBILIDAD)
st.markdown("""
    <style>
    /* Fondo degradado para toda la app */
    .stApp { 
        background: linear-gradient(135deg, #461a42 0%, #2d0b2a 100%); 
    }
    
    /* Panel de Estado Superior (Nombre, Aciertos, etc.) */
    .status-panel {
        background-color: white; 
        border-radius: 50px; 
        padding: 10px;
        text-align: center; 
        color: #461a42; 
        font-weight: bold;
        font-size: 1.2rem; 
        margin-bottom: 10px;
    }

    /* Contenedor y Barra de Energía (Tiempo) */
    .energy-container { 
        width: 100%; 
        background-color: rgba(255,255,255,0.2); 
        border-radius: 10px; 
        margin-bottom: 20px; 
    }
    .energy-bar { 
        height: 12px; 
        background: #ff4b4b; 
        border-radius: 10px; 
        transition: width 0.1s; 
    }

    /* FORZAR VISIBILIDAD DE OPCIONES A, B, C, D */
    /* Usamos selectores específicos de Streamlit para asegurar el color blanco */
    div[data-testid="stRadio"] label p {
        color: white !important;
        font-size: 1.3rem !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 2px black;
    }
    
    /* Etiquetas generales de texto en Markdown */
    .stMarkdown p { 
        color: white !important; 
        font-weight: bold; 
    }

    /* Tarjeta blanca donde vive la imagen de la pregunta */
    .question-card { 
        background-color: white; 
        padding: 15px; 
        border-radius: 20px; 
        margin-bottom: 10px; 
    }
    
    /* Estilo para los botones generales */
    .stButton>button {
        border-radius: 10px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
# 3. BANCO DE PREGUNTAS (DATOS MAESTROS) ---
# Inicializamos el banco de preguntas en el estado de la sesión si no existe
if 'banco_completo' not in st.session_state:
    st.session_state.banco_completo = [
        # --- TEMA A ---
        {"id": "A1", "mision": 1, "pregunta": "Pasa por A=(-4,8) y B=(4,2). ¿m y b?", "opciones": ["m = 5, b = -3/4", "m = 3/4, b = -5", "m = -3/4, b = -5", "m = -3/4, b = 5"], "correcta_texto": "m = -3/4, b = 5", "t_max": 60},
        {"id": "A2", "mision": 1, "pregunta": "Ecuación por A(1, 3) y B(2, 10):", "opciones": ["y = 3/7x + 4", "y = 2/7x - 4", "y = -2/7x - 4", "y = -2/7x + 4"], "correcta_texto": "y = 2/7x - 4", "t_max": 60},
        {"id": "A3", "mision": 1, "pregunta": "P(-6, 2) con m = -2/3. ¿Fórmula?", "opciones": ["y = -2/3x - 2", "y = -2/3x - 3", "y = -3/2x - 3", "y = -3/2x - 2"], "correcta_texto": "y = -2/3x - 2", "t_max": 60},
        {"id": "A4", "mision": 1, "pregunta": "¿Paralela a y = -4/5x - 3?", "opciones": ["y = -4/5x + 3", "y = 5/4x + 2", "y = 4/5x + 10", "y = -5/4x - 7"], "correcta_texto": "y = -4/5x + 3", "t_max": 45},
        {"id": "A5", "mision": 1, "pregunta": "Perpendicular a y = 2/3x + 1:", "opciones": ["y = 2/3x - 5", "y = 3/2x + 2", "y = -2/3x + 4", "y = -3/2x + 5"], "correcta_texto": "y = -3/2x + 5", "t_max": 45},
        {"id": "A6", "mision": 1, "pregunta": "m = -5/4 por p:(4,2):", "opciones": ["y = -4/5x + 5 (9,-2)", "y = -5/4x + 7 (8,-3)", "y = -5/4x + 7 (8,2)", "y = -4/5x + 5 (0,5)"], "correcta_texto": "y = -5/4x + 7 (8,-3)", "t_max": 60},
        {"id": "A7", "mision": 2, "pregunta": "Horno inicia 15°C y sube 10°C c/3 min. ¿Función?", "opciones": ["y = 15x + 3/10", "y = 3/10x + 15", "y = 15x + 10/3", "y = 10/3x + 15"], "correcta_texto": "y = 10/3x + 15", "t_max": 90},
        {"id": "A8", "mision": 2, "pregunta": "Taxi: $7 base + $2 c/3 km. ¿Costo por 15 km?", "opciones": ["$10", "$23", "$17", "$15"], "correcta_texto": "$17", "t_max": 90},
        {"id": "A9", "mision": 2, "pregunta": "Tanque A (2m=10L, 8m=40L). Tanque B (1m=50L, 11m=10L). ¿Cruce?", "opciones": ["4", "6", "8", "10"], "correcta_texto": "6", "t_max": 120},
        {"id": "A10", "mision": 2, "pregunta": "Andrés $150 (+$50/s). Beatriz $950 (-$150/s). ¿Semana igual?", "opciones": ["2", "3", "4", "5"], "correcta_texto": "4", "t_max": 120},
        
        # --- TEMA B ---
        {"id": "B1", "mision": 1, "pregunta": "Por A=(-3, 5) y B=(3, 1). ¿m y b?", "opciones": ["m = 2/3, b = 3", "m = -2/3, b = 3", "m = -3/2, b = -3", "m = 3/2, b = 3"], "correcta_texto": "m = -2/3, b = 3", "t_max": 60},
        {"id": "B2", "mision": 1, "pregunta": "Ecuación por A(-2, -5) y B(5, -7):", "opciones": ["y = -2/7x - 39/7", "y = 2/7x + 39/7", "y = -7/2x - 4", "y = 7/2x + 4"], "correcta_texto": "y = -2/7x - 39/7", "t_max": 60},
        {"id": "B3", "mision": 1, "pregunta": "P(5, -2) con m = -4/5:", "opciones": ["y = -4/5x + 2", "y = -4/5x - 6", "y = 4/5x + 2", "y = -5/4x + 2"], "correcta_texto": "y = -4/5x + 2", "t_max": 60},
        {"id": "B4", "mision": 1, "pregunta": "¿Paralela a y = 3/7x + 5?", "opciones": ["y = -3/7x + 5", "y = 7/3x - 1", "y = 3/7x - 8", "y = -7/3x + 2"], "correcta_texto": "y = 3/7x - 8", "t_max": 45},
        {"id": "B5", "mision": 1, "pregunta": "Perpendicular a y = -5/2x - 4:", "opciones": ["y = 5/2x + 1", "y = 2/5x + 10", "y = -2/5x - 4", "y = -5/2x + 3"], "correcta_texto": "y = 2/5x + 10", "t_max": 45},
        {"id": "B6", "mision": 1, "pregunta": "m = 1/3 por P(6, 4):", "opciones": ["y = 1/3x + 2 (0, 2)", "y = 3x - 2 (1, 1)", "y = 1/3x + 4 (3, 5)", "y = -1/3x + 2 (6, 0)"], "correcta_texto": "y = 1/3x + 2 (0, 2)", "t_max": 60},
        {"id": "B7", "mision": 2, "pregunta": "Enfriador 20°C baja 4°C c/3 min. ¿Función?", "opciones": ["y = 3/4x + 20", "y = -4/3x + 20", "y = 4/3x - 20", "y = -3/4x + 20"], "correcta_texto": "y = -4/3x + 20", "t_max": 90},
        {"id": "B8", "mision": 2, "pregunta": "Mensajería: $10 base + $3 c/4 km. ¿Costo por 20 km?", "opciones": ["$15", "$20", "$25", "$30"], "correcta_texto": "$25", "t_max": 90},
        {"id": "B9", "mision": 2, "pregunta": "Tanque A 15L (+3/2). Tanque B 45L (-5/2). ¿Cruce?", "opciones": ["6", "7.5", "10", "15"], "correcta_texto": "7.5", "t_max": 120},
        {"id": "B10", "mision": 2, "pregunta": "Camilo $400 (-$25/2s). Sara $100 (+$75/2s). ¿Semana?", "opciones": ["4", "6", "8", "10"], "correcta_texto": "6", "t_max": 120},

        # --- TEMA C ---
        {"id": "C1", "mision": 1, "pregunta": "Por A=(-5, 7) y B=(5, 3). ¿m y b?", "opciones": ["m = 2/5, b = 5", "m = -5/2, b = 5", "m = -2/5, b = 5", "m = 5/2, b = -5"], "correcta_texto": "m = -2/5, b = 5", "t_max": 60},
        {"id": "C2", "mision": 1, "pregunta": "Ecuación por A(-3, 1) y B(6, 7):", "opciones": ["y = 2/3x + 3", "y = -2/3x + 3", "y = 3/2x - 1", "y = 2/3x - 3"], "correcta_texto": "y = 2/3x + 3", "t_max": 60},
        {"id": "C3", "mision": 1, "pregunta": "P(-4, 2) con m = 3/4:", "opciones": ["y = 3/4x - 5", "y = 3/4x + 5", "y = -3/4x + 5", "y = 4/3x + 5"], "correcta_texto": "y = 3/4x + 5", "t_max": 60},
        {"id": "C4", "mision": 1, "pregunta": "¿Paralela a y = -2/9x + 10?", "opciones": ["y = 9/2x + 10", "y = -2/9x - 4", "y = 2/9x + 4", "y = -9/2x + 1"], "correcta_texto": "y = -2/9x - 4", "t_max": 45},
        {"id": "C5", "mision": 1, "pregunta": "Perpendicular a y = 7/3x - 2:", "opciones": ["y = -3/7x + 6", "y = 3/7x + 6", "y = -7/3x - 2", "y = 7/3x + 4"], "correcta_texto": "y = -3/7x + 6", "t_max": 45},
        {"id": "C6", "mision": 1, "pregunta": "m = -3/2 por P(4, -1):", "opciones": ["y = -3/2x + 5 (0, 5)", "y = 3/2x - 7 (2, -4)", "y = -3/2x + 5 (2, 1)", "y = 2/3x + 1 (3, 3)"], "correcta_texto": "y = -3/2x + 5 (0, 5)", "t_max": 60},
        {"id": "C7", "mision": 2, "pregunta": "Vehículo 40L consume 5L c/4 km. ¿Función?", "opciones": ["y = 4/5x + 40", "y = -5/4x + 40", "y = 5/4x - 40", "y = -4/5x + 40"], "correcta_texto": "y = -5/4x + 40", "t_max": 90},
        {"id": "C8", "mision": 2, "pregunta": "Reparación: $15 base + $5 c/2h. ¿Costo por 7 horas?", "opciones": ["$30.0", "$32.5", "$35.0", "$17.5"], "correcta_texto": "$32.5", "t_max": 90},
        {"id": "C9", "mision": 2, "pregunta": "Tanque A 100L (-10/3). Tanque B 20L (+10/3). ¿Cruce?", "opciones": ["10", "12", "15", "18"], "correcta_texto": "12", "t_max": 120},
        {"id": "C10", "mision": 2, "pregunta": "Marta $600 (-$40/3s). Luis $1000 (-$120/3s). ¿Igualdad?", "opciones": ["Semana 12", "Semana 15", "Semana 18", "Semana 20"], "correcta_texto": "Semana 15", "t_max": 120},

        # --- TEMA D ---
        {"id": "D1", "mision": 1, "pregunta": "Por A=(-6, 1) y B=(6, 6). ¿m y b?", "opciones": ["m = 5/12, b = 3.5", "m = -5/12, b = 3.5", "m = 12/5, b = -3", "m = 5/12, b = -3.5"], "correcta_texto": "m = 5/12, b = 3.5", "t_max": 60},
        {"id": "D2", "mision": 1, "pregunta": "Ecuación por A(-4, 8) y B(2, -1):", "opciones": ["y = 3/2x + 2", "y = -3/2x + 2", "y = -2/3x + 2", "y = 3/2x - 2"], "correcta_texto": "y = -3/2x + 2", "t_max": 60},
        {"id": "D3", "mision": 1, "pregunta": "P(3, -4) con m = -1/3:", "opciones": ["y = -1/3x - 3", "y = -1/3x + 3", "y = 1/3x - 3", "y = -3x - 3"], "correcta_texto": "y = -1/3x - 3", "t_max": 60},
        {"id": "D4", "mision": 1, "pregunta": "¿Paralela a y = -5/6x - 1?", "opciones": ["y = 6/5x + 4", "y = 5/6x - 1", "y = -5/6x + 9", "y = -6/5x + 2"], "correcta_texto": "y = -5/6x + 9", "t_max": 45},
        {"id": "D5", "mision": 1, "pregunta": "Perpendicular a y = -1/4x + 5:", "opciones": ["y = -4x + 2", "y = 1/4x - 5", "y = 4x - 8", "y = -4/1x + 3"], "correcta_texto": "y = 4x - 8", "t_max": 45},
        {"id": "D6", "mision": 1, "pregunta": "m = 4/5 por P(5, 7):", "opciones": ["y = 4/5x + 3 (0, 3)", "y = -4/5x + 3 (5, -1)", "y = 4/5x - 3 (10, 5)", "y = 5/4x + 3 (4, 8)"], "correcta_texto": "y = 4/5x + 3 (0, 3)", "t_max": 60},
        {"id": "D7", "mision": 2, "pregunta": "Depósito 80 gal pierde 3 gal c/2h. ¿Función?", "opciones": ["y = 3/2x + 80", "y = -2/3x + 80", "y = -3/2x + 80", "y = -3/2x - 80"], "correcta_texto": "y = -3/2x + 80", "t_max": 90},
        {"id": "D8", "mision": 2, "pregunta": "Carpintero: $20 base + $15 c/4h. ¿Costo 12h?", "opciones": ["$45", "$65", "$35", "$70"], "correcta_texto": "$65", "t_max": 90},
        {"id": "D9", "mision": 2, "pregunta": "Globo A 10m (+5/4). Globo B 40m (-7/4). ¿Segundo?", "opciones": ["8", "10", "12", "15"], "correcta_texto": "10", "t_max": 120},
        {"id": "D10", "mision": 2, "pregunta": "Daniel $500 (-$30/2s). Sofía $800 (-$80/2s). ¿Semana?", "opciones": ["6", "10", "12", "14"], "correcta_texto": "12", "t_max": 120}
    ]

#--- 4. INICIALIZACIÓN DE ESTADO (EL CEREBRO DEL JUEGO) ---
# Inicializamos todas las variables de control si no existen
if 'paso' not in st.session_state:
    st.session_state.update({
        'paso': 'registro',         # Pantalla actual
        'nombre': '',               # Nombre del estudiante
        'mision': 1,                # Misión actual (1 o 2)
        'n_pregunta': 0,            # Índice de la pregunta actual (0 a 4)
        'aciertos': 0,              # Contador de puntos
        'power_5050': True,         # Disponibilidad del Power-up
        'usar_5050': False,         # Estado de activación del Power-up en la pregunta actual
        'lista_examen': [],         # Las 5 preguntas seleccionadas para el intento
        't_inicio_pregunta': 0,     # Momento exacto en que inicia la pregunta
        'examen_finalizado': False  # Control de fin de juego
    })
    #5. FUNCIONES DE APOYO (MOTOR GRÁFICO Y LÓGICA) ---


def enviar_a_google(nombre, curso, mision, aciertos, powerup):
    url_script = 
    "https://script.google.com/macros/s/AKfycbyX5JRshORtaiXVXTXF73nblLEj3M4oX79hF_heKDbEHnuPwfH0PqJBTDXM8_gqYHx4cQ/exec"
    datos = {
        "nombre": nombre,
        "curso": curso,
        "mision": mision,
        "aciertos": aciertos,
        "powerup": "Sí" if not powerup else "No" # Si power_5050 es False, es porque lo usó
    }
    try:
        requests.post(url_script, json=datos)
    except:
        pass # Para que el juego no se trabe si falla el internet


def crear_imagen(texto, opciones, ocultas=[]):
    """
    Genera una imagen blanca con el texto de la pregunta y sus opciones.
    'ocultas' contiene las letras (A, B, C o D) que el 50/50 debe tachar.
    """
    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor('white')
    
    texto_final = []
    for opt in opciones:
        # Verificamos si la primera letra de la opción (ej. 'A') está en la lista de ocultas
        if opt[0] in ocultas:
            texto_final.append(f"{opt[0]} [ ELIMINADA ]")
        else:
            texto_final.append(opt)
            
    # Unimos la pregunta con las opciones procesadas
    cuerpo = f"{texto}\n\n" + "\n".join(texto_final)
    
    # Dibujamos el texto en el canvas
    ax.text(0.05, 0.5, cuerpo, 
            fontsize=15, 
            fontweight='bold', 
            wrap=True, 
            va='center', 
            color='#2d0b2a', 
            family='sans-serif')
    
    ax.axis('off') # Ocultamos los ejes del gráfico
    
    # Guardamos el resultado en un buffer de memoria para Streamlit
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    plt.close(fig)
    return buf

def reset_juego():
    """Limpia el estado para permitir un nuevo intento"""
    st.session_state.update({
        'paso': 'registro',
        'n_pregunta': 0,
        'aciertos': 0,
        'power_5050': True,
        'usar_5050': False,
        'lista_examen': [],
        'examen_finalizado': False
    })
    #6. PANTALLAS (FLUJO DE JUEGO) ---
# --- PANTALLA 1: REGISTRO ---
if st.session_state.paso == 'registro':
    st.markdown("<div class='status-panel'>MATH QUEST: REGISTRO DE GUERRERO</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='question-card'>", unsafe_allow_html=True)
        nom = st.text_input("Nombre del Guerrero:")
        cur = st.selectbox("Misión del Curso:", ["908", "909", "910"])
        
        if st.button("¡INICIAR AVENTURA!"):
            if nom:
                # Seleccionamos 5 preguntas aleatorias de la Misión 1
                pool = [p for p in st.session_state.banco_completo if p['mision'] == 1]
                st.session_state.lista_examen = random.sample(pool, min(5, len(pool)))
                
                # Seteamos el estado para empezar
                st.session_state.update({
                    'nombre': nom, 
                    'curso': cur, 
                    'paso': 'examen', 
                    'n_pregunta': 0,
                    'aciertos': 0,
                    't_inicio_pregunta': time.time()
                })
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- PANTALLA 2: EXAMEN ---
elif st.session_state.paso == 'examen':
    idx = st.session_state.n_pregunta
    
    # Verificar si ya terminamos todas las preguntas
    if idx >= len(st.session_state.lista_examen):
        st.session_state.paso = 'feedback'
        st.rerun()
        
    p = st.session_state.lista_examen[idx]
    
    # 1. ANCLAJE DE OPCIONES (Para que no cambien al refrescar)
    if f"q_opts_{idx}" not in st.session_state:
        opts_mezcladas = p['opciones'].copy()
        random.shuffle(opts_mezcladas)
        letras = ["A)", "B)", "C)", "D)"]
        st.session_state[f"q_opts_{idx}"] = [f"{letras[i]} {opts_mezcladas[i]}" for i in range(4)]
        st.session_state[f"q_cor_{idx}"] = ["A", "B", "C", "D"][opts_mezcladas.index(p['correcta_texto'])]
        # Guardar cuáles son las letras incorrectas para el 50/50
        cor_letra = st.session_state[f"q_cor_{idx}"]
        st.session_state[f"inc_{idx}"] = [L for L in ["A", "B", "C", "D"] if L != cor_letra]

    # UI: Panel de Estado y Barra de Energía
    msg = "⚡ 50/50 DISPONIBLE" if st.session_state.power_5050 else "¡SIN POWER-UPS!"
    if st.session_state.usar_5050: msg = "🔥 MODO 50/50 ACTIVADO"
    st.markdown(f"<div class='status-panel'>{msg}</div>", unsafe_allow_html=True)

    t_limite = p.get('t_max', 60)
    t_actual = time.time() - st.session_state.t_inicio_pregunta
    porcentaje = max(0, 100 - (t_actual / t_limite * 100))
    st.markdown(f"<div class='energy-container'><div class='energy-bar' style='width:{porcentaje}%'></div></div>", unsafe_allow_html=True)

    # 2. LÓGICA 50/50 FIJA
    ocultas = []
    if st.session_state.usar_5050:
        if f"ocultas_fix_{idx}" not in st.session_state:
            st.session_state[f"ocultas_fix_{idx}"] = random.sample(st.session_state[f"inc_{idx}"], 2)
        ocultas = st.session_state[f"ocultas_fix_{idx}"]
    
    # Render de la pregunta
    img_buf = crear_imagen(p['pregunta'], st.session_state[f"q_opts_{idx}"], ocultas)
    st.markdown("<div class='question-card'>", unsafe_allow_html=True)
    st.image(img_buf)
    st.markdown("</div>", unsafe_allow_html=True)

    # Botón de Power-up
    col_a, col_b = st.columns([3,1])
    with col_b:
        if st.session_state.power_5050:
            if st.button("⚡ 50/50"):
                st.session_state.usar_5050 = True
                st.session_state.power_5050 = False
                st.rerun()

    # Selección de respuesta
    ans = st.radio("TU ELECCIÓN:", ["A", "B", "C", "D"], key=f"r_{idx}", index=None, horizontal=True)
    
    if st.button("ENVIAR RESPUESTA ➡️"):
        if ans:
            if ans == st.session_state[f"q_cor_{idx}"]:
                st.session_state.aciertos += 1
                st.toast("¡Punto para ti!", icon="🔥")
            else:
                st.toast("Incorrecto...", icon="❌")
            
            st.session_state.n_pregunta += 1
            st.session_state.usar_5050 = False # Reset para la siguiente pregunta
            st.session_state.t_inicio_pregunta = time.time()
            st.rerun()

    # Control de Tiempo (Auto-refresh)
    if porcentaje > 0:
        time.sleep(1)
        st.rerun()
    else:
        st.error("¡TIEMPO AGOTADO!")
        time.sleep(1)
        st.session_state.n_pregunta += 1
        st.session_state.t_inicio_pregunta = time.time()
        st.rerun()


# --- PANTALLA 3: FEEDBACK ---
elif st.session_state.paso == 'feedback':
    # ENVIAR DATOS SOLO UNA VEZ
    if not st.session_state.get('datos_enviados', False):
        enviar_a_google(
            st.session_state.nombre, 
            st.session_state.curso, 
            st.session_state.mision, 
            st.session_state.aciertos,
            st.session_state.power_5050
        )
        st.session_state.datos_enviados = True # Evita duplicados al refrescar

    st.markdown(f"<div class='status-panel'>RESUMEN: {st.session_state.nombre}</div>", unsafe_allow_html=True)
   
# ... (resto de tu código de feedback)

elif st.session_state.paso == 'feedback':
    st.markdown(f"<div class='status-panel'>RESUMEN: {st.session_state.nombre}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='question-card' style='text-align:center;'>", unsafe_allow_html=True)
    st.markdown(f"### Has completado la Misión")
    st.markdown(f"## Puntaje Final: **{st.session_state.aciertos} / 5**")
    
    if st.button("INTENTAR DE NUEVO"):
        reset_juego() # Función que creamos en la sección 5
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
