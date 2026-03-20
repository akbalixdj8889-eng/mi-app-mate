import streamlit as st
import random
import time
import requests
from streamlit_autorefresh import st_autorefresh
# --- CONFIGURACIÓN (Mantén tus IDs iguales) ---
URL_FORM = "https://docs.google.com/forms/d/e/1FAIpQLScin_I5blL_gwFbDP8vfjTz7SQj4BRZQ0_wI7rmJvXvNjkzzQ/formResponse"
ENTRY_NOMBRE = "entry.1544483154"
ENTRY_CURSO  = "entry.2027082892"
ENTRY_NOTA   = "entry.1011634935"
ENTRY_TIEMPO = "entry.1300499693"

# --- INICIALIZACIÓN DE VARIABLES DE SESIÓN ---
if 'trampas' not in st.session_state:
    st.session_state.trampas = 0

# --- FUNCIÓN DE ENVÍO ---
def enviar_a_google(nombre, curso, nota, segundos, trampas):
    # Añadimos las trampas al reporte de nota
    nota_final = f"{nota} (Salió de la app {trampas} veces)"
    data = {
        ENTRY_NOMBRE: nombre,
        ENTRY_CURSO: curso,
        ENTRY_NOTA: nota_final,
        ENTRY_TIEMPO: f"{segundos}s"
    }
    requests.post(URL_FORM, data=data)

st.title("🔢 Reto Matemático Blindado")



# --- LÓGICA DE DETECCIÓN (Copia esto sobre tu bloque de JS actual) ---
# Usamos un componente que "escucha" el valor de JavaScript
from streamlit_gsheets import GSheetsConnection # No la necesitas, ignora esto

# Código JavaScript para detectar desenfoque (blur)
# El secreto es usar st.components.v1.html con un pequeño truco de 'st_bridge'
if 'trampas' not in st.session_state:
    st.session_state.trampas = 0

# Este bloque captura el evento de salir de la pestaña
components_value = st.components.v1.html(
    """
    <script>
    var count = 0;
    // Función que se ejecuta al salir de la pestaña
    window.onblur = function() {
        count++;
        // Enviamos el dato a la aplicación de Streamlit
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: count
        }, '*');
    };
    </script>
    """,
    height=0,
)

# --- ACTUALIZAR EL CONTADOR ---
# Si el componente detecta un cambio, lo sumamos al estado de la sesión
if components_value is not None:
    st.session_state.trampas = components_value



# --- PANTALLA DE INICIO ---
if 'estudiante' not in st.session_state:
    nombre = st.text_input("Nombre completo:")
    curso = st.selectbox("Curso:", ["601", "602", "701", "702"])
    if st.button("Empezar"):
        if nombre:
            st.session_state.estudiante = nombre
            st.session_state.curso = curso
            st.session_state.inicio_total = time.time()
            st.rerun()
else:
    # Mostramos advertencia si ha salido
    if st.session_state.trampas > 0:
        st.warning(f"⚠️ Atención: Has salido de la aplicación {st.session_state.trampas} veces. Esto se reportará al profesor.")

    # Generación de ejercicio (igual al anterior)
    if 'a' not in st.session_state:
        st.session_state.a = random.randint(2, 12); st.session_state.b = random.randint(1, 20)
        st.session_state.x_true = random.randint(1, 10)
        st.session_state.c = st.session_state.a * st.session_state.x_true + st.session_state.b

    st.subheader(f"Resuelve: {st.session_state.a}x + {st.session_state.b} = {st.session_state.c}")
    resp = st.number_input("x =", step=1)

    if st.button("Enviar"):
        tiempo = int(time.time() - st.session_state.inicio_total)
        res = "Correcto" if resp == st.session_state.x_true else "Incorrecto"
        
        enviar_a_google(st.session_state.estudiante, st.session_state.curso, res, tiempo, st.session_state.trampas)
        st.success("Enviado. Revisa tu Excel.")
        
        if st.button("Reiniciar"):
            st.session_state.clear()
            st.rerun()
