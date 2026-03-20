import streamlit as st
import random
import time
import matplotlib.pyplot as plt
import io

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Math Quest Pro", page_icon="⚡", layout="centered")

# --- 2. CSS ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #461a42 0%, #2d0b2a 100%); }
    .status-panel {
        background-color: white; border-radius: 50px; padding: 10px;
        text-align: center; color: #461a42; font-weight: bold; font-size: 1.2rem;
    }
    .energy-container { width: 100%; background-color: rgba(255,255,255,0.2); border-radius: 10px; margin: 10px 0; }
    .energy-bar { height: 12px; background: #ff4b4b; border-radius: 10px; transition: width 0.1s; }
    div[data-testid="stRadio"] label p { color: white !important; font-size: 1.3rem !important; font-weight: bold !important; }
    .stMarkdown p { color: white !important; }
    .question-card { background-color: white; padding: 15px; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INICIALIZACIÓN ---
if 'paso' not in st.session_state:
    banco = [
        {"id": "A1", "mision": 1, "pregunta": "Pasa por A=(-4,8) y B=(4,2). ¿m y b?", "opciones": ["m = -3/4, b = 5", "m = 5, b = -3/4", "m = 3/4, b = -5", "m = -3/4, b = -5"], "correcta_texto": "m = -3/4, b = 5", "t_max": 60},
        # Añade aquí tus otras preguntas
    ]
    st.session_state.update({
        'paso': 'registro', 'n_pregunta': 0, 'aciertos': 0,
        'power_5050': True, 'usar_5050': False, 'banco_total': banco, 
        'lista_examen': [], 't_inicio_pregunta': 0
    })

# --- 4. FUNCIONES ---
def crear_imagen(texto, opciones, ocultas=[]):
    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor('white')
    finales = []
    for opt in opciones:
        if opt[0] in ocultas: finales.append(f"{opt[0]} [ ELIMINADA ]")
        else: finales.append(opt)
    cuerpo = f"{texto}\n\n" + "\n".join(finales)
    ax.text(0.05, 0.5, cuerpo, fontsize=14, fontweight='bold', wrap=True, va='center', color='#2d0b2a')
    ax.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    return buf

# --- 5. PANTALLAS ---

# PANTALLA A: REGISTRO
if st.session_state.paso == 'registro':
    st.markdown("<div class='status-panel'>MATH QUEST: REGISTRO</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='question-card'>", unsafe_allow_html=True)
        nom = st.text_input("Nombre:")
        if st.button("¡EMPEZAR!"):
            if nom:
                # Seleccionar preguntas una sola vez
                pool = st.session_state.banco_total
                st.session_state.lista_examen = random.sample(pool, min(5, len(pool)))
                st.session_state.update({'nombre': nom, 'paso': 'examen', 'n_pregunta': 0, 'aciertos': 0, 't_inicio_pregunta': time.time()})
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# PANTALLA B: EXAMEN (UNIFICADO)
elif st.session_state.paso == 'examen':
    idx = st.session_state.n_pregunta
    
    # Verificar si terminamos
    if idx >= len(st.session_state.lista_examen):
        st.session_state.paso = 'feedback'
        st.rerun()

    p = st.session_state.lista_examen[idx]
    
    # Inicializar datos fijos de esta pregunta específica
    if f"q_opts_{idx}" not in st.session_state:
        opts = p['opciones'].copy()
        random.shuffle(opts)
        letras = ["A)", "B)", "C)", "D)"]
        st.session_state[f"q_opts_{idx}"] = [f"{letras[i]} {opts[i]}" for i in range(4)]
        st.session_state[f"q_cor_{idx}"] = ["A", "B", "C", "D"][opts.index(p['correcta_texto'])]
        st.session_state[f"inc_{idx}"] = [L for L in ["A", "B", "C", "D"] if L != st.session_state[f"q_cor_{idx}"]]

    # UI
    msg = "⚡ 50/50 DISPONIBLE" if st.session_state.power_5050 else "¡CONCÉNTRATE!"
    if st.session_state.usar_5050: msg = "🔥 MODO 50/50 ACTIVADO"
    st.markdown(f"<div class='status-panel'>{msg}</div>", unsafe_allow_html=True)

    # Tiempo
    t_limite = p.get('t_max', 60)
    t_actual = time.time() - st.session_state.t_inicio_pregunta
    porcentaje = max(0, 100 - (t_actual / t_limite * 100))
    st.markdown(f"<div class='energy-container'><div class='energy-bar' style='width:{porcentaje}%'></div></div>", unsafe_allow_html=True)

    # Lógica 50/50 estática
    ocultas = []
    if st.session_state.usar_5050:
        if f"ocultas_fix_{idx}" not in st.session_state:
            st.session_state[f"ocultas_fix_{idx}"] = random.sample(st.session_state[f"inc_{idx}"], 2)
        ocultas = st.session_state[f"ocultas_fix_{idx}"]

    # Imagen
    img = crear_imagen(p['pregunta'], st.session_state[f"q_opts_{idx}"], ocultas)
    st.markdown("<div class='question-card'>", unsafe_allow_html=True)
    st.image(img)
    st.markdown("</div>", unsafe_allow_html=True)

    # Botones
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.session_state.power_5050:
            if st.button("⚡ 50/50"):
                st.session_state.usar_5050 = True
                st.session_state.power_5050 = False
                st.rerun()

    ans = st.radio("SELECCIONA:", ["A", "B", "C", "D"], key=f"r_{idx}", index=None, horizontal=True)
    
    if st.button("ENVIAR ➡️"):
        if ans:
            if ans == st.session_state[f"q_cor_{idx}"]:
                st.session_state.aciertos += 1
                st.toast("¡Correcto!", icon="✅")
            else:
                st.toast("Incorrecto", icon="❌")
            
            st.session_state.n_pregunta += 1
            st.session_state.usar_5050 = False
            st.session_state.t_inicio_pregunta = time.time()
            st.rerun()

    # Auto-refresh
    if porcentaje > 0:
        time.sleep(1)
        st.rerun()
    else:
        st.session_state.n_pregunta += 1
        st.session_state.t_inicio_pregunta = time.time()
        st.rerun()

# PANTALLA C: FEEDBACK
elif st.session_state.paso == 'feedback':
    st.markdown(f"<div class='status-panel'>¡Misión Terminada, {st.session_state.nombre}!</div>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center; color: white;'>Puntaje: {st.session_state.aciertos}/5</h2>", unsafe_allow_html=True)
    if st.button("INTENTAR DE NUEVO"):
        st.session_state.update({'paso': 'registro', 'power_5050': True, 'usar_5050': False})
        st.rerun()







