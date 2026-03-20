import streamlit as st
import random
import time
import requests
import matplotlib.pyplot as plt
import io

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Math Quest Pro", page_icon="⚡", layout="centered")

# --- 2. CSS (TEXTO BLANCO Y BOTONES) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #461a42 0%, #2d0b2a 100%); }
    .status-panel {
        background-color: white; border-radius: 50px; padding: 10px;
        text-align: center; color: #461a42; font-weight: bold; font-size: 1.2rem;
    }
    .energy-container { width: 100%; background-color: rgba(255,255,255,0.2); border-radius: 10px; margin: 10px 0; }
    .energy-bar { height: 12px; background: #ff4b4b; border-radius: 10px; transition: width 0.1s; }
    
    /* Letras A, B, C, D en Blanco */
    div[data-testid="stRadio"] label p { color: white !important; font-size: 1.3rem !important; font-weight: bold !important; }
    .stMarkdown p { color: white !important; }
    .question-card { background-color: white; padding: 15px; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INICIALIZACIÓN (EL ANCLA DEL JUEGO) ---
if 'juego_iniciado' not in st.session_state:
    # BANCO DE PREGUNTAS (Asegúrate de poner las 40 aquí)
    banco = [
        {"id": "A1", "mision": 1, "pregunta": "Pasa por A=(-4,8) y B=(4,2). ¿m y b?", "opciones": ["m = -3/4, b = 5", "m = 5, b = -3/4", "m = 3/4, b = -5", "m = -3/4, b = -5"], "correcta_texto": "m = -3/4, b = 5", "t_max": 60},
        # ... añade las demás aquí
    ]
    st.session_state.update({
        'juego_iniciado': False, 'paso': 'registro', 'mision': 1, 'n_pregunta': 0, 'aciertos': 0,
        'power_5050': True, 'usar_5050': False, 'banco_total': banco, 'lista_examen': [],
        'preguntas_data': {} # Aquí guardaremos el orden fijo de opciones por pregunta
    })

# --- 4. FUNCIONES ---
def preparar_examen(mision_actual):
    pool = [p for p in st.session_state.banco_total if p['mision'] == mision_actual]
    seleccionadas = random.sample(pool, min(5, len(pool)))
    st.session_state.lista_examen = seleccionadas
    # Generamos y guardamos el orden de las opciones para que NO cambien
    for i, p in enumerate(seleccionadas):
        opts = p['opciones'].copy()
        random.shuffle(opts)
        letras = ["A)", "B)", "C)", "D)"]
        st.session_state.preguntas_data[i] = {
            'finales': [f"{letras[j]} {opts[j]}" for j in range(4)],
            'correcta': ["A", "B", "C", "D"][opts.index(p['correcta_texto'])],
            'letras_incorrectas': [L for L in ["A", "B", "C", "D"] if ["A", "B", "C", "D"][opts.index(p['correcta_texto'])] != L]
        }

def crear_imagen(texto, opciones_finales, letras_a_borrar=[]):
    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor('white')
    texto_mostrar = []
    for opt in opciones_finales:
        if opt[0] in letras_a_borrar:
            texto_mostrar.append(f"{opt[0]} [ ELIMINADA ]")
        else:
            texto_mostrar.append(opt)
    cuerpo = f"{texto}\n\n" + "\n".join(texto_mostrar)
    ax.text(0.05, 0.5, cuerpo, fontsize=14, fontweight='bold', wrap=True, va='center', color='#2d0b2a')
    ax.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    return buf

# --- 5. PANTALLAS ---
if st.session_state.paso == 'registro':
    st.markdown("<div class='status-panel'>MATH QUEST: INGRESO</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='question-card'>", unsafe_allow_html=True)
        nom = st.text_input("Nombre:")
        cur = st.selectbox("Curso:", ["908", "909", "910"])
        if st.button("¡EMPEZAR MISION 1!"):
            if nom:
                preparar_examen(1)
                st.session_state.update({'nombre': nom, 'curso': cur, 'paso': 'examen', 't_inicio_pregunta': time.time(), 'juego_iniciado': True})
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.paso == 'examen':
    idx = st.session_state.n_pregunta
    p = st.session_state.lista_examen[idx]
    data = st.session_state.preguntas_data[idx]
    
    # UI SUPERIOR
    msg = f"Misión {st.session_state.mision} - Guerrero: {st.session_state.nombre}"
    st.markdown(f"<div class='status-panel'>{msg}</div>", unsafe_allow_html=True)

    # BARRA DE TIEMPO
    t_limite = p.get('t_max', 60)
    t_actual = time.time() - st.session_state.t_inicio_pregunta
    porcentaje = max(0, 100 - (t_actual / t_limite * 100))
    st.markdown(f"<div class='energy-container'><div class='energy-bar' style='width:{porcentaje}%'></div></div>", unsafe_allow_html=True)

    # LÓGICA 50/50 (Se mantiene fija una vez activada para esta pregunta)
    letras_ocultas = []
    if st.session_state.usar_5050:
        if f"ocultas_{idx}" not in st.session_state:
            st.session_state[f"ocultas_{idx}"] = random.sample(data['letras_incorrectas'], 2)
        letras_ocultas = st.session_state[f"ocultas_{idx}"]

    # IMAGEN FIJA
    img_buf = crear_imagen(p['pregunta'], data['finales'], letras_ocultas)
    st.markdown("<div class='question-card'>", unsafe_allow_html=True)
    st.image(img_buf)
    st.markdown("</div>", unsafe_allow_html=True)

    # BOTÓN POWER-UP
    if st.session_state.power_5050:
        if st.button("⚡ USAR 50/50"):
            st.session_state.usar_5050 = True
            st.session_state.power_5050 = False
            st.rerun()

    # RESPUESTA (Aquí las letras A, B, C, D ahora son blancas)
    ans = st.radio("TU ELECCIÓN:", ["A", "B", "C", "D"], key=f"r_{idx}_{st.session_state.mision}", index=None, horizontal=True)
    
    if st.button("ENVIAR ➡️"):
        if ans:
            if ans == data['correcta']:
                st.session_state.aciertos += 1
                st.toast("¡CORRECTO!", icon="✅")
            else:
                st.toast("FALLASTE", icon="❌")
            
            # Pasar a la siguiente
            st.session_state.n_pregunta += 1
            st.session_state.usar_5050 = False
            st.session_state.t_inicio_pregunta = time.time()
            if st.session_state.n_pregunta >= len(st.session_state.lista_examen):
                st.session_state.paso = 'feedback'
            st.rerun()

    # Refresh de la barra (Solo si no ha terminado)
    if porcentaje > 0:
        time.sleep(1)
        st.rerun()
    else:
        st.error("TIEMPO AGOTADO")
        time.sleep(1)
        st.session_state.n_pregunta += 1
        st.session_state.t_inicio_pregunta = time.time()
        st.rerun()
