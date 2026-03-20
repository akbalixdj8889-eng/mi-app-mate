import streamlit as st
import random
import time
import requests
import matplotlib.pyplot as plt
import io
import numpy as np

# --- CONFIGURACIÓN DE GOOGLE (Mantén tus IDs iguales) ---
URL_FORM = "https://docs.google.com/forms/d/e/1FAIpQLScin_I5blL_gwFbDP8vfjTz7SQj4BRZQ0_wI7rmJvXvNjkzzQ/formResponse"
ENTRY_NOMBRE = "entry.1544483154"
ENTRY_CURSO  = "entry.2027082892"
ENTRY_NOTA   = "entry.1011634935"
ENTRY_TIEMPO = "entry.1300499693"

st.set_page_config(page_title="Reto Blindado v3", page_icon="🛡️")

# --- BLOQUEO DE COPIADO/PEGADO (CSS) ---
st.markdown("""
    <style>
    /* Deshabilitar selección de texto y menú contextual en toda la app */
    * {
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
    }
    /* Permitir interacción solo con el campo de entrada */
    .stNumberInput input {
        -webkit-user-select: auto !important;
        -moz-user-select: auto !important;
        -ms-user-select: auto !important;
        user-select: auto !important;
        pointer-events: auto !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZACIÓN DE VARIABLES ---
if 'evaluando' not in st.session_state:
    st.session_state.evaluando = False
if 'ejercicio_imagen' not in st.session_state:
    st.session_state.ejercicio_imagen = None

# --- FUNCIÓN MAESTRA: GENERAR EJERCICIO COMO IMAGEN BLINDADA ---
def generar_imagen_ejercicio(a, x_true, res):
    """Dibuja la ecuación en una imagen con ruido visual anti-OCR"""
    # Crear el lienzo gráfico (Fig) y los ejes (ax)
    fig, ax = plt.figure(figsize=(6, 2), dpi=100), plt.gca()
    
    # Texto de la ecuación
    texto_ecuacion = f"{a} * X = {res}"
    
    # Estilo del texto (Grande, negrita, azul oscuro)
    ax.text(0.5, 0.5, texto_ecuacion, fontsize=28, fontweight='bold',
            ha='center', va='center', color='#1f77b4', family='serif')
    
    # --- AÑADIR RUIDO VISUAL (Anti-IA) ---
    # Líneas aleatorias suaves que cruzan el texto
    for _ in range(3):
        ax.plot([random.random(), random.random()], [random.random(), random.random()], 
                color='gray', alpha=0.3, linewidth=1)
    
    # Puntos aleatorios (tipo arena)
    ax.scatter(np.random.rand(50), np.random.rand(50), color='gray', s=1, alpha=0.2)
    
    # Ocultar ejes, bordes y fondo
    ax.axis('off')
    plt.tight_layout()
    
    # Guardar la imagen en un búfer de memoria (no en disco)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1, transparent=True)
    buf.seek(0)
    plt.close() # Cerrar plot para liberar memoria
    return buf

# --- FUNCIÓN DE ENVÍO A GOOGLE SHEETS ---
def enviar_a_google(nombre, curso, nota, segundos):
    payload = {
        ENTRY_NOMBRE: nombre,
        ENTRY_CURSO: curso,
        ENTRY_NOTA: nota,
        ENTRY_TIEMPO: f"{segundos}s"
    }
    try:
        requests.post(URL_FORM, data=payload, timeout=5)
    except:
        st.error("Error de red al guardar el resultado.")

st.title("🛡️ Reto Matemático Blindado v3")
st.write("---")

# --- FLUJO DE LA APLICACIÓN ---
if not st.session_state.evaluando:
    # --- PANTALLA DE REGISTRO ---
    nombre = st.text_input("Ingresa tu Nombre Completo:")
    curso = st.selectbox("Selecciona tu Curso:", ["601", "701", "801"])
    
    st.warning("⏱️ Tienes un límite estricto de **20 segundos** para resolver el reto.")
    st.info("⚠️ La imagen del ejercicio es dinámica y anti-copia. No intentes capturarla.")
    
    if st.button("COMENZAR EXAMEN AHORA"):
        if nombre:
            # Inicializar datos del reto
            st.session_state.estudiante = nombre
            st.session_state.curso = curso
            st.session_state.inicio_total = time.time()
            st.session_state.evaluando = True
            
            # Generar el ejercicio internamente
            st.session_state.a = random.randint(3, 9)
            st.session_state.x_true = random.randint(2, 10)
            st.session_state.res = st.session_state.a * st.session_state.x_true
            
            # Generar y guardar la imagen blindada en sesión
            st.session_state.ejercicio_imagen = generar_imagen_ejercicio(
                st.session_state.a, st.session_state.x_true, st.session_state.res
            )
            
            st.rerun()
        else:
            st.warning("Escribe tu nombre para empezar.")
else:
    # --- PANTALLA DE EXAMEN ACTIVO ---
    
    # 1. CÁLCULO DE TIEMPO (Cronómetro de Anulación)
    tiempo_transcurrido = int(time.time() - st.session_state.inicio_total)
    tiempo_limite = 20 # Segundos estrictos
    tiempo_restante = tiempo_limite - tiempo_transcurrido
    
    if tiempo_restante <= 0:
        # --- CASO: TIEMPO AGOTADO (Castigo y Anulación) ---
        st.error(f"❌ ¡EXAMEN ANULADO! Has superado el tiempo límite de {tiempo_limite} segundos.")
        st.write("Esto sucede por sospecha de consulta externa (capturas, IAs, etc.).")
        
        # Enviar reporte de anulación
        enviar_a_google(st.session_state.estudiante, st.session_state.curso, "ANULADO (Exceso de Tiempo)", tiempo_transcurrido)
        
        # Limpiar sesión para reintentar
        if st.button("Volver al Inicio"):
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.rerun()
    else:
        # --- CASO: EXAMEN ACTIVO ---
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"Estudiante: **{st.session_state.estudiante}** | Curso: **{st.session_state.curso}**")
        with col2:
            st.metric("Tiempo Restante", f"{tiempo_restante}s", delta_color="inverse")
        
        st.write("---")
        
        # 2. MOSTRAR EL EJERCICIO COMO IMAGEN BLINDADA
        st.subheader("Calcula el valor de X mentalmente:")
        st.image(st.session_state.ejercicio_imagen, use_column_width=False, width=450)
        
        st.write("---")
        
        # 3. CAMPO DE RESPUESTA Y ENTREGA
        respuesta_estudiante = st.number_input("Escribe el número de la respuesta (X):", step=1, value=0)
        
        if st.button("ENVIAR RESPUESTA FINAL"):
            final_time = int(time.time() - st.session_state.inicio_total)
            
            # Validar respuesta
            es_correcto = (respuesta_estudiante == st.session_state.x_true)
            resultado_texto = "Correcto" if es_correcto else f"Incorrecto (Puso {respuesta_estudiante})"
            
            # Enviar a Google Sheets
            enviar_a_google(st.session_state.estudiante, st.session_state.curso, resultado_texto, final_time)
            
            # Feedback visual y reinicio
            if es_correcto:
                st.success(f"✅ ¡Correcto! Datos enviados a tu profesor en {final_time} segundos.")
                st.balloons()
            else:
                st.error(f"❌ Incorrecto. La respuesta era {st.session_state.x_true}. Datos enviados.")
            
            # Botón para limpiar sesión y hacer otro
            if st.button("Finalizar y Cerrar"):
                for key in list(st.session_state.keys()): del st.session_state[key]
                st.rerun()

# Bloqueo extra por JavaScript (por si acaso el navegador lo permite)
st.components.v1.html("""
    <script>
    document.addEventListener('contextmenu', event => event.preventDefault()); // Bloquear clic derecho
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && (e.key === 'c' || e.key === 'v' || e.key === 'p' || e.key === 's')) {
            e.preventDefault(); // Bloquear Ctrl+C, Ctrl+V, etc.
        }
    });
    </script>
""", height=0)
