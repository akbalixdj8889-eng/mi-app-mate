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

st.set_page_config(page_title="Examen Noveno", page_icon="📐")

# --- BANCO DE PREGUNTAS ---
BANCO_NOVENO = [
    {"id": 1, "pregunta": "Pasa por A=(-6, 1) y B=(6, 6). ¿Pendiente m y corte Y (b)?", "opciones": ["A) m=5/12, b=3.5", "B) m=-5/12, b=3.5", "C) m=12/5, b=-3", "D) m=5/12, b=-3.5"], "correcta": "A", "tiempo": 240},
    {"id": 2, "pregunta": "Ecuación de la recta por A(-4, 8) y B(2, -1):", "opciones": ["A) y=3/2x + 2", "B) y=-3/2x + 2", "C) y=-2/3x + 2", "D) y=3/2x - 2"], "correcta": "B", "tiempo": 240},
    {"id": 4, "pregunta": "¿Cuál es PARALELA a y = -5/6x - 1?", "opciones": ["A) y=6/5x + 4", "B) y=5/6x - 1", "C) y=-5/6x + 9", "D) y=-6/5x + 2"], "correcta": "C", "tiempo": 120},
    {"id": 5, "pregunta": "La recta y = -1/4x + 5 es PERPENDICULAR a:", "opciones": ["A) y=-4x + 2", "B) y=1/4x - 5", "C) y=4x - 8", "D) y=-4/1x + 3"], "correcta": "C", "tiempo": 120}
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

# --- LÓGICA DE NAVEGACIÓN ---
if 'paso' not in st.session_state: st.session_state.paso = "registro"

if st.session_state.paso == "registro":
    st.title("📝 Evaluación de Matemáticas")
    nombre = st.text_input("Nombre del Estudiante:")
    curso = st.selectbox("Curso:", ["901", "902", "903"])
    if st.button("Iniciar"):
        if nombre:
            st.session_state.nombre = nombre
            st.session_state.curso = curso
            st.session_state.pregunta_actual = random.choice(BANCO_NOVENO)
            st.session_state.inicio_time = time.time()
            st.session_state.paso = "examen"
            st.rerun()

elif st.session_state.paso == "examen":
    p = st.session_state.pregunta_actual
    restante = p['tiempo'] - int(time.time() - st.session_state.inicio_time)

    if restante <= 0:
        st.error("⏳ TIEMPO AGOTADO.")
        requests.post(URL_FORM, data={ENTRY_NOMBRE: st.session_state.nombre, ENTRY_NOTA: f"Preg {p['id']}: TIEMPO AGOTADO"})
        if st.button("Volver al inicio"):
            st.session_state.clear()
            st.rerun()
    else:
        st.write(f"Estudiante: **{st.session_state.nombre}** | Tiempo: **{restante}s**")
        
        # Mostrar imagen
        img = crear_imagen_pregunta(p['pregunta'], p['opciones'])
        st.image(img)
        
        seleccion = st.radio("Tu respuesta:", ["A", "B", "C", "D"], key="radio_preg", index=None)
        
        if st.button("ENVIAR Y TERMINAR"):
            if seleccion:
                # 1. Evaluar
                es_correcta = (seleccion == p['correcta'])
                resultado = "Correcto" if es_correcta else f"Incorrecto (Marcó {seleccion})"
                
                # 2. Registrar en Google (No importa si falló)
                requests.post(URL_FORM, data={
                    ENTRY_NOMBRE: st.session_state.nombre,
                    ENTRY_CURSO: st.session_state.curso,
                    ENTRY_NOTA: f"Pregunta {p['id']}: {resultado}",
                    ENTRY_TIEMPO: f"{int(time.time() - st.session_state.inicio_time)}s"
                })
                
                # 3. Mostrar mensaje final y limpiar para el siguiente
                st.session_state.paso = "finalizado"
                st.rerun()
            else:
                st.warning("Selecciona una opción antes de enviar.")

elif st.session_state.paso == "finalizado":
    st.success("✅ Tu respuesta ha sido registrada correctamente.")
    st.write("Puedes cerrar esta pestaña o iniciar un nuevo ejercicio.")
    if st.button("Hacer otra pregunta"):
        st.session_state.clear() # Limpia todo para que el siguiente estudiante o pregunta sea nueva
        st.rerun()
