import streamlit as st
import random
import time
import requests
import matplotlib.pyplot as plt
import io

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Math Quest Pro", page_icon="⚡", layout="centered")

# --- 2. CSS REFORZADO (LETRAS BLANCAS Y VISIBLES) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #461a42 0%, #2d0b2a 100%); }
    
    /* Panel de Estado Superior */
    .status-panel {
        background-color: white; border-radius: 50px; padding: 10px;
        text-align: center; color: #461a42; font-weight: bold;
        font-size: 1.2rem; margin-bottom: 10px;
    }

    /* Barra de Energía */
    .energy-container { width: 100%; background-color: rgba(255,255,255,0.2); border-radius: 10px; margin-bottom: 20px; }
    .energy-bar { height: 12px; background: #ff4b4b; border-radius: 10px; transition: width 0.1s; }

    /* FORZAR VISIBILIDAD DE OPCIONES A, B, C, D */
    div[data-testid="stRadio"] label p {
        color: white !important;
        font-size: 1.3rem !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 2px black;
    }
    
    /* Texto "SELECCIONA:" */
    .stMarkdown p { color: white !important; font-weight: bold; }

    .question-card { background-color: white; padding: 15px; border-radius: 20px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BANCO DE PREGUNTAS (Asegúrate de tener todas aquí) ---
if 'banco_completo' not in st.session_state:
    st.session_state.banco_completo = 
    
    # --- 5. BANCO DE PREGUNTAS (Simplificado para ejemplo) ---
BANCO_PREGUNTAS = [
    # TEMA A
    {"id": "A1", "mision": 1, "pregunta": "Pasa por A=(-4,8) y B=(4,2). ¿m y b?", "opciones": ["m = 5, b = -3/4", "m = 3/4, b = -5", "m = -3/4, b = -5", "m = -3/4, b = 5"], "correcta_texto": "m = -3/4, b = 5"},
    {"id": "A2", "mision": 1, "pregunta": "Ecuación por A(1, 3) y B(2, 10):", "opciones": ["y = 3/7x + 4", "y = 2/7x - 4", "y = -2/7x - 4", "y = -2/7x + 4"], "correcta_texto": "y = 2/7x - 4"},
    {"id": "A3", "mision": 1, "pregunta": "P(-6, 2) con m = -2/3. ¿Fórmula?", "opciones": ["y = -2/3x - 2", "y = -2/3x - 3", "y = -3/2x - 3", "y = -3/2x - 2"], "correcta_texto": "y = -2/3x - 2"},
    {"id": "A4", "mision": 1, "pregunta": "¿Paralela a y = -4/5x - 3?", "opciones": ["y = -4/5x + 3", "y = 5/4x + 2", "y = 4/5x + 10", "y = -5/4x - 7"], "correcta_texto": "y = -4/5x + 3"},
    {"id": "A5", "mision": 1, "pregunta": "Perpendicular a y = 2/3x + 1:", "opciones": ["y = 2/3x - 5", "y = 3/2x + 2", "y = -2/3x + 4", "y = -3/2x + 5"], "correcta_texto": "y = -3/2x + 5"},
    {"id": "A6", "mision": 1, "pregunta": "m = -5/4 por p:(4,2):", "opciones": ["y = -4/5x + 5 (9,-2)", "y = -5/4x + 7 (8,-3)", "y = -5/4x + 7 (8,2)", "y = -4/5x + 5 (0,5)"], "correcta_texto": "y = -5/4x + 7 (8,-3)"},
    {"id": "A7", "mision": 2, "pregunta": "Horno inicia 15°C y sube 10°C c/3 min. ¿Función?", "opciones": ["y = 15x + 3/10", "y = 3/10x + 15", "y = 15x + 10/3", "y = 10/3x + 15"], "correcta_texto": "y = 10/3x + 15"},
    {"id": "A8", "mision": 2, "pregunta": "Taxi: $7 base + $2 c/3 km. ¿Costo por 15 km?", "opciones": ["$10", "$23", "$17", "$15"], "correcta_texto": "$17"},
    {"id": "A9", "mision": 2, "pregunta": "Tanque A (2m=10L, 8m=40L). Tanque B (1m=50L, 11m=10L). ¿Cruce?", "opciones": ["4", "6", "8", "10"], "correcta_texto": "6"},
    {"id": "A10", "mision": 2, "pregunta": "Andrés $150 (+$50/s). Beatriz $950 (-$150/s). ¿Semana igual?", "opciones": ["2", "3", "4", "5"], "correcta_texto": "4"},
    
    # TEMA B
    {"id": "B1", "mision": 1, "pregunta": "Por A=(-3, 5) y B=(3, 1). ¿m y b?", "opciones": ["m = 2/3, b = 3", "m = -2/3, b = 3", "m = -3/2, b = -3", "m = 3/2, b = 3"], "correcta_texto": "m = -2/3, b = 3"},
    {"id": "B2", "mision": 1, "pregunta": "Ecuación por A(-2, -5) y B(5, -7):", "opciones": ["y = -2/7x - 39/7", "y = 2/7x + 39/7", "y = -7/2x - 4", "y = 7/2x + 4"], "correcta_texto": "y = -2/7x - 39/7"},
    {"id": "B3", "mision": 1, "pregunta": "P(5, -2) con m = -4/5:", "opciones": ["y = -4/5x + 2", "y = -4/5x - 6", "y = 4/5x + 2", "y = -5/4x + 2"], "correcta_texto": "y = -4/5x + 2"},
    {"id": "B4", "mision": 1, "pregunta": "¿Paralela a y = 3/7x + 5?", "opciones": ["y = -3/7x + 5", "y = 7/3x - 1", "y = 3/7x - 8", "y = -7/3x + 2"], "correcta_texto": "y = 3/7x - 8"},
    {"id": "B5", "mision": 1, "pregunta": "Perpendicular a y = -5/2x - 4:", "opciones": ["y = 5/2x + 1", "y = 2/5x + 10", "y = -2/5x - 4", "y = -5/2x + 3"], "correcta_texto": "y = 2/5x + 10"},
    {"id": "B6", "mision": 1, "pregunta": "m = 1/3 por P(6, 4):", "opciones": ["y = 1/3x + 2 (0, 2)", "y = 3x - 2 (1, 1)", "y = 1/3x + 4 (3, 5)", "y = -1/3x + 2 (6, 0)"], "correcta_texto": "y = 1/3x + 2 (0, 2)"},
    {"id": "B7", "mision": 2, "pregunta": "Enfriador 20°C baja 4°C c/3 min. ¿Función?", "opciones": ["y = 3/4x + 20", "y = -4/3x + 20", "y = 4/3x - 20", "y = -3/4x + 20"], "correcta_texto": "y = -4/3x + 20"},
    {"id": "B8", "mision": 2, "pregunta": "Mensajería: $10 base + $3 c/4 km. ¿Costo por 20 km?", "opciones": ["$15", "$20", "$25", "$30"], "correcta_texto": "$25"},
    {"id": "B9", "mision": 2, "pregunta": "Tanque A 15L (+3/2). Tanque B 45L (-5/2). ¿Cruce?", "opciones": ["6", "7.5", "10", "15"], "correcta_texto": "7.5"},
    {"id": "B10", "mision": 2, "pregunta": "Camilo $400 (-$25/2s). Sara $100 (+$75/2s). ¿Semana?", "opciones": ["4", "6", "8", "10"], "correcta_texto": "6"},

    # TEMA C
    {"id": "C1", "mision": 1, "pregunta": "Por A=(-5, 7) y B=(5, 3). ¿m y b?", "opciones": ["m = 2/5, b = 5", "m = -5/2, b = 5", "m = -2/5, b = 5", "m = 5/2, b = -5"], "correcta_texto": "m = -2/5, b = 5"},
    {"id": "C2", "mision": 1, "pregunta": "Ecuación por A(-3, 1) y B(6, 7):", "opciones": ["y = 2/3x + 3", "y = -2/3x + 3", "y = 3/2x - 1", "y = 2/3x - 3"], "correcta_texto": "y = 2/3x + 3"},
    {"id": "C3", "mision": 1, "pregunta": "P(-4, 2) con m = 3/4:", "opciones": ["y = 3/4x - 5", "y = 3/4x + 5", "y = -3/4x + 5", "y = 4/3x + 5"], "correcta_texto": "y = 3/4x + 5"},
    {"id": "C4", "mision": 1, "pregunta": "¿Paralela a y = -2/9x + 10?", "opciones": ["y = 9/2x + 10", "y = -2/9x - 4", "y = 2/9x + 4", "y = -9/2x + 1"], "correcta_texto": "y = -2/9x - 4"},
    {"id": "C5", "mision": 1, "pregunta": "Perpendicular a y = 7/3x - 2:", "opciones": ["y = -3/7x + 6", "y = 3/7x + 6", "y = -7/3x - 2", "y = 7/3x + 4"], "correcta_texto": "y = -3/7x + 6"},
    {"id": "C6", "mision": 1, "pregunta": "m = -3/2 por P(4, -1):", "opciones": ["y = -3/2x + 5 (0, 5)", "y = 3/2x - 7 (2, -4)", "y = -3/2x + 5 (2, 1)", "y = 2/3x + 1 (3, 3)"], "correcta_texto": "y = -3/2x + 5 (0, 5)"},
    {"id": "C7", "mision": 2, "pregunta": "Vehículo 40L consume 5L c/4 km. ¿Función?", "opciones": ["y = 4/5x + 40", "y = -5/4x + 40", "y = 5/4x - 40", "y = -4/5x + 40"], "correcta_texto": "y = -5/4x + 40"},
    {"id": "C8", "mision": 2, "pregunta": "Reparación: $15 base + $5 c/2h. ¿Costo por 7 horas?", "opciones": ["$30.0", "$32.5", "$35.0", "$17.5"], "correcta_texto": "$32.5"},
    {"id": "C9", "mision": 2, "pregunta": "Tanque A 100L (-10/3). Tanque B 20L (+10/3). ¿Cruce?", "opciones": ["10", "12", "15", "18"], "correcta_texto": "12"},
    {"id": "C10", "mision": 2, "pregunta": "Marta $600 (-$40/3s). Luis $1000 (-$120/3s). ¿Igualdad?", "opciones": ["Semana 12", "Semana 15", "Semana 18", "Semana 20"], "correcta_texto": "Semana 15"},

    # TEMA D
    {"id": "D1", "mision": 1, "pregunta": "Por A=(-6, 1) y B=(6, 6). ¿m y b?", "opciones": ["m = 5/12, b = 3.5", "m = -5/12, b = 3.5", "m = 12/5, b = -3", "m = 5/12, b = -3.5"], "correcta_texto": "m = 5/12, b = 3.5"},
    {"id": "D2", "mision": 1, "pregunta": "Ecuación por A(-4, 8) y B(2, -1):", "opciones": ["y = 3/2x + 2", "y = -3/2x + 2", "y = -2/3x + 2", "y = 3/2x - 2"], "correcta_texto": "y = -3/2x + 2"},
    {"id": "D3", "mision": 1, "pregunta": "P(3, -4) con m = -1/3:", "opciones": ["y = -1/3x - 3", "y = -1/3x + 3", "y = 1/3x - 3", "y = -3x - 3"], "correcta_texto": "y = -1/3x - 3"},
    {"id": "D4", "mision": 1, "pregunta": "¿Paralela a y = -5/6x - 1?", "opciones": ["y = 6/5x + 4", "y = 5/6x - 1", "y = -5/6x + 9", "y = -6/5x + 2"], "correcta_texto": "y = -5/6x + 9"},
    {"id": "D5", "mision": 1, "pregunta": "Perpendicular a y = -1/4x + 5:", "opciones": ["y = -4x + 2", "y = 1/4x - 5", "y = 4x - 8", "y = -4/1x + 3"], "correcta_texto": "y = 4x - 8"},
    {"id": "D6", "mision": 1, "pregunta": "m = 4/5 por P(5, 7):", "opciones": ["y = 4/5x + 3 (0, 3)", "y = -4/5x + 3 (5, -1)", "y = 4/5x - 3 (10, 5)", "y = 5/4x + 3 (4, 8)"], "correcta_texto": "y = 4/5x + 3 (0, 3)"},
    {"id": "D7", "mision": 2, "pregunta": "Depósito 80 gal pierde 3 gal c/2h. ¿Función?", "opciones": ["y = 3/2x + 80", "y = -2/3x + 80", "y = -3/2x + 80", "y = -3/2x - 80"], "correcta_texto": "y = -3/2x + 80"},
    {"id": "D8", "mision": 2, "pregunta": "Carpintero: $20 base + $15 c/4h. ¿Costo 12h?", "opciones": ["$45", "$65", "$35", "$70"], "correcta_texto": "$65"},
    {"id": "D9", "mision": 2, "pregunta": "Globo A 10m (+5/4). Globo B 40m (-7/4). ¿Segundo?", "opciones": ["8", "10", "12", "15"], "correcta_texto": "10"},
    {"id": "D10", "mision": 2, "pregunta": "Daniel $500 (-$30/2s). Sofía $800 (-$80/2s). ¿Semana?", "opciones": ["6", "10", "12", "14"], "correcta_texto": "12"}
]

# --- 4. INICIALIZACIÓN DE ESTADO (EVITA EL CAMBIO ALEATORIO) ---
if 'paso' not in st.session_state:
    st.session_state.update({
        'paso': 'registro', 'mision': 1, 'n_pregunta': 0, 'aciertos': 0,
        'power_5050': True, 'usar_5050': False, 'lista_examen': [], 'cache_img': None
    })

# --- 5. FUNCIONES ---
def crear_imagen(texto, opciones, ocultas=[]):
    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor('white')
    finales = []
    for opt in opciones:
        # Si la letra (A, B, C o D) está en ocultas, tachamos el texto
        if opt[0] in ocultas: finales.append(f"{opt[0]} [ ELIMINADA ]")
        else: finales.append(opt)
            
    cuerpo = f"{texto}\n\n" + "\n".join(finales)
    ax.text(0.05, 0.5, cuerpo, fontsize=14, fontweight='bold', wrap=True, va='center', color='#2d0b2a')
    ax.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    return buf

# --- 6. PANTALLAS ---

# REGISTRO
if st.session_state.paso == 'registro':
    st.markdown("<div class='status-panel'>MATH QUEST: REGISTRO DE GUERRERO</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='question-card'>", unsafe_allow_html=True)
        nom = st.text_input("Nombre:")
        cur = st.selectbox("Curso:", ["908", "909", "910"])
        if st.button("¡EMPEZAR!"):
            if nom:
                # CONGELAMOS LAS PREGUNTAS AQUÍ (Solo una vez)
                pool = [p for p in st.session_state.banco_completo if p['mision'] == 1]
                st.session_state.lista_examen = random.sample(pool, min(5, len(pool)))
                st.session_state.update({'nombre': nom, 'curso': cur, 'paso': 'examen', 't_inicio_pregunta': time.time()})
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# EXAMEN
elif st.session_state.paso == 'examen':
    idx = st.session_state.n_pregunta
    p = st.session_state.lista_examen[idx]
    
    # Manejo de opciones y correcta (se guarda en session_state para que no cambie al refrescar)
    if f"q_opts_{idx}" not in st.session_state:
        opts_mezcladas = p['opciones'].copy()
        random.shuffle(opts_mezcladas)
        letras = ["A)", "B)", "C)", "D)"]
        st.session_state[f"q_opts_{idx}"] = [f"{letras[i]} {opts_mezcladas[i]}" for i in range(4)]
        st.session_state[f"q_cor_{idx}"] = ["A", "B", "C", "D"][opts_mezcladas.index(p['correcta_texto'])]

    # UI SUPERIOR
    msg = "⚡ 50/50 DISPONIBLE" if st.session_state.power_5050 else "¡SIN POWER-UPS!"
    st.markdown(f"<div class='status-panel'>{msg}</div>", unsafe_allow_html=True)

    # BARRA DE TIEMPO
    t_limite = p.get('t_max', 60)
    t_actual = time.time() - st.session_state.t_inicio_pregunta
    porcentaje = max(0, 100 - (t_actual / t_limite * 100))
    st.markdown(f"<div class='energy-container'><div class='energy-bar' style='width:{porcentaje}%'></div></div>", unsafe_allow_html=True)

    # GENERAR IMAGEN (Con lógica 50/50)
    ocultas = []
    if st.session_state.usar_5050:
        cor = st.session_state[f"q_cor_{idx}"]
        incorrectas = [L for L in ["A", "B", "C", "D"] if L != cor]
        ocultas = random.sample(incorrectas, 2)
    
    img_buf = crear_imagen(p['pregunta'], st.session_state[f"q_opts_{idx}"], ocultas)

    st.markdown("<div class='question-card'>", unsafe_allow_html=True)
    st.image(img_buf)
    st.markdown("</div>", unsafe_allow_html=True)

    # BOTÓN 50/50
    col_a, col_b = st.columns([3,1])
    with col_b:
        if st.session_state.power_5050:
            if st.button("⚡ 50/50"):
                st.session_state.usar_5050 = True
                st.session_state.power_5050 = False
                st.rerun()

    # RESPUESTA
    ans = st.radio("SELECCIONA:", ["A", "B", "C", "D"], key=f"r_{idx}", index=None, horizontal=True)
    
    if st.button("ENVIAR ➡️"):
        if ans:
            if ans == st.session_state[f"q_cor_{idx}"]:
                st.session_state.aciertos += 1
                st.toast("¡Punto para ti!", icon="🔥")
            else:
                st.toast("Casi...", icon="❌")
            
            st.session_state.n_pregunta += 1
            st.session_state.usar_5050 = False
            st.session_state.t_inicio_pregunta = time.time()
            if st.session_state.n_pregunta >= len(st.session_state.lista_examen):
                st.session_state.paso = 'feedback'
            st.rerun()

    # Auto-refresh cada 1 segundo para la barra
    if porcentaje > 0:
        time.sleep(1)
        st.rerun()
    else:
        st.error("TIEMPO AGOTADO")
        time.sleep(1)
        st.session_state.n_pregunta += 1
        st.session_state.t_inicio_pregunta = time.time()
        st.rerun()











































