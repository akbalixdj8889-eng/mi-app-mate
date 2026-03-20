import streamlit as st
import random
import time
import requests
import matplotlib.pyplot as plt
import io
import numpy as np

# --- CONFIGURACIÓN GOOGLE ---
URL_FORM = "https://docs.google.com/forms/d/e/1FAIpQLScin_I5blL_gwFbDP8vfjTz7SQj4BRZQ0_wI7rmJvXvNjkzzQ/formResponse"
ENTRY_NOMBRE = "entry.1544483154"
ENTRY_CURSO  = "entry.2027082892"
ENTRY_NOTA   = "entry.1011634935"
ENTRY_TIEMPO = "entry.1300499693"

st.set_page_config(page_title="Examen 5 Preguntas", page_icon="📝")

# --- BANCO DE PREGUNTAS (Puedes agregar las 10 aquí) ---
BANCO_NOVENO = [
    {"id": 1, "pregunta": "Pasa por A=(-6, 1) y B=(6, 6). ¿m y b?", "opciones": ["A) m=5/12, b=3.5", "B) m=-5/12, b=3.5", "C) m=12/5, b=-3", "D) m=5/12, b=-3.5"], "correcta": "A", "tiempo": 180},
    {"id": 2, "pregunta": "Ecuación por A(-4, 8) y B(2, -1):", "opciones": ["A) y=3/2x + 2", "B) y=-3/2x + 2", "C) y=-2/3x + 2", "D) y=3/2x - 2"], "correcta": "B", "tiempo": 180},
    {"id": 3, "pregunta": "Punto P(3, -4) y m = -1/3. ¿Fórmula?", "opciones": ["A) y=-1/3x - 3", "B) y=-1/3x + 3", "C) y=1/3x - 3", "D) y=-3x - 3"], "correcta": "A", "tiempo": 180},
    {"id": 4, "pregunta": "¿Recta PARALELA a y = -5/6x - 1?", "opciones": ["A) y=6/5x + 4", "B) y=5/6x - 1", "C) y=-5/6x + 9", "D) y=-6/5x + 2"], "correcta": "C", "tiempo": 120},
    {"id": 5, "pregunta": "Recta y = -1/4x + 5 es PERPENDICULAR a:", "opciones": ["A) y=-4x + 2", "B) y=1/4x - 5", "C) y=4x - 8", "D) y=-4/1x + 3"], "correcta": "C", "tiempo": 120}
]

def crear_imagen_pregunta(texto, opciones):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_facecolor('#f0f2f6')
    contenido = f"{texto}\n\n" + "\n".join(opciones)
    ax.text(0.05, 0.5, contenido, fontsize=14, fontweight='bold', wrap=True)
    ax.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    return buf

# --- INICIALIZACIÓN DE SESIÓN ---
if 'paso' not in st.session_state:
    st.session_state.paso = "registro"
    st.session_state.preguntas_respondidas = 0
    st.session_state.aciertos = 0
    st.session_state.historial = []

# --- PANTALLA 1: REGISTRO ---
if st.session_state.paso == "registro":
    st.title("🎯 Reto de Matemáticas: 5 Preguntas")
    st.write("Ingresa tus datos una sola vez para comenzar el examen.")
    
    nom = st.text_input("Nombre completo:")
    cur = st.selectbox("Curso:", ["901", "902", "903"])
    
    if st.button("Comenzar Examen"):
        if nom:
            st.session_state.nombre = nom
            st.session_state.curso = cur
            st.session_state.paso = "examen"
            # Seleccionar 5 preguntas aleatorias sin repetir
            st.session_state.lista_examen = random.sample(BANCO_NOVENO, 5)
            st.session_state.inicio_total = time.time()
            st.rerun()

# --- PANTALLA 2: EXAMEN ---
elif st.session_state.paso == "examen":
    n = st.session_state.preguntas_respondidas
    pregunta = st.session_state.lista_examen[n]
    
    st.info(f"Pregunta {n+1} de 5")
    st.write(f"Estudiante: **{st.session_state.nombre}**")

    # Imagen blindada
    img = crear_imagen_pregunta(pregunta['pregunta'], pregunta['opciones'])
    st.image(img)
    
    ans = st.radio("Tu respuesta:", ["A", "B", "C", "D"], key=f"p_{n}", index=None)

    if st.button("Siguiente Pregunta ➡️"):
        if ans:
            # Validar y Guardar
            es_correcta = (ans == pregunta['correcta'])
            if es_correcta: st.session_state.aciertos += 1
            
            st.session_state.preguntas_respondidas += 1
            
            # ¿Ya terminó las 5?
            if st.session_state.preguntas_respondidas >= 5:
                st.session_state.paso = "finalizado"
            st.rerun()
        else:
            st.warning("Por favor selecciona una respuesta.")

# --- PANTALLA 3: RESULTADOS Y ENVÍO ---
elif st.session_state.paso == "finalizado":
    st.title("✅ ¡Examen Terminado!")
    puntaje = st.session_state.aciertos
    tiempo_fin = int(time.time() - st.session_state.inicio_total)
    
    st.balloons()
    st.metric("Tu puntaje final", f"{puntaje} / 5")
    
    # Enviar un solo reporte consolidado a Google Sheets
    nota_final = f"Puntaje: {puntaje}/5"
    try:
        requests.post(URL_FORM, data={
            ENTRY_NOMBRE: st.session_state.nombre,
            ENTRY_CURSO: st.session_state.curso,
            ENTRY_NOTA: nota_final,
            ENTRY_TIEMPO: f"{tiempo_fin}s"
        })
        st.success("Tus resultados han sido enviados al profesor.")
    except:
        st.error("Error al enviar. Avisa al profesor.")

    if st.button("Reiniciar para otro estudiante"):
        st.session_state.clear()
        st.rerun()
