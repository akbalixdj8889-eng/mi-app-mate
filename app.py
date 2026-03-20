
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


# --- 3. BANCO DE PREGUNTAS (40 PREGUNTAS) ---
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



























