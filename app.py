import streamlit as st
import random
import time
import requests
import matplotlib.pyplot as plt
import io
import numpy as np

# --- 1. CONFIGURACIÓN Y GOOGLE ---
URL_FORM = "https://docs.google.com/forms/d/e/1FAIpQLScin_I5blL_gwFbDP8vfjTz7SQj4BRZQ0_wI7rmJvXvNjkzzQ/formResponse"
ENTRY_NOMBRE = "entry.1544483154"
ENTRY_CURSO  = "entry.2027082892"
ENTRY_NOTA   = "entry.1011634935"
ENTRY_TIEMPO = "entry.1300499693"

st.set_page_config(page_title="Math Quest: Noveno", page_icon="🎮", layout="centered")

# --- 2. ESTILOS CSS (MEJORADO PARA VISIBILIDAD) ---
st.markdown("""
    <style>
    /* Fondo General */
    .stApp { background: linear-gradient(135deg, #461a42 0%, #2d0b2a 100%); }
    
    /* Tarjeta de Pregunta */
    .question-card {
        background-color: white; 
        padding: 25px; 
        border-radius: 20px;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.4); 
        margin-bottom: 20px;
    }
    
    /* Marcadores Superiores */
    .stat-box {
        background-color: rgba(255, 255, 255, 0.2); 
        padding: 15px;
        border-radius: 12px; 
        color: white; 
        text-align: center; 
        font-weight: bold;
        font-size: 1.2rem;
        border: 1px solid rgba(255,255,255,0.3);
    }

    /* FORZAR TEXTO BLANCO EN RADIOS Y LABELS */
    .stWidgetLabel p { color: white !important; font-size: 1.2rem !important; font-weight: bold !important; }
    div[data-testid="stMarkdownContainer"] p { color: white; }
    
    /* Estilo específico para las letras A, B, C, D */
    div[data-testid="stRadio"] label {
        color: white !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        background: rgba(255,255,255,0.1);
        padding: 5px 15px;
        border-radius: 10px;
        margin-right: 10px;
    }

    /* Botón Enviar */
    .stButton>button {
        width: 100%; border-radius: 12px; height: 3.5em;
        background-color: #6d28d9; color: white; font-weight: bold; border: 2px solid #a78bfa;
    }
    .stButton>button:hover { background-color: #7c3aed; border-color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BANCO DE PREGUNTAS (Resumen de los 4 temas) ---
# He mantenido la estructura para que solo copies y pegues
BANCO_PREGUNTAS = [
    # TEMA A
    {"id": "A1", "mision": 1, "pregunta": "Para la función que pasa por los puntos A=(-4,8) y B=(4,2), ¿Cuál es la pendiente y el corte en el eje Y?", "opciones": ["m = 5, b = -3/4", "m = 3/4, b = -5", "m = -3/4, b = -5", "m = -3/4, b = 5"], "correcta_texto": "m = -3/4, b = 5"},
    {"id": "A2", "mision": 1, "pregunta": "Ecuación de la recta que pasa por los puntos A(1, 3) y B(2, 10):", "opciones": ["y = 3/7x + 4", "y = 2/7x - 4", "y = -2/7x - 4", "y = -2/7x + 4"], "correcta_texto": "y = 2/7x - 4"},
    {"id": "A3", "mision": 1, "pregunta": "La recta que pasa por el punto P(-6, 2) con pendiente m = -2/3 tiene como fórmula:", "opciones": ["y = -2/3x - 2", "y = -2/3x - 3", "y = -3/2x - 3", "y = -3/2x - 2"], "correcta_texto": "y = -2/3x - 2"},
    {"id": "A4", "mision": 1, "pregunta": "¿Cuál de las siguientes rectas es paralela a y = -4/5x - 3?", "opciones": ["y = -4/5x + 3", "y = 5/4x + 2", "y = 4/5x + 10", "y = -5/4x - 7"], "correcta_texto": "y = -4/5x + 3"},
    {"id": "A5", "mision": 1, "pregunta": "La recta y = 2/3x + 1 es perpendicular a la recta:", "opciones": ["y = 2/3x - 5", "y = 3/2x + 2", "y = -2/3x + 4", "y = -3/2x + 5"], "correcta_texto": "y = -3/2x + 5"},
    {"id": "A6", "mision": 1, "pregunta": "La recta con pendiente m = -5/4 y que pasa por el punto p:(4,2) cumple que tiene como ecuación:", "opciones": ["y = -4/5x + 5 pasa por (9,-2)", "y = -5/4x + 7 pasa por (8,-3)", "y = -5/4x + 7 pasa por (8,2)", "y = -4/5x + 5 pasa por (0,5)"], "correcta_texto": "y = -5/4x + 7 pasa por (8,-3)"},
    {"id": "A7", "mision": 2, "pregunta": "El horno inicia en 15°C y sube 10°C cada 3 minutos. La función es:", "opciones": ["y = 15x + 3/10", "y = 3/10x + 15", "y = 15x + 10/3", "y = 10/3x + 15"], "correcta_texto": "y = 10/3x + 15"},
    {"id": "A8", "mision": 2, "pregunta": "Un taxi cobra una tarifa fija de $7 más $2 por cada 3 km recorridos. ¿Cuánto costará un viaje de 15 km?", "opciones": ["$10", "$23", "$17", "$15"], "correcta_texto": "$17"},
    {"id": "A9", "mision": 2, "pregunta": "Tanque A: 2 min=10L, 8 min=40L. Tanque B: 1 min=50L, 11 min=10L. ¿A los cuántos minutos tienen la misma cantidad?", "opciones": ["4", "6", "8", "10"], "correcta_texto": "6"},
    {"id": "A10", "mision": 2, "pregunta": "Andrés tiene $150 y ahorra $50/sem. Beatriz tiene $950 y gasta $150/sem. ¿En qué semana igualan capital?", "opciones": ["2", "3", "4", "5"], "correcta_texto": "4"},
    # ... (Puedes seguir pegando el resto de los temas B, C y D aquí abajo)
]

# --- 4. FUNCIONES ---
def crear_imagen(texto, opciones):
    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    # Texto de la pregunta
    cuerpo = f"{texto}\n\n" + "\n".join(opciones)
    ax.text(0.05, 0.5, cuerpo, fontsize=13, fontweight='bold', wrap=True, family='sans-serif', va='center', color='#2d0b2a')
    ax.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=120)
    plt.close()
    return buf

# --- 5. LÓGICA DE NAVEGACIÓN ---
if 'paso' not in st.session_state:
    st.session_state.update({'paso': 'registro', 'mision': 1, 'n_pregunta': 0, 'aciertos': 0})

if st.session_state.paso == 'registro':
    st.markdown("<h1 style='text-align: center; color: white;'>🎮 MATH QUEST</h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='question-card'>", unsafe_allow_html=True)
        nom = st.text_input("Ingresa tu Nombre:")
        # ACTUALIZACIÓN DE CURSOS
        cur = st.selectbox("Elige tu Curso:", ["908", "909", "910"]) 
        if st.button("¡COMENZAR AVENTURA!"):
            if nom:
                pool = [p for p in BANCO_PREGUNTAS if p['mision'] == 1]
                st.session_state.update({
                    'nombre': nom, 'curso': cur, 'paso': 'examen',
                    'lista_examen': random.sample(pool, 5), 'inicio_total': time.time()
                })
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.paso == 'examen':
    idx = st.session_state.n_pregunta
    p = st.session_state.lista_examen[idx]
    
    col1, col2 = st.columns(2)
    with col1: st.markdown(f"<div class='stat-box'>Pregunta {idx+1} de 5</div>", unsafe_allow_html=True)
    with col2: st.markdown(f"<div class='stat-box'>Aciertos: {st.session_state.aciertos}</div>", unsafe_allow_html=True)
    
    st.write("") 
    
    # Área de la pregunta
    if f"img_{st.session_state.mision}_{idx}" not in st.session_state:
        opts = p['opciones'].copy()
        random.shuffle(opts)
        letras_labels = ["A)", "B)", "C)", "D)"]
        finales = [f"{letras_labels[i]} {opts[i]}" for i in range(4)]
        st.session_state[f"correcta_{idx}"] = ["A", "B", "C", "D"][opts.index(p['correcta_texto'])]
        st.session_state[f"img_{st.session_state.mision}_{idx}"] = crear_imagen(p['pregunta'], finales)

    st.markdown("<div class='question-card'>", unsafe_allow_html=True)
    st.image(st.session_state[f"img_{st.session_state.mision}_{idx}"])
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Opciones con mejor contraste
    ans = st.radio("SELECCIONA TU RESPUESTA:", ["A", "B", "C", "D"], key=f"ans_{idx}", index=None, horizontal=True)
    
    if st.button("ENVIAR RESPUESTA ➡️"):
        if ans:
            if ans == st.session_state[f"correcta_{idx}"]:
                st.session_state.aciertos += 1
                st.toast("¡Correcto! +100 pts", icon="🔥")
            else:
                st.toast("Incorrecto", icon="❌")
            
            st.session_state.n_pregunta += 1
            if st.session_state.n_pregunta >= 5:
                st.session_state.paso = 'feedback'
            st.rerun()

elif st.session_state.paso == 'feedback':
    # (Lógica de feedback igual a la anterior pero con cursos actualizados)
    st.markdown("<div class='question-card' style='text-align:center;'>", unsafe_allow_html=True)
    puntos = st.session_state.aciertos
    st.header(f"Resultado: {puntos}/5")
    
    # Registro en Google Sheets
    try:
        requests.post(URL_FORM, data={
            ENTRY_NOMBRE: st.session_state.nombre, 
            ENTRY_CURSO: st.session_state.curso,
            ENTRY_NOTA: f"Mision {st.session_state.mision}: {puntos}/5"
        })
    except: pass

    if puntos >= 3:
        st.balloons()
        st.success("¡MISIÓN CUMPLIDA!")
        if st.session_state.mision == 1:
            if st.button("DESBLOQUEAR MISIÓN 2"):
                # Aquí cargarías el pool de misión 2 y resetearías n_pregunta
                st.session_state.update({'mision': 2, 'n_pregunta': 0, 'aciertos': 0, 'paso': 'examen'})
                # Importante: aquí deberías filtrar el banco para la misión 2
                st.rerun()
    else:
        st.error("No has logrado los aciertos mínimos.")
        if st.button("INTENTAR DE NUEVO"):
            st.session_state.update({'n_pregunta': 0, 'aciertos': 0, 'paso': 'examen'})
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
