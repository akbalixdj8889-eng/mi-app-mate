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
    st.session_state.banco_completo = [
        {"id": "A1", "mision": 1, "pregunta": "Pasa por A=(-4,8) y B=(4,2). ¿m y b?", "opciones": ["m = -3/4, b = 5", "m = 5, b = -3/4", "m = 3/4, b = -5", "m = -3/4, b = -5"], "correcta_texto": "m = -3/4, b = 5", "t_max": 60},
        # Agrega aquí las demás preguntas siguiendo este formato
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
