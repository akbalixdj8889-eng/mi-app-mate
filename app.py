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

# --- INICIALIZACIÓN DE ESTADOS ---
if 'trampas' not in st.session_state:
    st.session_state.trampas = 0
if 'estudiante' not in st.session_state:
    st.session_state.evaluando = False

def enviar_a_google(nombre, curso, nota, segundos, trampas):
    nota_final = f"{nota} (Salió {trampas} veces)"
    data = {ENTRY_NOMBRE: nombre, ENTRY_CURSO: curso, ENTRY_NOTA: nota_final, ENTRY_TIEMPO: f"{segundos}s"}
    requests.post(URL_FORM, data=data)

st.title("🔢 Reto Matemático Blindado")

# --- DETECTOR DE TRAMPAS (JS mejorado) ---
# Este componente captura las salidas y las guarda en 'components_value'
components_value = st.components.v1.html(
    """
    <script>
    var count = 0;
    window.onblur = function() {
        count++;
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: count
        }, '*');
    };
    </script>
    """,
    height=0,
)

# Actualizamos el contador de la sesión si el JS detecta algo
if components_value:
    st.session_state.trampas = components_value

# --- FLUJO DE LA APP ---
if not st.session_state.evaluando:
    nombre = st.text_input("Nombre completo:")
    curso = st.selectbox("Curso:", ["601", "602", "701", "702"])
    if st.button("Empezar"):
        if nombre:
            st.session_state.estudiante = nombre
            st.session_state.curso = curso
            st.session_state.inicio_total = time.time()
            st.session_state.evaluando = True
            st.rerun()
else:
    # Mostrar advertencia en tiempo real
    if st.session_state.trampas > 0:
        st.error(f"⚠️ Has salido de la app {st.session_state.trampas} veces. ¡Sigue concentrado!")

    # Generación de ejercicio
    if 'a' not in st.session_state:
        st.session_state.a = random.randint(2, 12)
        st.session_state.b = random.randint(1, 20)
        st.session_state.x_true = random.randint(1, 10)
        st.session_state.c = st.session_state.a * st.session_state.x_true + st.session_state.b

    st.subheader(f"Resuelve para x: {st.session_state.a}x + {st.session_state.b} = {st.session_state.c}")
    resp = st.number_input("Tu respuesta:", step=1, value=0)

    if st.button("Enviar Respuesta Final"):
        tiempo = int(time.time() - st.session_state.inicio_total)
        res = "Correcto" if resp == st.session_state.x_true else f"Incorrecto (puso {resp})"
        
        enviar_a_google(st.session_state.estudiante, st.session_state.curso, res, tiempo, st.session_state.trampas)
        
        st.success(f"¡Hecho! Se registraron {st.session_state.trampas} salidas de pantalla.")
        st.balloons()
        
        if st.button("Hacer otro"):
            # Limpiar todo para reiniciar
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
