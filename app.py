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

st.set_page_config(page_title="Misiones Noveno - Full Bank", page_icon="🚀")

# --- BANCO DE PREGUNTAS COMPLETO (Temas A, B, C, D) ---
BANCO_PREGUNTAS = [
    # --- TEMA A ---
    {"id": "A1", "mision": 1, "pregunta": "Para la función que pasa por los puntos A=(-4,8) y B=(4,2), ¿Cuál es la pendiente y el corte en el eje Y?", "opciones": ["m = 5, b = -3/4", "m = 3/4, b = -5", "m = -3/4, b = -5", "m = -3/4, b = 5"], "correcta_texto": "m = -3/4, b = 5", "tiempo": 240},
    {"id": "A2", "mision": 1, "pregunta": "Al dibujar la ecuación se determina que la ecuación de la recta que pasa por los puntos A(1, 3) y B(2, 10) es:", "opciones": ["y = 3/7x + 4", "y = 2/7x - 4", "y = -2/7x - 4", "y = -2/7x + 4"], "correcta_texto": "y = 2/7x - 4", "tiempo": 240},
    {"id": "A3", "mision": 1, "pregunta": "La recta que pasa por el punto P(-6, 2) con pendiente m = -2/3 tiene como fórmula:", "opciones": ["y = -2/3x - 2", "y = -2/3x - 3", "y = -3/2x - 3", "y = -3/2x - 2"], "correcta_texto": "y = -2/3x - 2", "tiempo": 180},
    {"id": "A4", "mision": 1, "pregunta": "¿Cuál de las siguientes rectas es paralela a y = -4/5x - 3?", "opciones": ["y = -4/5x + 3", "y = 5/4x + 2", "y = 4/5x + 10", "y = -5/4x - 7"], "correcta_texto": "y = -4/5x + 3", "tiempo": 120},
    {"id": "A5", "mision": 1, "pregunta": "La recta y = 2/3x + 1 es perpendicular a la recta:", "opciones": ["y = 2/3x - 5", "y = 3/2x + 2", "y = -2/3x + 4", "y = -3/2x + 5"], "correcta_texto": "y = -3/2x + 5", "tiempo": 120},
    {"id": "A6", "mision": 1, "pregunta": "La recta con pendiente m = -5/4 y que pasa por el punto p:(4,2) cumple que tiene como ecuación:", "opciones": ["y = -4/5x + 5 pasa por (9,-2)", "y = -5/4x + 7 pasa por (8,-3)", "y = -5/4x + 7 pasa por (8,2)", "y = -4/5x + 5 pasa por (0,5)"], "correcta_texto": "y = -5/4x + 7 pasa por (8,-3)", "tiempo": 200},
    {"id": "A7", "mision": 2, "pregunta": "El horno inicia en 15°C y sube 10°C cada 3 minutos. La función es:", "opciones": ["y = 15x + 3/10", "y = 3/10x + 15", "y = 15x + 10/3", "y = 10/3x + 15"], "correcta_texto": "y = 10/3x + 15", "tiempo": 300},
    {"id": "A8", "mision": 2, "pregunta": "Un taxi cobra una tarifa fija de $7 más $2 por cada 3 km recorridos. ¿Cuánto costará un viaje de 15 km?", "opciones": ["$10", "$23", "$17", "$15"], "correcta_texto": "$17", "tiempo": 300},
    {"id": "A9", "mision": 2, "pregunta": "Tanque A: 2 min=10L, 8 min=40L. Tanque B: 1 min=50L, 11 min=10L. ¿A los cuántos minutos tienen la misma cantidad?", "opciones": ["4", "6", "8", "10"], "correcta_texto": "6", "tiempo": 360},
    {"id": "A10", "mision": 2, "pregunta": "Andrés tiene $150 y ahorra $50/sem. Beatriz tiene $950 y gasta $150/sem. ¿En qué semana igualan capital?", "opciones": ["2", "3", "4", "5"], "correcta_texto": "4", "tiempo": 360},

    # --- TEMA B ---
    {"id": "B1", "mision": 1, "pregunta": "Para la función que pasa por A=(-3, 5) y B=(3, 1), ¿cuál es la pendiente m y el corte b?", "opciones": ["m = 2/3, b = 3", "m = -2/3, b = 3", "m = -3/2, b = -3", "m = 3/2, b = 3"], "correcta_texto": "m = -2/3, b = 3", "tiempo": 240},
    {"id": "B2", "mision": 1, "pregunta": "Ecuación de la recta que pasa por A(-2, -5) y B(5, -7):", "opciones": ["y = -2/7x - 39/7", "y = 2/7x + 39/7", "y = -7/2x - 4", "y = 7/2x + 4"], "correcta_texto": "y = -2/7x - 39/7", "tiempo": 240},
    {"id": "B3", "mision": 1, "pregunta": "Recta por P(5, -2) con m = -4/5:", "opciones": ["y = -4/5x + 2", "y = -4/5x - 6", "y = 4/5x + 2", "y = -5/4x + 2"], "correcta_texto": "y = -4/5x + 2", "tiempo": 180},
    {"id": "B4", "mision": 1, "pregunta": "¿Cuál es paralela a y = 3/7x + 5?", "opciones": ["y = -3/7x + 5", "y = 7/3x - 1", "y = 3/7x - 8", "y = -7/3x + 2"], "correcta_texto": "y = 3/7x - 8", "tiempo": 120},
    {"id": "B5", "mision": 1, "pregunta": "Recta perpendicular a y = -5/2x - 4:", "opciones": ["y = 5/2x + 1", "y = 2/5x + 10", "y = -2/5x - 4", "y = -5/2x + 3"], "correcta_texto": "y = 2/5x + 10", "tiempo": 120},
    {"id": "B6", "mision": 1, "pregunta": "Pendiente m = 1/3 y pasa por P(6, 4):", "opciones": ["y = 1/3x + 2 y pasa por (0, 2)", "y = 3x - 2 y pasa por (1, 1)", "y = 1/3x + 4 y pasa por (3, 5)", "y = -1/3x + 2 y pasa por (6, 0)"], "correcta_texto": "y = 1/3x + 2 y pasa por (0, 2)", "tiempo": 200},
    {"id": "B7", "mision": 2, "pregunta": "Enfriador inicia a 20°C y baja 4°C cada 3 min. La función es:", "opciones": ["y = 3/4x + 20", "y = -4/3x + 20", "y = 4/3x - 20", "y = -3/4x + 20"], "correcta_texto": "y = -4/3x + 20", "tiempo": 300},
    {"id": "B8", "mision": 2, "pregunta": "Mensajería: $10 base + $3 por cada 4 km. ¿Costo por 20 km?", "opciones": ["$15", "$20", "$25", "$30"], "correcta_texto": "$25", "tiempo": 300},
    {"id": "B9", "mision": 2, "pregunta": "Contenedor A: 15L (+3/2 L/min). Contenedor B: 45L (-5/2 L/min). ¿Cuándo se igualan?", "opciones": ["6 minutos", "7.5 minutos", "10 minutos", "15 minutos"], "correcta_texto": "7.5 minutos", "tiempo": 360},
    {"id": "B10", "mision": 2, "pregunta": "Camilo: $400 (gasta $25/2 sem). Sara: $100 (ahorra $75/2 sem). ¿En qué semana igualan?", "opciones": ["Semana 4", "Semana 6", "Semana 8", "Semana 10"], "correcta_texto": "Semana 6", "tiempo": 360},

    # --- TEMA C ---
    {"id": "C1", "mision": 1, "pregunta": "Pasa por A=(-5, 7) y B=(5, 3), ¿Pendiente m y corte b?", "opciones": ["m = 2/5, b = 5", "m = -5/2, b = 5", "m = -2/5, b = 5", "m = 5/2, b = -5"], "correcta_texto": "m = -2/5, b = 5", "tiempo": 240},
    {"id": "C2", "mision": 1, "pregunta": "Ecuación de la recta por A(-3, 1) y B(6, 7):", "opciones": ["y = 2/3x + 3", "y = -2/3x + 3", "y = 3/2x - 1", "y = 2/3x - 3"], "correcta_texto": "y = 2/3x + 3", "tiempo": 240},
    {"id": "C3", "mision": 1, "pregunta": "Recta por P(-4, 2) con m = 3/4:", "opciones": ["y = 3/4x - 5", "y = 3/4x + 5", "y = -3/4x + 5", "y = 4/3x + 5"], "correcta_texto": "y = 3/4x + 5", "tiempo": 180},
    {"id": "C4", "mision": 1, "pregunta": "¿Cuál es paralela a y = -2/9x + 10?", "opciones": ["y = 9/2x + 10", "y = -2/9x - 4", "y = 2/9x + 4", "y = -9/2x + 1"], "correcta_texto": "y = -2/9x - 4", "tiempo": 120},
    {"id": "C5", "mision": 1, "pregunta": "Recta perpendicular a y = 7/3x - 2:", "opciones": ["y = -3/7x + 6", "y = 3/7x + 6", "y = -7/3x - 2", "y = 7/3x + 4"], "correcta_texto": "y = -3/7x + 6", "tiempo": 120},
    {"id": "C6", "mision": 1, "pregunta": "Pendiente m = -3/2 y pasa por P(4, -1):", "opciones": ["y = -3/2x + 5 y pasa por (0, 5)", "y = 3/2x - 7 y pasa por (2, -4)", "y = -3/2x + 5 y pasa por (2, 1)", "y = 2/3x + 1 y pasa por (3, 3)"], "correcta_texto": "y = -3/2x + 5 y pasa por (0, 5)", "tiempo": 200},
    {"id": "C7", "mision": 2, "pregunta": "Vehículo con 40L consume 5L cada 4 km. La función es:", "opciones": ["y = 4/5x + 40", "y = -5/4x + 40", "y = 5/4x - 40", "y = -4/5x + 40"], "correcta_texto": "y = -5/4x + 40", "tiempo": 300},
    {"id": "C8", "mision": 2, "pregunta": "Reparación: $15 visita + $5 cada 2 horas. ¿Costo por 7 horas?", "opciones": ["$30.0", "$32.5", "$35.0", "$17.5"], "correcta_texto": "$32.5", "tiempo": 300},
    {"id": "C9", "mision": 2, "pregunta": "Tanque A: 100L (-10/3 L/min). Tanque B: 20L (+10/3 L/min). ¿Cuándo se igualan?", "opciones": ["10 minutos", "12 minutos", "15 minutos", "18 minutos"], "correcta_texto": "12 minutos", "tiempo": 360},
    {"id": "C10", "mision": 2, "pregunta": "Marta: debe $600 (paga $40/3 sem). Luis: debe $1000 (paga $120/3 sem). ¿Semana de igualdad?", "opciones": ["Semana 12", "Semana 15", "Semana 18", "Semana 20"], "correcta_texto": "Semana 15", "tiempo": 360},

    # --- TEMA D ---
    {"id": "D1", "mision": 1, "pregunta": "Pasa por A=(-6, 1) y B=(6, 6), ¿Pendiente m y corte b?", "opciones": ["m = 5/12, b = 3.5", "m = -5/12, b = 3.5", "m = 12/5, b = -3", "m = 5/12, b = -3.5"], "correcta_texto": "m = 5/12, b = 3.5", "tiempo": 240},
    {"id": "D2", "mision": 1, "pregunta": "Ecuación de la recta por A(-4, 8) y B(2, -1):", "opciones": ["y = 3/2x + 2", "y = -3/2x + 2", "y = -2/3x + 2", "y = 3/2x - 2"], "correcta_texto": "y = -3/2x + 2", "tiempo": 240},
    {"id": "D3", "mision": 1, "pregunta": "Recta por P(3, -4) con m = -1/3:", "opciones": ["y = -1/3x - 3", "y = -1/3x + 3", "y = 1/3x - 3", "y = -3x - 3"], "correcta_texto": "y = -1/3x - 3", "tiempo": 180},
    {"id": "D4", "mision": 1, "pregunta": "¿Cuál es paralela a y = -5/6x - 1?", "opciones": ["y = 6/5x + 4", "y = 5/6x - 1", "y = -5/6x + 9", "y = -6/5x + 2"], "correcta_texto": "y = -5/6x + 9", "tiempo": 120},
    {"id": "D5", "mision": 1, "pregunta": "Recta perpendicular a y = -1/4x + 5:", "opciones": ["y = -4x + 2", "y = 1/4x - 5", "y = 4x - 8", "y = -4/1x + 3"], "correcta_texto": "y = 4x - 8", "tiempo": 120},
    {"id": "D6", "mision": 1, "pregunta": "Pendiente m = 4/5 y pasa por P(5, 7):", "opciones": ["y = 4/5x + 3 y pasa por (0, 3)", "y = -4/5x + 3 y pasa por (5, -1)", "y = 4/5x - 3 y pasa por (10, 5)", "y = 5/4x + 3 y pasa por (4, 8)"], "correcta_texto": "y = 4/5x + 3 y pasa por (0, 3)", "tiempo": 200},
    {"id": "D7", "mision": 2, "pregunta": "Depósito inicia con 80 gal y pierde 3 gal cada 2 horas. La función es:", "opciones": ["y = 3/2x + 80", "y = -2/3x + 80", "y = -3/2x + 80", "y = -3/2x - 80"], "correcta_texto": "y = -3/2x + 80", "tiempo": 300},
    {"id": "D8", "mision": 2, "pregunta": "Carpintero: $20 base + $15 cada 4 horas. ¿Costo por 12 horas?", "opciones": ["$45", "$65", "$35", "$70"], "correcta_texto": "$65", "tiempo": 300},
    {"id": "D9", "mision": 2, "pregunta": "Globo A: 10m (+5/4 m/s). Globo B: 40m (-7/4 m/s). ¿En qué segundo se igualan?", "opciones": ["8 segundos", "10 segundos", "12 segundos", "15 segundos"], "correcta_texto": "10 segundos", "tiempo": 360},
    {"id": "D10", "mision": 2, "pregunta": "Daniel: debe $500 (paga $30/2 sem). Sofía: debe $800 (paga $80/2 sem). ¿Semana de igualdad?", "opciones": ["Semana 6", "Semana 10", "Semana 12", "Semana 14"], "correcta_texto": "Semana 12", "tiempo": 360}
]

# --- LÓGICA DE STREAMLIT ---
# (Aquí sigue el resto del código del flujo de misiones, registro y mezcla de opciones 
# que ya construimos en el paso anterior, solo que ahora usará este BANCO_PREGUNTAS)


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
