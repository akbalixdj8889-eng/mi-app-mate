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

st.set_page_config(page_title="Reto Matemático Pro", page_icon="🔢")

# Función para enviar los datos a Google
def enviar_a_google(nombre, curso, nota, segundos):
    data = {
        ENTRY_NOMBRE: nombre,
        ENTRY_CURSO: curso,
        ENTRY_NOTA: nota,
        ENTRY_TIEMPO: f"{segundos}s"
    }
    try:
        requests.post(URL_FORM, data=data)
        return True
    except:
        return False

# --- PANTALLA DE INICIO ---
if 'estudiante' not in st.session_state:
    st.title("🚀 ¡Bienvenido al Reto!")
    nombre = st.text_input("Nombre completo:")
    curso = st.selectbox("Selecciona tu curso:", ["601", "602", "701", "702"]) # Puedes editarlos
    
    if st.button("Empezar Evaluación"):
        if nombre:
            st.session_state.estudiante = nombre
            st.session_state.curso = curso
            st.session_state.inicio_total = time.time()
            st.rerun()
        else:
            st.warning("Escribe tu nombre para continuar.")

# --- PANTALLA DE EXAMEN ---
else:
    st.write(f"Estudiante: **{st.session_state.estudiante}** | Curso: **{st.session_state.curso}**")
    
    if 'a' not in st.session_state:
        st.session_state.a = random.randint(2, 12)
        st.session_state.b = random.randint(1, 25)
        st.session_state.x_true = random.randint(1, 10)
        st.session_state.c = st.session_state.a * st.session_state.x_true + st.session_state.b

    st.subheader(f"Resuelve: {st.session_state.a}x + {st.session_state.b} = {st.session_state.c}")
    resp = st.number_input("¿Cuánto vale x?", step=1)

    if st.button("Enviar y Terminar"):
        tiempo_final = int(time.time() - st.session_state.inicio_total)
        resultado = "Correcto" if resp == st.session_state.x_true else f"Error (puso {resp})"
        
        exito = enviar_a_google(st.session_state.estudiante, st.session_state.curso, resultado, tiempo_final)
        
        if exito:
            st.success("✅ ¡Datos guardados! Ya puedes cerrar la app.")
            if resp == st.session_state.x_true:
                st.balloons()
        else:
            st.error("❌ Error de conexión al guardar. Avisa a tu profesor.")
            
        if st.button("Reiniciar"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# Bloqueo de trampa (onblur)
st.components.v1.html("""
    <script>
    window.onblur = function() {
        alert("¡Ojo! Detectamos que saliste de la app. El tiempo sigue corriendo.");
    };
    </script>
""", height=0)
