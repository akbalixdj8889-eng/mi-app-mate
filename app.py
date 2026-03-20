import streamlit as st
import random
import time

# Configuración de la página para que parezca una App móvil
st.set_page_config(page_title="Reto Matemático", page_icon="🔢")

st.title("⚡ Reto de Ecuaciones")
st.write("Resuelve antes de que se acabe el tiempo. ¡Si sales de la app, pierdes!")

# 1. Generador de parámetros aleatorios (Como en Moodle)
if 'a' not in st.session_state:
    st.session_state.a = random.randint(2, 10)
    st.session_state.b = random.randint(1, 20)
    st.session_state.x_true = random.randint(1, 10)
    # Generamos la ecuación: ax + b = c  => c = a*x + b
    st.session_state.c = st.session_state.a * st.session_state.x_true + st.session_state.b
    st.session_state.start_time = time.time()

# 2. Lógica del Cronómetro (60 segundos)
duracion = 60
tiempo_transcurrido = time.time() - st.session_state.start_time
tiempo_restante = max(0, duracion - int(tiempo_transcurrido))

if tiempo_restante > 0:
    st.metric(label="Tiempo restante", value=f"{tiempo_restante}s")
    
    # Mostrar la ecuación de forma visual
    st.subheader(f"Resuelve para $x$:")
    st.info(f"## {st.session_state.a}x + {st.session_state.b} = {st.session_state.c}")

    # Entrada de respuesta
    respuesta = st.number_input("Tu respuesta:", step=1, key="input_usuario")

    if st.button("Enviar Respuesta"):
        if respuesta == st.session_state.x_true:
            st.success(f"¡Correcto! Lo lograste en {int(tiempo_transcurrido)} segundos.")
            st.balloons()
            # Botón para reiniciar
            if st.button("Siguiente ejercicio"):
                del st.session_state.a
                st.rerun()
        else:
            st.error("Incorrecto. Intenta de nuevo (el tiempo sigue corriendo).")
else:
    st.error("¡Se acabó el tiempo! La IA fue más lenta que el reloj, pero tú también.")
    if st.button("Reintentar con otro ejercicio"):
        del st.session_state.a
        st.rerun()

# 3. Nota de seguridad (Detección de cambio de pestaña básica)
st.components.v1.html("""
    <script>
    window.onblur = function() {
        alert("¡Cuidado! Se ha detectado que saliste de la aplicación. Esto quedará registrado.");
    };
    </script>
""", height=0)
