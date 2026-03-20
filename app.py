import streamlit as st
import random
import time
import requests
import matplotlib.pyplot as plt
import io

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Math Quest Pro", page_icon="⚡", layout="centered")

# --- 2. ESTILOS CSS (INCLUYE ANIMACIÓN DE BARRA) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #461a42 0%, #2d0b2a 100%); }
    
    .question-card {
        background-color: white; padding: 20px; border-radius: 20px;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.4); margin-bottom: 10px;
    }

    /* Estilo para el cuadro blanco dinámico */
    .status-panel {
        background-color: white; border-radius: 50px; padding: 10px 30px;
        text-align: center; color: #461a42; font-weight: bold;
        font-size: 1.1rem; min-height: 40px; margin-bottom: 15px;
        display: flex; align-items: center; justify-content: center;
    }

    /* Barra de Energía */
    .energy-container {
        width: 100%; background-color: #ddd; border-radius: 10px; margin-bottom: 20px;
    }
    .energy-bar {
        height: 15px; background: linear-gradient(90deg, #f59e0b, #ef4444);
        border-radius: 10px; transition: width 0.5s ease;
    }

    /* Texto de opciones */
    .stWidgetLabel p { color: white !important; font-size: 1.2rem !important; font-weight: bold !important; }
    div[data-testid="stRadio"] label { color: white !important; font-weight: bold !important; }
    
    /* Botón Power-up */
    .powerup-btn {
        background-color: #10b981 !important; color: white !important;
        border: 2px solid #34d399 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LÓGICA DE ESTADO ---
if 'paso' not in st.session_state:
    st.session_state.update({
        'paso': 'registro', 'mision': 1, 'n_pregunta': 0, 'aciertos': 0,
        'power_5050': True, 'usar_5050': False, 'tiempo_inicio': 0
    })

# --- 4. FUNCIONES ---
def crear_imagen(texto, opciones, ocultas=[]):
    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor('white')
    
    # Si el power-up está activo, tachamos u ocultamos opciones
    finales = []
    for opt in opciones:
        if opt[0] in ocultas: # opt[0] es la letra A, B, C o D
            finales.append(f"{opt[0]} (ELIMINADA)")
        else:
            finales.append(opt)
            
    cuerpo = f"{texto}\n\n" + "\n".join(finales)
    ax.text(0.05, 0.5, cuerpo, fontsize=13, fontweight='bold', wrap=True, va='center', color='#2d0b2a')
    ax.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=120)
    plt.close()
    return buf

# --- 5. BANCO DE PREGUNTAS (Simplificado para ejemplo) ---
BANCO = [
    {"id": "A1", "mision": 1, "pregunta": "Pasa por A=(-4,8) y B=(4,2). ¿m y b?", "opciones": ["m = 5, b = -3/4", "m = 3/4, b = -5", "m = -3/4, b = -5", "m = -3/4, b = 5"], "correcta_texto": "m = -3/4, b = 5", "t_max": 60},
    # ... incluir aquí el resto del banco enviado antes
]

# --- 6. PANTALLAS ---
if st.session_state.paso == 'registro':
    st.markdown("<h1 style='text-align: center; color: white;'>🎮 MATH QUEST PRO</h1>", unsafe_allow_html=True)
    st.markdown("<div class='status-panel'>¡Bienvenido Guerrero! Ingresa tus datos</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='question-card'>", unsafe_allow_html=True)
        nom = st.text_input("Nombre:")
        cur = st.selectbox("Curso:", ["908", "909", "910"])
        if st.button("¡ENTRAR AL JUEGO!"):
            if nom:
                pool = [p for p in BANCO if p['mision'] == 1]
                st.session_state.update({
                    'nombre': nom, 'curso': cur, 'paso': 'examen',
                    'lista_examen': random.sample(pool, 1), # Cambiar a 5 para real
                    'tiempo_inicio_pregunta': time.time()
                })
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.paso == 'examen':
    idx = st.session_state.n_pregunta
    p = st.session_state.lista_examen[idx]
    
    # 1. Cuadro Blanco Dinámico
    msg = "¡Vas por buen camino!" if st.session_state.aciertos > 0 else "¡A por la primera!"
    if st.session_state.usar_5050: msg = "⚡ POWER-UP ACTIVADO: 50/50"
    st.markdown(f"<div class='status-panel'>{msg}</div>", unsafe_allow_html=True)

    # 2. Barra de Energía (Tiempo)
    t_limite = p.get('t_max', 60)
    t_transcurrido = time.time() - st.session_state.tiempo_inicio_pregunta
    porcentaje = max(0, 100 - (t_transcurrido / t_limite * 100))
    st.markdown(f"""<div class='energy-container'><div class='energy-bar' style='width: {porcentaje}%'></div></div>""", unsafe_allow_html=True)

    # 3. Preparación de Pregunta e Imagen
    if f"img_data_{idx}" not in st.session_state:
        opts = p['opciones'].copy()
        random.shuffle(opts)
        st.session_state[f"opts_{idx}"] = [f"{['A)','B)','C)','D)'][i]} {opts[i]}" for i in range(4)]
        st.session_state[f"correcta_{idx}"] = ["A", "B", "C", "D"][opts.index(p['correcta_texto'])]

    # Lógica 50/50
    ocultas = []
    if st.session_state.usar_5050:
        correcta = st.session_state[f"correcta_{idx}"]
        incorrectas = [L for L in ["A", "B", "C", "D"] if L != correcta]
        ocultas = random.sample(incorrectas, 2)

    img = crear_imagen(p['pregunta'], st.session_state[f"opts_{idx}"], ocultas)
    
    st.markdown("<div class='question-card'>", unsafe_allow_html=True)
    st.image(img)
    st.markdown("</div>", unsafe_allow_html=True)

    # 4. Controles y Power-ups
    col_p1, col_p2 = st.columns([3, 1])
    with col_p2:
        if st.session_state.power_5050:
            if st.button("⚡ 50/50", help="Elimina 2 incorrectas"):
                st.session_state.usar_5050 = True
                st.session_state.power_5050 = False # Se gasta
                st.rerun()
    
    ans = st.radio("SELECCIONA:", ["A", "B", "C", "D"], key=f"ans_{idx}", index=None, horizontal=True)
    
    if st.button("ENVIAR ➡️"):
        if ans:
            if ans == st.session_state[f"correcta_{idx}"]:
                st.session_state.aciertos += 1
                st.toast("¡CORRECTO!", icon="✅")
            else:
                st.toast("FALLASTE", icon="❌")
            
            st.session_state.n_pregunta += 1
            st.session_state.usar_5050 = False # Resetear para la siguiente
            st.session_state.tiempo_inicio_pregunta = time.time()
            if st.session_state.n_pregunta >= len(st.session_state.lista_examen):
                st.session_state.paso = 'feedback'
            st.rerun()

    # Auto-refresh para la barra de tiempo
    time.sleep(1)
    if porcentaje > 0: st.rerun()
    else: st.error("¡TIEMPO AGOTADO!"); time.sleep(1); st.session_state.n_pregunta += 1; st.rerun()
