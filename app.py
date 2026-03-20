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

st.set_page_config(page_title="Examen Seguro", page_icon="🔒")

# --- ESTILOS PARA EVITAR COPIAR/PEGAR ---
st.markdown("""
    <style>
    input { -webkit-user-select: none; -moz-user-select: none; -ms-user-select: none; user-select: none; }
    .stNumberInput { pointer-events: auto; }
    </style>
""", unsafe_allow_html=True)

if 'inicio' not in st.session_state:
    st.session_state.inicio = None

def enviar(nombre, curso, nota, seg):
    payload = {ENTRY_NOMBRE: nombre, ENTRY_CURSO: curso, ENTRY_NOTA: nota, ENTRY_TIEMPO: f"{seg}s"}
    requests.post(URL_FORM, data=payload)

st.title("🛡️ Reto Matemático Anti-IA")

if not st.session_state.inicio:
    nom = st.text_input("Nombre:")
    cur = st.selectbox("Curso:", ["601", "701"])
    if st.button("INICIAR EXAMEN (Tienes 20 segundos)"):
        st.session_state.inicio = time.time()
        st.session_state.nom = nom
        st.session_state.cur = cur
        st.rerun()
else:
    # CÁLCULO DE TIEMPO
    transcurrido = int(time.time() - st.session_state.inicio)
    restante = 20 - transcurrido

    if restante <= 0:
        st.error("❌ ¡TIEMPO AGOTADO! El examen ha sido anulado por sospecha de consulta externa.")
        enviar(st.session_state.nom, st.session_state.cur, "ANULADO (Exceso de tiempo)", transcurrido)
        if st.button("Reintentar"):
            st.session_state.inicio = None
            st.rerun()
    else:
        st.metric("Tiempo restante", f"{restante}s")
        
        # Generar ejercicio (fijo durante la sesión)
        if 'num' not in st.session_state:
            st.session_state.a = random.randint(2, 9)
            st.session_state.x = random.randint(1, 10)
            st.session_state.res = st.session_state.a * st.session_state.x

        # MOSTRAR EJERCICIO COMO ENCABEZADO GRANDE (Más difícil de leer para algunas IAs simples)
        st.subheader(f"¿Cuánto vale X?")
        st.info(f"### {st.session_state.a} * X = {st.session_state.res}")
        
        ans = st.number_input("Escribe tu respuesta:", step=1, value=0)

        if st.button("ENTREGAR AHORA"):
            nota = "Correcto" if ans == st.session_state.x else f"Incorrecto (Puso {ans})"
            enviar(st.session_state.nom, st.session_state.cur, nota, transcurrido)
            st.success("¡Enviado con éxito!")
            st.session_state.inicio = None
            if st.button("Hacer otro"): st.rerun()
