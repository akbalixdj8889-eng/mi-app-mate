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

st.set_page_config(page_title="Misiones Matemáticas - Noveno", page_icon="🚀")

# --- BANCO DE PREGUNTAS COMPLETO ---
BANCO_PREGUNTAS = [
    # MISIÓN 1: CONCEPTOS Y ECUACIONES
    {"id": 1, "mision": 1, "pregunta": "Puntos A(-6, 1) y B(6, 6). ¿Pendiente m y corte Y (b)?", "opciones": ["A) m=5/12, b=3.5", "B) m=-5/12, b=3.5", "C) m=12/5, b=-3", "D) m=5/12, b=-3.5"], "correcta": "A", "tiempo": 240},
    {"id": 2, "mision": 1, "pregunta": "Ecuación de la recta por A(-4, 8) y B(2, -1):", "opciones": ["A) y=3/2x + 2", "B) y=-3/2x + 2", "C) y=-2/3x + 2", "D) y=3/2x - 2"], "correcta": "B", "tiempo": 240},
    {"id": 3, "mision": 1, "pregunta": "Recta por P(3, -4) con m = -1/3. ¿Fórmula?", "opciones": ["A) y=-1/3x - 3", "B) y=-1/3x + 3", "C) y=1/3x - 3", "D) y=-3x - 3"], "correcta": "A", "tiempo": 180},
    {"id": 4, "mision": 1, "pregunta": "¿Qué recta es PARALELA a y = -5/6x - 1?", "opciones": ["A) y=6/5x + 4", "B) y=5/6x - 1", "C) y=-5/6x + 9", "D) y=-6/5x + 2"], "correcta": "C", "tiempo": 120},
    {"id": 5, "mision": 1, "pregunta": "La recta y = -1/4x + 5 es PERPENDICULAR a:", "opciones": ["A) y=-4x + 2", "B) y=1/4x - 5", "C) y=4x - 8", "D) y=-4/1x + 3"], "correcta": "C", "tiempo": 120},
    {"id": 6, "mision": 1, "pregunta": "Recta m = 4/5 por P(5, 7). ¿Cuál cumple?", "opciones": ["A) y=4/5x + 3 y pasa por (0,3)", "B) y=-4/5x + 3 y pasa por (5,-1)", "C) y=4/5x - 3 y pasa por (10,5)", "D) y=5/4x + 3 y pasa por (4,8)"], "correcta": "A", "tiempo": 200},

    # MISIÓN 2: APLICACIONES (Mundo Real)
    {"id": 7, "mision": 2, "pregunta": "Depósito de 80 gal. Pierde 3 gal cada 2 horas. ¿Función?", "opciones": ["A) y=3/2x + 80", "B) y=-2/3x + 80", "C) y=-3/2x + 80", "D) y=-3/2x - 80"], "correcta": "C", "tiempo": 300},
    {"id": 8, "mision": 2, "pregunta": "Carpintero: $20 base + $15 c/4h. ¿Costo por 12 horas?", "opciones": ["A) $45", "B) $65", "C) $35", "D) $70"], "correcta": "B", "tiempo": 300},
    {"id": 9, "mision": 2, "pregunta": "Globo A (10m, sube 5/4 m/s). Globo B (40m, baja 7/4 m/s). ¿En qué segundo se cruzan?", "opciones": ["A) 8s", "B) 10s", "C) 12s", "D) 15s"], "correcta": "B", "tiempo": 360},
    {"id": 10, "mision": 2, "pregunta": "Daniel (deuda $500, abona $15/sem). Sofía (deuda $800, abona $40/sem). ¿Semana de igualdad?", "opciones": ["A) Sem 6", "B) Sem 10", "C) Sem 12", "D) Sem 14"], "correcta": "C", "tiempo": 360}
]

# --- FUNCIÓN GENERADORA DE IMAGEN ---
def crear_imagen(texto, opciones):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_facecolor('#fdfdfd')
    # Texto con ruido anti-IA
    contenido = f"{texto}\n\n" + "\n".join(opciones)
    ax.text(0.05, 0.5, contenido, fontsize=13, fontweight='bold', wrap=True, family='serif')
    for _ in range(4):
        ax.plot([random.random()*8, random.random()*8], [0, 1], color='red', alpha=0.05, lw=1)
    ax.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    return buf

# --- INICIALIZACIÓN DE ESTADOS ---
if 'mision_actual' not in st.session_state:
    st.session_state.update({
        'paso': 'registro', 'mision_actual': 1, 'n_pregunta': 0,
        'aciertos': 0, 'lista_preguntas': [], 'inicio_total': 0
    })

# --- FLUJO: REGISTRO ---
if st.session_state.paso == 'registro':
    st.title("🚀 Misiones Matemáticas: Nivel Noveno")
    st.write("Debes completar la **Misión 1** con al menos 3 aciertos para desbloquear la **Misión 2**.")
    nom = st.text_input("Nombre:")
    cur = st.selectbox("Curso:", ["901", "902"])
    if st.button("INICIAR AVENTURA"):
        if nom:
            st.session_state.nombre, st.session_state.curso = nom, cur
            st.session_state.lista_preguntas = random.sample([p for p in BANCO_PREGUNTAS if p['mision'] == 1], 5)
            st.session_state.paso, st.session_state.inicio_total = 'examen', time.time()
            st.rerun()

# --- FLUJO: EXAMEN ---
elif st.session_state.paso == 'examen':
    idx = st.session_state.n_pregunta
    p = st.session_state.lista_preguntas[idx]
    
    st.subheader(f"Misión {st.session_state.mision_actual} - Pregunta {idx+1}/5")
    st.image(crear_imagen(p['pregunta'], p['opciones']))
    
    ans = st.radio("Selecciona tu respuesta:", ["A", "B", "C", "D"], key=f"r_{st.session_state.mision_actual}_{idx}", index=None)
    
    if st.button("Siguiente ➡️"):
        if ans:
            if ans == p['correcta']: st.session_state.aciertos += 1
            st.session_state.n_pregunta += 1
            
            if st.session_state.n_pregunta >= 5:
                st.session_state.paso = 'feedback_mision'
            st.rerun()

# --- FLUJO: FEEDBACK DE MISIÓN ---
elif st.session_state.paso == 'feedback_mision':
    puntos = st.session_state.aciertos
    st.title("Fin de la Misión")
    st.metric("Puntaje Obtenido", f"{puntos} / 5")
    
    # Reporte a Google
    requests.post(URL_FORM, data={
        ENTRY_NOMBRE: st.session_state.nombre,
        ENTRY_CURSO: st.session_state.curso,
        ENTRY_NOTA: f"Misión {st.session_state.mision_actual}: {puntos}/5",
        ENTRY_TIEMPO: f"{int(time.time()-st.session_state.inicio_total)}s"
    })

    if st.session_state.mision_actual == 1:
        if puntos >= 3:
            st.success("🎉 ¡MISIÓN 1 COMPLETADA! Has desbloqueado la Misión 2.")
            if st.button("IR A LA MISIÓN 2"):
                st.session_state.update({
                    'mision_actual': 2, 'n_pregunta': 0, 'aciertos': 0, 'paso': 'examen',
                    'lista_preguntas': random.sample([p for p in BANCO_PREGUNTAS if p['mision'] == 2], 4),
                    'inicio_total': time.time()
                })
                st.rerun()
        else:
            st.error("❌ No lograste los aciertos necesarios para la Misión 2. Repasa y vuelve a intentar.")
            if st.button("REINTENTAR MISIÓN 1"):
                st.session_state.update({'paso': 'registro', 'aciertos': 0, 'n_pregunta': 0})
                st.rerun()
    else:
        st.success("🎓 ¡Has terminado todas las misiones disponibles!")
        if st.button("FINALIZAR"):
            st.session_state.clear()
            st.rerun()
