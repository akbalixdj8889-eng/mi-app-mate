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

st.set_page_config(page_title="Examen Noveno - Matemáticas", page_icon="📐")

# --- BANCO DE PREGUNTAS (Tus preguntas de LaTeX) ---
BANCO_NOVENO = [
    {
        "id": 1,
        "pregunta": "Para la función que pasa por A=(-6, 1) y B=(6, 6),\n¿cuál es la pendiente m y el corte con el eje Y (b)?",
        "opciones": ["A) m=5/12, b=3.5", "B) m=-5/12, b=3.5", "C) m=12/5, b=-3", "D) m=5/12, b=-3.5"],
        "correcta": "A",
        "tiempo": 240
    },
    {
        "id": 2,
        "pregunta": "Ecuación de la recta que pasa por\nA(-4, 8) y B(2, -1):",
        "opciones": ["A) y=3/2x + 2", "B) y=-3/2x + 2", "C) y=-2/3x + 2", "D) y=3/2x - 2"],
        "correcta": "B",
        "tiempo": 240
    },
    {
        "id": 4,
        "pregunta": "¿Cuál recta es PARALELA a y = -5/6x - 1?",
        "opciones": ["A) y=6/5x + 4", "B) y=5/6x - 1", "C) y=-5/6x + 9", "D) y=-6/5x + 2"],
        "correcta": "C",
        "tiempo": 120
    },
    {
        "id": 5,
        "pregunta": "La recta y = -1/4x + 5 es PERPENDICULAR a:",
        "opciones": ["A) y=-4x + 2", "B) y=1/4x - 5", "C) y=4x - 8", "D) y=-4/1x + 3"],
        "correcta": "C",
        "tiempo": 120
    }
]

# --- FUNCIÓN GENERADORA DE IMAGEN ---
def crear_imagen_pregunta(texto, opciones):
    fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
    ax.set_facecolor('#f0f2f6')
    
    # Unir pregunta y opciones
    contenido = f"{texto}\n\n" + "\n".join(opciones)
    
    # Dibujar texto con "Ruido" anti-IA
    ax.text(0.05, 0.5, contenido, fontsize=14, fontweight='bold', color='#0e1117',
            ha='left', va='center', wrap=True, family='sans-serif')
    
    # Ruido visual (Líneas y puntos)
    for _ in range(5):
        ax.plot([random.random()*8, random.random()*8], [0, 1], color='blue', alpha=0.1, lw=2)
    ax.scatter(np.random.rand(100)*8, np.random.rand(100), color='gray', s=1, alpha=0.1)
    
    ax.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    return buf

# --- LÓGICA DE SESIÓN ---
if 'paso' not in st.session_state: st.session_state.paso = "registro"

if st.session_state.paso == "registro":
    st.title("📝 Evaluación de Matemáticas - Noveno")
    nombre = st.text_input("Nombre del Estudiante:")
    curso = st.selectbox("Curso:", ["901", "902", "903"])
    
    if st.button("Iniciar Evaluación"):
        if nombre:
            st.session_state.nombre = nombre
            st.session_state.curso = curso
            st.session_state.pregunta_actual = random.choice(BANCO_NOVENO)
            st.session_state.inicio_time = time.time()
            st.session_state.paso = "examen"
            st.rerun()

elif st.session_state.paso == "examen":
    p = st.session_state.pregunta_actual
    transcurrido = int(time.time() - st.session_state.inicio_time)
    restante = p['tiempo'] - transcurrido

    if restante <= 0:
        st.error("⏳ TIEMPO AGOTADO. Se ha registrado como intento fallido.")
        requests.post(URL_FORM, data={ENTRY_NOMBRE: st.session_state.nombre, ENTRY_NOTA: "ANULADO - TIEMPO"})
        if st.button("Salir"): st.session_state.paso = "registro"; st.rerun()
    else:
        st.write(f"Estudiante: **{st.session_state.nombre}** | Tiempo: **{restante}s**")
        
        # Generar imagen (solo una vez por pregunta)
        if 'img_buf' not in st.session_state:
            st.session_state.img_buf = crear_imagen_pregunta(p['pregunta'], p['opciones'])
        
        st.image(st.session_state.img_buf)
        
        seleccion = st.radio("Selecciona tu respuesta justificada:", ["A", "B", "C", "D"], index=None)
        
        if st.button("Enviar Respuesta"):
            if seleccion:
                resultado = "Correcto" if seleccion == p['correcta'] else f"Incorrecto (Marcó {seleccion})"
                requests.post(URL_FORM, data={
                    ENTRY_NOMBRE: st.session_state.nombre,
                    ENTRY_CURSO: st.session_state.curso,
                    ENTRY_NOTA: f"Pregunta {p['id']}: {resultado}",
                    ENTRY_TIEMPO: f"{transcurrido}s"
                })
                st.success("Respuesta enviada. ¡Revisa tu cuaderno con el profesor!")
                if st.button("Finalizar"): 
                    del st.session_state.img_buf
                    st.session_state.paso = "registro"
                    st.rerun()
