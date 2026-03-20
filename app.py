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

        # --- 3. BANCO DE PREGUNTAS ACTUALIZADO Y HUMANIZADO ---
if 'banco_completo' not in st.session_state:st.session_state.banco_completo = [
        # --- TEMA A: RETOS DE NAVEGACIÓN Y VIDA REAL ---
        {"id": "A1", "mision": 1, "pregunta": "Un dron vuela en línea recta pasando por los puntos A=(-4,8) y B=(4,2). ¿Cuál es su pendiente (m) y su punto de corte (b)?", "opciones": ["m = 5, b = -3/4", "m = 3/4, b = -5", "m = -3/4, b = -5", "m = -3/4, b = 5"], "correcta_texto": "m = -3/4, b = 5", "t_max": 75},
        {"id": "A2", "mision": 1, "pregunta": "Halla la ecuación de la recta que conecta las coordenadas A(1, 3) y B(2, 10) en el mapa del tesoro:", "opciones": ["y = 3/7x + 4", "y = 2/7x - 4", "y = -2/7x - 4", "y = 7x - 4"], "correcta_texto": "y = 7x - 4", "t_max": 75},
        {"id": "A3", "mision": 1, "pregunta": "Un rayo láser sale del punto P(-6, 2) con una inclinación m = -2/3. ¿Cuál es su fórmula matemática?", "opciones": ["y = -2/3x - 2", "y = -2/3x - 3", "y = -3/2x - 3", "y = -3/2x - 2"], "correcta_texto": "y = -2/3x - 2", "t_max": 75},
        {"id": "A4", "mision": 1, "pregunta": "El camino de un barco es y = -4/5x - 3. ¿Cuál de estas rutas es PARALELA a la del barco?", "opciones": ["y = -4/5x + 3", "y = 5/4x + 2", "y = 4/5x + 10", "y = -5/4x - 7"], "correcta_texto": "y = -4/5x + 3", "t_max": 60},
        {"id": "A5", "mision": 1, "pregunta": "Para cruzar un río de forma PERPENDICULAR a la corriente (y = 2/3x + 1), ¿qué trayectoria debes seguir?", "opciones": ["y = 2/3x - 5", "y = 3/2x + 2", "y = -2/3x + 4", "y = -3/2x + 5"], "correcta_texto": "y = -3/2x + 5", "t_max": 60},
        
        {"id": "A7", "mision": 2, "pregunta": "Un horno de cerámica inicia a 15°C y sube su temperatura 10°C cada 3 minutos. ¿Qué función representa este calor?", "opciones": ["y = 15x + 3/10", "y = 3/10x + 15", "y = 15x + 10/3", "y = 10/3x + 15"], "correcta_texto": "y = 10/3x + 15", "t_max": 90},
        {"id": "A8", "mision": 2, "pregunta": "Un taxi cobra $7 de tarifa base y suma $2 por cada 3 km recorridos. ¿Cuánto pagarás por un viaje de 15 km?", "opciones": ["$10", "$23", "$17", "$15"], "correcta_texto": "$17", "t_max": 90},
        {"id": "A9", "mision": 2, "pregunta": "El tanque A sube (2min=10L, 8min=40L). El tanque B baja (1min=50L, 11min=10L). ¿En qué minuto tienen la misma agua?", "opciones": ["4", "6", "8", "10"], "correcta_texto": "6", "t_max": 120},
        {"id": "A10", "mision": 2, "pregunta": "Andrés tiene $150 y ahorra $50/semana. Beatriz tiene $950 y gasta $150/semana. ¿En qué semana tendrán lo mismo?", "opciones": ["2", "3", "4", "5"], "correcta_texto": "4", "t_max": 120},

        # --- TEMA B: DESAFÍOS DE INGENIERÍA Y FINANZAS ---
        {"id": "B1", "mision": 1, "pregunta": "Una rampa de acceso pasa por A=(-3, 5) y B=(3, 1). Calcula su pendiente (m) y su altura inicial (b):", "opciones": ["m = 2/3, b = 3", "m = -2/3, b = 3", "m = -3/2, b = -3", "m = 3/2, b = 3"], "correcta_texto": "m = -2/3, b = 3", "t_max": 75},
        {"id": "B3", "mision": 1, "pregunta": "Una antena se ubica en P(5, -2) con una inclinación m = -4/5. ¿Cuál es la ecuación de su señal?", "opciones": ["y = -4/5x + 2", "y = -4/5x - 6", "y = 4/5x + 2", "y = -5/4x + 2"], "correcta_texto": "y = -4/5x + 2", "t_max": 75},
        {"id": "B5", "mision": 1, "pregunta": "Si una calle tiene la ecuación y = -5/2x - 4, ¿cuál es la ecuación de una calle PERPENDICULAR para un cruce?", "opciones": ["y = 5/2x + 1", "y = 2/5x + 10", "y = -2/5x - 4", "y = -5/2x + 3"], "correcta_texto": "y = 2/5x + 10", "t_max": 60},
        
        {"id": "B7", "mision": 2, "pregunta": "Un enfriador industrial está a 20°C y baja 4°C cada 3 minutos. ¿Qué función modela su temperatura?", "opciones": ["y = 3/4x + 20", "y = -4/3x + 20", "y = 4/3x - 20", "y = -3/4x + 20"], "correcta_texto": "y = -4/3x + 20", "t_max": 90},
        {"id": "B8", "mision": 2, "pregunta": "Una mensajería cobra $10 de base más $3 por cada 4 km. ¿Cuál es el costo total por enviar un paquete a 20 km?", "opciones": ["$15", "$20", "$25", "$30"], "correcta_texto": "$25", "t_max": 90},
        {"id": "B10", "mision": 2, "pregunta": "Camilo tiene $400 y gasta $25 cada 2 semanas. Sara tiene $100 y ahorra $75 cada 2 semanas. ¿En qué semana se igualan?", "opciones": ["4", "6", "8", "10"], "correcta_texto": "6", "t_max": 120},

        # --- TEMA C: LOGÍSTICA Y RECURSOS ---
        {"id": "C7", "mision": 2, "pregunta": "Un vehículo inicia con 40L de gasolina y consume 5L cada 4 km recorridos. ¿Cuál es la función del combustible?", "opciones": ["y = 4/5x + 40", "y = -5/4x + 40", "y = 5/4x - 40", "y = -4/5x + 40"], "correcta_texto": "y = -5/4x + 40", "t_max": 90},
        {"id": "C8", "mision": 2, "pregunta": "Un técnico cobra $15 por la visita y $5 por cada 2 horas de trabajo. ¿Cuánto cobrará por una reparación de 7 horas?", "opciones": ["$30.0", "$32.5", "$35.0", "$17.5"], "correcta_texto": "$32.5", "t_max": 90},
        {"id": "C9", "mision": 2, "pregunta": "Tanque A (100L, pierde 10L c/3 min). Tanque B (20L, gana 10L c/3 min). ¿En qué minuto tendrán el mismo nivel?", "opciones": ["10", "12", "15", "18"], "correcta_texto": "12", "t_max": 120},

        # --- TEMA D: FÍSICA Y CONSTRUCCIÓN ---
        {"id": "D6", "mision": 1, "pregunta": "Un soporte arquitectónico tiene pendiente m = 4/5 y pasa por P(5, 7). ¿En qué punto cortará al eje Y?", "opciones": ["y = 4/5x + 3 (Corta en 3)", "y = -4/5x + 3", "y = 4/5x - 3", "y = 5/4x + 3"], "correcta_texto": "y = 4/5x + 3 (Corta en 3)", "t_max": 75},
        {"id": "D7", "mision": 2, "pregunta": "Un depósito de 80 galones pierde 3 galones cada 2 horas por una fuga. ¿Qué función describe la pérdida?", "opciones": ["y = 3/2x + 80", "y = -2/3x + 80", "y = -3/2x + 80", "y = -3/2x - 80"], "correcta_texto": "-3/2x + 80", "t_max": 90},
        {"id": "D10", "mision": 2, "pregunta": "Daniel tiene $500 y gasta $30 c/2 semanas. Sofía tiene $800 y gasta $80 c/2 semanas. ¿En qué semana tendrán lo mismo?", "opciones": ["6", "10", "12", "14"], "correcta_texto": "12", "t_max": 120}
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
    url_script ="https://script.google.com/macros/s/AKfycbyX5JRshORtaiXVXTXF73nblLEj3M4oX79hF_heKDbEHnuPwfH0PqJBTDXM8_gqYHx4cQ/exec"
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
    
    # El botón DEBE estar alineado con el radio de arriba
    if st.button("ENVIAR RESPUESTA ➡️"):
        if ans:
            # Verificación de acierto
            if ans == st.session_state[f"q_cor_{idx}"]:
                st.session_state.aciertos += 1
                st.toast("¡Punto para ti!", icon="🔥")
            else:
                st.toast("Incorrecto...", icon="❌")
            
            # Avance de pregunta
            st.session_state.n_pregunta += 1
            st.session_state.usar_5050 = False
            st.session_state.t_inicio_pregunta = time.time()

            # --- LÓGICA DE CAMBIO DE MISIÓN ---
            if st.session_state.n_pregunta >= len(st.session_state.lista_examen):
                if st.session_state.mision == 1 and st.session_state.aciertos >= 3:
                    st.success("¡MISIÓN 1 COMPLETADA! Preparando Misión 2...")
                    time.sleep(2)
                    
                    pool_2 = [p for p in st.session_state.banco_completo if p['mision'] == 2]
                    st.session_state.lista_examen = random.sample(pool_2, min(5, len(pool_2)))
                    
                    st.session_state.update({
                        'mision': 2,
                        'n_pregunta': 0,
                        'aciertos': 0, 
                        't_inicio_pregunta': time.time()
                    })
                else:
                    st.session_state.paso = 'feedback'

            st.rerun()

    # --- Control de Tiempo (Auto-refresh) ---
    # Este bloque también debe estar dentro del "elif st.session_state.paso == 'examen':"
    if porcentaje > 0:
        time.sleep(1)
        st.rerun()
    else:
        st.error("¡TIEMPO AGOTADO!")
        time.sleep(1)
        
        st.session_state.n_pregunta += 1
        st.session_state.usar_5050 = False 
        st.session_state.t_inicio_pregunta = time.time()
        
        if st.session_state.n_pregunta >= len(st.session_state.lista_examen):
            if st.session_state.mision == 1 and st.session_state.aciertos >= 3:
                pool_2 = [p for p in st.session_state.banco_completo if p['mision'] == 2]
                st.session_state.lista_examen = random.sample(pool_2, min(5, len(pool_2)))
                st.session_state.update({'mision': 2, 'n_pregunta': 0, 'aciertos': 0})
            else:
                st.session_state.paso = 'feedback'
        
        st.rerun()
        
# --- Control de Tiempo (Auto-refresh) ---
    if porcentaje > 0:
        time.sleep(1)
        st.rerun()
    else:
        # Se acabó el tiempo
        st.error("¡TIEMPO AGOTADO!")
        time.sleep(1)
        
        # Avanzamos a la siguiente pregunta (sin sumar acierto)
        st.session_state.n_pregunta += 1
        st.session_state.usar_5050 = False # Resetear power-up si estaba activo
        st.session_state.t_inicio_pregunta = time.time()
        
        # VERIFICACIÓN IGUAL A LA DEL BOTÓN: ¿Terminó el examen por tiempo?
        if st.session_state.n_pregunta >= len(st.session_state.lista_examen):
            if st.session_state.mision == 1 and st.session_state.aciertos >= 3:
                # Si a pesar de que se le acabó el tiempo en la última, ya tenía 3 aciertos...
                pool_2 = [p for p in st.session_state.banco_completo if p['mision'] == 2]
                st.session_state.lista_examen = random.sample(pool_2, min(5, len(pool_2)))
                st.session_state.update({'mision': 2, 'n_pregunta': 0, 'aciertos': 0})
            else:
                st.session_state.paso = 'feedback'
        
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
