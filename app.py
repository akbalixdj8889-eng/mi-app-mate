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

st.set_page_config(page_title="Examen Noveno - Shuffled", page_icon="🎲")

# --- BANCO DE PREGUNTAS COMPLETO ---
BANCO_PREGUNTAS = [
    # MISIÓN 1: CONCEPTOS Y ECUACIONES (6 preguntas)
    {
        "id": 1, "mision": 1, 
        "pregunta": "Para la función que pasa por A=(-6, 1) y B=(6, 6), ¿cuál es la pendiente m y el corte con el eje Y (b)?", 
        "opciones": ["m = 5/12, b = 3.5", "m = -5/12, b = 3.5", "m = 12/5, b = -3", "m = 5/12, b = -3.5"], 
        "correcta_texto": "m = 5/12, b = 3.5", "tiempo": 240
    },
    {
        "id": 2, "mision": 1, 
        "pregunta": "Ecuación de la recta que pasa por los puntos A(-4, 8) y B(2, -1):", 
        "opciones": ["y = -3/2x + 2", "y = 3/2x + 2", "y = -2/3x + 2", "y = 3/2x - 2"], 
        "correcta_texto": "y = -3/2x + 2", "tiempo": 240
    },
    {
        "id": 3, "mision": 1, 
        "pregunta": "La recta que pasa por el punto P(3, -4) con una pendiente m = -1/3 tiene como fórmula:", 
        "opciones": ["y = -1/3x - 3", "y = -1/3x + 3", "y = 1/3x - 3", "y = -3x - 3"], 
        "correcta_texto": "y = -1/3x - 3", "tiempo": 180
    },
    {
        "id": 4, "mision": 1, 
        "pregunta": "¿Cuál de las siguientes rectas es PARALELA a y = -5/6x - 1?", 
        "opciones": ["y = -5/6x + 9", "y = 6/5x + 4", "y = 5/6x - 1", "y = -6/5x + 2"], 
        "correcta_texto": "y = -5/6x + 9", "tiempo": 120
    },
    {
        "id": 5, "mision": 1, 
        "pregunta": "La recta y = -1/4x + 5 es PERPENDICULAR a la recta:", 
        "opciones": ["y = 4x - 8", "y = -4x + 2", "y = 1/4x - 5", "y = -4/1x + 3"], 
        "correcta_texto": "y = 4x - 8", "tiempo": 120
    },
    {
        "id": 6, "mision": 1, 
        "pregunta": "La recta con pendiente m = 4/5 y que pasa por el punto P(5, 7) cumple que:", 
        "opciones": ["y = 4/5x + 3 y pasa por (0, 3)", "y = -4/5x + 3 y pasa por (5, -1)", "y = 4/5x - 3 y pasa por (10, 5)", "y = 5/4x + 3 y pasa por (4, 8)"], 
        "correcta_texto": "y = 4/5x + 3 y pasa por (0, 3)", "tiempo": 200
    },

    # MISIÓN 2: APLICACIONES (4 preguntas)
    {
        "id": 7, "mision": 2, 
        "pregunta": "Un depósito inicia con 80 galones y pierde 3 galones cada 2 horas. ¿Cuál es la función?", 
        "opciones": ["y = -3/2x + 80", "y = 3/2x + 80", "y = -2/3x + 80", "y = -3/2x - 80"], 
        "correcta_texto": "y = -3/2x + 80", "tiempo": 300
    },
    {
        "id": 8, "mision": 2, 
        "pregunta": "Carpintero cobra $20 base más $15 por cada 4h. Si x son horas y y el costo, ¿cuánto cuesta un trabajo de 12h?", 
        "opciones": ["$65", "$45", "$35", "$70"], 
        "correcta_texto": "$65", "tiempo": 300
    },
    {
        "id": 9, "mision": 2, 
        "pregunta": "Globo A (10m, sube 5m cada 4s). Globo B (40m, baja 7/4 m/s). ¿En qué segundo estarán a la misma altura?", 
        "opciones": ["10 segundos", "8 segundos", "12 segundos", "15 segundos"], 
        "correcta_texto": "10 segundos", "tiempo": 360
    },
    {
        "id": 10, "mision": 2, 
        "pregunta": "Daniel debe $500 y abona $30 cada 2 sem. Sofía debe $800 y abona $80 cada  2 sem. ¿En qué semana sus deudas son iguales?", 
        "opciones": ["Semana 12", "Semana 6", "Semana 10", "Semana 14"], 
        "correcta_texto": "Semana 12", "tiempo": 360
    }
]

# --- FUNCIÓN GENERADORA DE IMAGEN ---
def crear_imagen(texto, opciones_letras):
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.set_facecolor('#ffffff')
    cuerpo = f"{texto}\n\n" + "\n".join(opciones_letras)
    ax.text(0.05, 0.5, cuerpo, fontsize=12, fontweight='bold', wrap=True, family='serif', verticalalignment='center')
    # Ruido sutil para confundir IAs
    ax.scatter(np.random.rand(40)*10, np.random.rand(40), color='blue', s=1, alpha=0.1)
    ax.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    return buf

# --- INICIALIZACIÓN ---
if 'paso' not in st.session_state:
    st.session_state.update({'paso': 'registro', 'mision_actual': 1, 'n_pregunta': 0, 'aciertos': 0})

# --- PANTALLA: REGISTRO ---
if st.session_state.paso == 'registro':
    st.title("🚀 Reto Matemático Noveno")
    st.info("Instrucciones: Resuelve en tu cuaderno y marca la opción. Debes aprobar la Misión 1 para ir a la 2.")
    nom = st.text_input("Nombre Completo:")
    cur = st.selectbox("Curso:", ["901", "902"])
    if st.button("COMENZAR EXAMEN"):
        if nom:
            # Seleccionamos 5 preguntas al azar de la Misión 1
            preguntas_m1 = [p for p in BANCO_PREGUNTAS if p['mision'] == 1]
            st.session_state.update({
                'nombre': nom, 'curso': cur, 'paso': 'examen', 
                'inicio_total': time.time(),
                'lista_preguntas': random.sample(preguntas_m1, 5)
            })
            st.rerun()

# --- PANTALLA: EXAMEN ---
elif st.session_state.paso == 'examen':
    idx = st.session_state.n_pregunta
    p = st.session_state.lista_preguntas[idx]
    
    # Lógica de Mezcla (Shuffling)
    if f"mezcla_{st.session_state.mision_actual}_{idx}" not in st.session_state:
        opts = p['opciones'].copy()
        random.shuffle(opts)
        letras = ["A) ", "B) ", "C) ", "D) "]
        finales = [letras[i] + opts[i] for i in range(len(opts))]
        
        c_idx = opts.index(p['correcta_texto'])
        st.session_state[f"correcta_letra_{idx}"] = ["A", "B", "C", "D"][c_idx]
        st.session_state[f"img_{idx}"] = crear_imagen(p['pregunta'], finales)
        st.session_state[f"mezcla_{st.session_state.mision_actual}_{idx}"] = True

    st.subheader(f"Misión {st.session_state.mision_actual} | Pregunta {idx+1} de 5")
    st.image(st.session_state[f"img_{idx}"])
    
    ans = st.radio("Tu respuesta:", ["A", "B", "C", "D"], key=f"r_{st.session_state.mision_actual}_{idx}", index=None)
    
    if st.button("Siguiente Pregunta ➡️"):
        if ans:
            if ans == st.session_state[f"correcta_letra_{idx}"]:
                st.session_state.aciertos += 1
            st.session_state.n_pregunta += 1
            
            if st.session_state.n_pregunta >= len(st.session_state.lista_preguntas):
                st.session_state.paso = 'feedback'
            st.rerun()

# --- PANTALLA: FEEDBACK ---
elif st.session_state.paso == 'feedback':
    puntos = st.session_state.aciertos
    total = len(st.session_state.lista_preguntas)
    st.title("Resumen de Misión")
    st.metric("Puntaje", f"{puntos} / {total}")
    
    # Enviar reporte
    requests.post(URL_FORM, data={
        ENTRY_NOMBRE: st.session_state.nombre,
        ENTRY_CURSO: st.session_state.curso,
        ENTRY_NOTA: f"Mision {st.session_state.mision_actual}: {puntos}/{total}",
        ENTRY_TIEMPO: f"{int(time.time()-st.session_state.inicio_total)}s"
    })

    if st.session_state.mision_actual == 1:
        if puntos >= 3:
            st.success("🌟 ¡Excelente! Has desbloqueado la Misión 2 (Problemas de Aplicación).")
            if st.button("INGRESAR A MISIÓN 2"):
                preguntas_m2 = [p for p in BANCO_PREGUNTAS if p['mision'] == 2]
                st.session_state.update({
                    'mision_actual': 2, 'n_pregunta': 0, 'aciertos': 0, 'paso': 'examen',
                    'lista_preguntas': random.sample(preguntas_m2, 4), # Son 4 de aplicación
                    'inicio_total': time.time()
                })
                # Limpiar caché de imágenes de Misión 1
                for k in list(st.session_state.keys()):
                    if "img_" in k or "correcta_letra_" in k: del st.session_state[k]
                st.rerun()
        else:
            st.error("Necesitas al menos 3 aciertos para avanzar. ¡Repasa tus apuntes!")
            if st.button("Reintentar Examen"):
                st.session_state.clear()
                st.rerun()
    else:
        st.balloons()
        st.success("🎯 ¡Has completado todas las misiones!")
        if st.button("Finalizar Sesión"):
            st.session_state.clear()
            st.rerun()
