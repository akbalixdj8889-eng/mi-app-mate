import streamlit as st
import random
import time
import requests

# --- CONFIGURACIÓN ---
URL_FORM = "https://docs.google.com/forms/d/e/1FAIpQLScin_I5blL_gwFbDP8vfjTz7SQj4BRZQ0_wI7rmJvXvNjkzzQ/formResponse"
ENTRY_NOMBRE = "entry.1544483154"
ENTRY_CURSO  = "entry.2027082892"
ENTRY_NOTA   = "entry.1011634935"
ENTRY_TIEMPO = "entry.1300499693"

st.set_page_config(page_title="Reto Matemático", page_icon="🔢")

# --- ESTADOS DE SESIÓN ---
if 'trampas' not in st.session_state:
    st.session_state.trampas = 0
if 'evaluando' not in st.session_state:
    st.session_state.evaluando = False

# --- DETECTOR DE TRAMPAS (JS MEJORADO) ---
# Usamos un ID único para que Streamlit no ignore el componente
js_detector = st.components.v1.html(
    f"""
    <html>
        <body>
            <script>
            var count = {st.session_state.trampas};
            window.parent.document.onvisibilitychange = function() {{
                if (window.parent.document.visibilityState === 'hidden') {{
                    count++;
                    window.parent.postMessage({{
                        type: 'streamlit:setComponentValue',
                        value: count
                    }}, '*');
                }}
            }};
            </script>
        </body>
    </html>
    """,
    height=0,
)

# Captura del valor con validación extra
if js_detector is not None:
    try:
        val = int(js_detector)
        if val > st.session_state.trampas:
            st.session_state.trampas = val
            st.rerun() # Forzamos recarga para mostrar el aviso
    except:
        pass

def enviar_a_google(nombre, curso, nota, segundos, trampas):
    nota_final = f"{nota} (Salió {trampas} veces)"
    data = {{ENTRY_NOMBRE: nombre, ENTRY_CURSO: curso, ENTRY_NOTA: nota_final, ENTRY_TIEMPO: f"{{segundos}}s"}}
    try:
        requests.post(URL_FORM, data=data, timeout=5)
    except:
        pass

st.title("🔢 Reto Matemático Blindado")

# --- FLUJO ---
if not st.session_state.evaluando:
    nombre = st.text_input("Nombre completo:")
    curso = st.selectbox("Curso:", ["601", "602", "701", "702"])
    if st.button("Empezar Reto"):
        if nombre:
            st.session_state.estudiante = nombre
            st.session_state.curso = curso
            st.session_state.inicio_total = time.time()
            st.session_state.evaluando = True
            st.rerun()
else:
    # Notificación de falta
    if st.session_state.trampas > 0:
        st.error(f"⚠️ ¡ALERTA! Has salido de la prueba {st.session_state.trampas} veces.")

    if 'a' not in st.session_state:
        st.session_state.a = random.randint(2, 12)
        st.session_state.b = random.randint(1, 20)
        st.session_state.x_true = random.randint(1, 10)
        st.session_state.c = st.session_state.a * st.session_state.x_true + st.session_state.b

    st.subheader(f"Resuelve: {st.session_state.a}x + {st.session_state.b} = {st.session_state.c}")
    resp = st.number_input("Valor de x:", step=1, value=0)

    if st.button("Enviar Finalizar"):
        tiempo = int(time.time() - st.session_state.inicio_total)
        res = "Correcto" if resp == st.session_state.x_true else f"Incorrecto (puso {resp})"
        
        enviar_a_google(st.session_state.estudiante, st.session_state.curso, res, tiempo, st.session_state.trampas)
        st.success(f"Registrado. Salidas detectadas: {st.session_state.trampas}")
        
        if st.button("Nuevo Ejercicio"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
