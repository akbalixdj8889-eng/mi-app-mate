#codigo corregido
# Parte 1: Importaciones, Configuración de Página y Estilos CSS

import streamlit as st
import random
import time
import requests
import matplotlib.pyplot as plt
import io

# --- 1. Configuración de la pestaña del navegador y disposición de la página ---
st.set_page_config(
    page_title="Math Quest Pro",
    page_icon="⚡",
    layout="centered",  # Alinea el contenido al centro
    initial_sidebar_state="collapsed" # Oculta la barra lateral por defecto
)

# --- 2. CSS REFORZADO (ESTILO Y VISIBILIDAD) ---
st.markdown("""
    <style>
    /* Fondo degradado para toda la app */
    .stApp {
        background: linear-gradient(135deg, #461a42 0%, #2d0b2a 100%);
        overflow: hidden; /* Evita scrollbars innecesarias si el contenido es muy grande */
    }
    
    /* Panel de Estado Superior (Nombre, Aciertos, etc.) */
    .status-panel {
        background-color: white;
        border-radius: 50px;
        padding: 10px 20px; /* Añadimos padding lateral */
        text-align: center;
        color: #461a42;
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 15px; /* Más espacio debajo */
        box-shadow: 0 4px 8px rgba(0,0,0,0.2); /* Sombra sutil */
    }

    /* Contenedor y Barra de Energía (Tiempo) */
    .energy-container {
        width: 100%;
        background-color: rgba(255,255,255,0.2);
        border-radius: 10px;
        margin-bottom: 25px; /* Más espacio debajo */
        overflow: hidden; /* Para que la barra interna respete el borde redondeado */
    }
    .energy-bar {
        height: 12px;
        background: #ff4b4b; /* Rojo vibrante para la barra de tiempo */
        border-radius: 10px; /* Asegura que la barra interna también tenga bordes redondeados */
        transition: width 0.1s linear; /* Transición suave al actualizar */
    }

    /* FORZAR VISIBILIDAD DE OPCIONES A, B, C, D */
    div[data-testid="stRadio"] label p {
        color: white !important;
        font-size: 1.3rem !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 2px black; /* Sombra de texto para mejor legibilidad */
    }
    div[data-testid="stRadio"] label {
        margin-right: 20px; /* Espacio entre opciones */
    }
    
    /* Etiquetas generales de texto en Markdown */
    .stMarkdown p {
        color: white !important;
        font-weight: bold;
        line-height: 1.6; /* Mejor interlineado */
    }
     .stMarkdown h2 { /* Estilo para títulos como "Resultado Final" */
        color: white !important;
        font-weight: bold;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    /* Tarjeta blanca donde vive la imagen de la pregunta */
    .question-card {
        background-color: white;
        padding: 20px; /* Más padding interno */
        border-radius: 25px; /* Bordes más curvos */
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3); /* Sombra más pronunciada */
        transition: all 0.3s ease; /* Transición suave al interactuar */
    }
    .question-card:hover {
        box-shadow: 0 6px 16px rgba(0,0,0,0.4); /* Sombra más intensa al pasar el ratón */
    }
    
    /* Estilo para los botones generales */
    .stButton>button {
        border-radius: 15px; /* Bordes más curvos */
        font-weight: bold;
        padding: 10px 20px; /* Padding interno del botón */
        font-size: 1.1rem;
        border: none; /* Sin borde por defecto */
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #ff4b4b !important; /* Rojo vibrante al pasar el ratón */
        color: white !important;
        box-shadow: 0 2px 6px rgba(255,75,75,0.4);
    }

    /* Estilo específico para el botón de ENVIAR RESPUESTA */
     button[kind="primary"] { /* Streamlit usa 'primary' para botones principales */
        background-color: #ff4b4b !important;
        color: white !important;
    }
    button[kind="primary"]:hover {
        background-color: #e53e3e !important; /* Un rojo más oscuro al pasar el ratón */
    }

    /* Estilo para mensajes de Toast */
    .stToast div>span {
        font-size: 1.1rem !important;
        text-shadow: 1px 1px 2px black;
    }

    /* Ajustes para mantener la imagen centrada si es necesario */
    .stImage {
        display: block;
        margin: 0 auto;
    }

    /* Estilo para el botón de 50/50 */
    div[data-testid="stButton"] button:contains("50/50") {
        background-color: #fbbf24 !important; /* Color amarillo/naranja */
        color: #2d0b2a !important;
    }
     div[data-testid="stButton"] button:contains("50/50"):hover {
        background-color: #e6a23f !important; /* Naranja más oscuro al pasar el ratón */
    }

    /* --- ESTILOS PARA LA PANTALLA DE REGISTRO --- */
    .input-container {
        /* Estilos para el contenedor general del registro */
        padding-bottom: 0; 
    }

    .registration-footer {
        height: 2px; /* Grosor de la línea */
        background-color: #3a0ca3; /* Color de la barra decorativa */
        margin-top: 20px; 
        margin-bottom: 0px; 
        border-radius: 5px; 
        width: 100%; 
        display: block; 
    }

    /* Añadimos un estilo base para todos los selectbox (dropdown) */
    .st-bf-dropdown { 
        background-color: white; 
        border-radius: 15px; 
        border: 1px solid #ccc; 
        padding: 10px;
    }
     /* Estilo para los elementos del selectbox */
    div[data-testid="stSelectbox"] .stSelectbox div[data-baseweb="select-element"] div[role="button"] {
         border-radius: 15px !important; 
         background-color: white;
         border: 1px solid #ccc;
    }
     div[data-testid="stSelectbox"] .stSelectbox div[data-baseweb="select-element"] div[role="button"] button {
         border-radius: 15px !important; 
     }

    </style>
    """, unsafe_allow_html=True)

# --- 3. Función para crear imágenes desde texto (para preguntas y opciones) ---
# La mantendremos aquí en la Parte 1 para que sea accesible globalmente.
def crear_imagen(texto, opciones, ocultas=[], idx_pregunta=None, id_pregunta=None):
    """
    Genera una imagen con texto, manejando opciones ocultas y evitando caracteres especiales
    que causen distorsión en el renderizado.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('white') # Fondo blanco para la imagen

    finales_render = []
    for opt_completo in opciones: # opt_completo es algo como "A) 65 (moneda)"
        letra_opcion = opt_completo[0] # Extrae la letra (ej. "A")
        
        if letra_opcion in ocultas and idx_pregunta is not None:
            finales_render.append(f"{letra_opcion} [ ELIMINADA ]")
        else:
            # Limpieza del texto para la visualización en Matplotlib.
            texto_limpio_opcion = opt_completo.replace('$', ' ').replace('(moneda)', ' ').replace('(', '[').replace(')', ']') 
            finales_render.append(texto_limpio_opcion)

    cuerpo_final = f"{texto}\n\n" + "\n".join(finales_render)

    size_fuente = 16 if len(cuerpo_final) < 200 else 14

    # Limpieza final del texto
    cuerpo_renderizado = cuerpo_final.replace('$', ' ').replace('(moneda)', ' ') 

    ax.text(0.05, 0.9, cuerpo_renderizado,
            fontsize=size_fuente,
            fontweight='bold',
            wrap=True,
            va='top',
            ha='left',
            color='#2d0b2a', 
            family='sans-serif', 
            linespacing=1.6)

    ax.axis('off') # Ocultamos los ejes de la gráfica

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=120)
    plt.close(fig) 
    buf.seek(0)
    return buf

# ----- FIN DE LA PARTE 1 -----# ----- FIN DE LA PARTE 1 -----

# Parte 2: Banco de Preguntas y Inicialización del Estado

# --- 3. BANCO DE PREGUNTAS CON CORRECCIONES Y HUMANIZACIÓN ---
# Se inicializa el banco de preguntas si no existe en el session_state
if 'banco_completo' not in st.session_state:
    st.session_state.banco_completo = [
        # ================= TEMA A =================
        # Preguntas sobre pendiente, intercepto y ecuaciones de la recta
        {"id": "A1", "mision": 1, "pregunta": "Un dron de vigilancia vuela en línea recta pasando por A=(-4,8) y B=(4,2). ¿Cuál es su pendiente (m) y su altura inicial (b)?", "opciones": ["m = 5, b = -3/4", "m = 3/4, b = -5", "m = -3/4, b = -5", "m = -3/4, b = 5"], "correcta_texto": "m = -3/4, b = 5", "t_max": 275},
        {"id": "A2", "mision": 1, "pregunta": "En un mapa de coordenadas, una carretera une A(1, 3) con B(2, 10). ¿Cuál es la ecuación que describe esta ruta?", "opciones": ["y = 3/7x + 4", "y = 2/7x - 4", "y = -2/7x - 4", "y = 7x - 4"], "correcta_texto": "y = 7x - 4", "t_max": 275},
        {"id": "A3", "mision": 1, "pregunta": "Un rayo láser se dispara desde P(-6, 2) con una inclinación m = -2/3. ¿Cuál es su fórmula de trayectoria?", "opciones": ["y = -2/3x - 2", "y = -2/3x - 3", "y = -3/2x - 3", "y = -3/2x - 2"], "correcta_texto": "y = -2/3x - 2", "t_max": 275},
        {"id": "A4", "mision": 1, "pregunta": "La trayectoria de un barco es y = -4/5x - 3. ¿Cuál de estas rutas es PARALELA a la del barco?", "opciones": ["y = -4/5x + 3", "y = 5/4x + 2", "y = 4/5x + 10", "y = -5/4x - 7"], "correcta_texto": "y = -4/5x + 3", "t_max": 260},
        {"id": "A5", "mision": 1, "pregunta": "Para cruzar un río de forma PERPENDICULAR a la corriente (y = 2/3x + 1), ¿qué trayectoria debe seguir el bote?", "opciones": ["y = 2/3x - 5", "y = 3/2x + 2", "y = -2/3x + 4", "y = -3/2x + 5"], "correcta_texto": "y = -3/2x + 5", "t_max": 260},
        # Pregunta con formato numérico para comparar
        {"id": "A6", "mision": 1, "pregunta": "Una pendiente de m = -5/4 pasa por el punto (4,2). ¿Qué ecuación la representa y por qué otro punto pasa?", "opciones": ["y = -4/5x + 5 (9,-2)", "y = -5/4x + 7 (8,-3)", "y = -5/4x + 7 (8,2)", "y = -4/5x + 5 (0,5)"], "correcta_texto": "y = -5/4x + 7 (8,-3)", "t_max": 280},
        # Preguntas aplicadas a problemas de la vida real (Misión 2)
        {"id": "A7", "mision": 2, "pregunta": "Un horno inicia a 15°C y sube 10°C cada 3 min. ¿Qué función representa su temperatura 'y' tras 'x' minutos?", "opciones": ["y = 15x + 3/10", "y = 3/10x + 15", "y = 10/3x + 15", "y = 3/10x + 15"], "correcta_texto": "y = 10/3x + 15", "t_max": 290},
        {"id": "A8", "mision": 2, "pregunta": "Un taxi cobra (pesos)7 de base y (pesos)2 por cada 3 km. ¿Cuál es el costo total por un viaje de 15 km?", "opciones": ["(pesos)10", "(pesos)23", "(pesos)17", "(pesos)15"], "correcta_texto": "(pesos)17", "t_max": 290},
        {"id": "A9", "mision": 2, "pregunta": "Tanque A (en 2 min tiene 10L, en 8 min tiene 40L). Tanque B (en 1 min tiene 50L, en 11 min tiene 10L). ¿En qué minuto se igualan sus niveles?", "opciones": ["4", "6", "8", "10"], "correcta_texto": "6", "t_max": 290},
        {"id": "A10", "mision": 2, "pregunta": "Andrés tiene (pesos)150 y ahorra (pesos)50 por semana. Beatriz tiene (pesos)950 y gasta (pesos)150 por semana. ¿En qué semana tendrán lo mismo?", "opciones": ["2", "3", "4", "5"], "correcta_texto": "4", "t_max": 290},

        # ================= TEMA B =================
        # Más ejemplos de cálculo de pendiente e intercepto
        {"id": "B1", "mision": 1, "pregunta": "Una rampa pasa por A=(-3, 5) y B=(3, 1). Calcula su pendiente (m) y su punto de corte (b):", "opciones": ["m = 2/3, b = 3", "m = -2/3, b = 3", "m = -3/2, b = -3", "m = 3/2, b = 3"], "correcta_texto": "m = -2/3, b = 3", "t_max": 275},
        {"id": "B2", "mision": 1, "pregunta": "Halla la ecuación de la recta que une los puntos A(-2, -5) y B(5, -7):", "opciones": ["y = -2/7x - 39/7", "y = 2/7x + 39/7", "y = -7/2x - 4", "y = 7/2x + 4"], "correcta_texto": "y = -2/7x - 39/7", "t_max": 275},
        {"id": "B3", "mision": 1, "pregunta": "Una antena transmite desde P(5, -2) con m = -4/5. ¿Cuál es su modelo matemático (ecuación de la recta)?", "opciones": ["y = -4/5x + 2", "y = -4/5x - 2", "y = 4/5x + 2", "y = -5/4x + 2"], "correcta_texto": "y = -4/5x + 2", "t_max": 275},
        {"id": "B4", "mision": 1, "pregunta": "Si una cerca sigue la línea y = 3/7x + 5, ¿cuál de estas opciones representa una cerca PARALELA?", "opciones": ["y = -3/7x + 5", "y = 7/3x - 1", "y = 3/7x - 8", "y = -7/3x + 2"], "correcta_texto": "y = 3/7x - 8", "t_max": 260},
        {"id": "B5", "mision": 1, "pregunta": "Una tubería (y = -5/2x - 4) debe cruzarse con otra de forma PERPENDICULAR. ¿Cuál es la ecuación de la segunda tubería?", "opciones": ["y = 5/2x + 1", "y = 2/5x + 10", "y = -2/5x - 4", "y = -5/2x + 3"], "correcta_texto": "y = 2/5x + 4", "t_max": 260},
        {"id": "B6", "mision": 1, "pregunta": "Halla la recta con m = 1/3 que pasa por P(6, 4) y identifica otro punto por donde pase:", "opciones": ["y = 1/3x + 2  Punto (0, 2)", "y = 3x - 2 Punto (1, 1)", "y = 1/3x + 4 Punto (3, 5)", "y = -1/3x + 2 Punto (6, 0)"], "correcta_texto": "y = 1/3x + 2  Punto (0, 2)", "t_max": 280},
        # Aplicaciones de ecuaciones lineales (Misión 2)
        {"id": "B7", "mision": 2, "pregunta": "Un enfriador está a 20°C y baja 4°C cada 3 min. ¿Qué función describe su temperatura tras 'x' minutos?", "opciones": ["y = 3/4x + 20", "y = -4/3x + 20", "y = 4/3x - 20", "y = -3/4x + 20"], "correcta_texto": "y = -4/3x + 20", "t_max": 290},
        {"id": "B8", "mision": 2, "pregunta": "Mensajería: (pesos)10 de cargo básico más (pesos)3 por cada 4 km recorridos. ¿Cuánto cuesta un envío a 20 km?", "opciones": ["(pesos)15", "(pesos)20", "(pesos)25", "(pesos)30"], "correcta_texto": "(pesos)25", "t_max": 290},
        {"id": "B9", "mision": 2, "pregunta": "Tanque A (15L inicial, sube 3L c/2 min). Tanque B (45L inicial, baja 5L c/2 min). ¿En qué minuto tienen igual nivel?", "opciones": ["6", "7.5", "10", "15"], "correcta_texto": "7.5", "t_max": 290},
        {"id": "B10", "mision": 2, "pregunta": "Camilo tiene (pesos)400 y gasta (pesos)25 cada 2 semanas. Sara tiene (pesos)100 y ahorra (pesos)75 cada 2 semanas. ¿En qué semana se igualan sus ahorros?", "opciones": ["2", "3", "4", "5"], "correcta_texto": "4", "t_max": 290},

        # ================= TEMA C =================
        # Más ejercicios de pendiente, intercepto y ecuaciones de la recta
        {"id": "C1", "mision": 1, "pregunta": "Una tirolesa une A=(-5, 7) y B=(5, 3). Halla su pendiente (m) y su punto de corte con el eje Y (b):", "opciones": ["m = 2/5, b = 5", "m = -5/2, b = 5", "m = -2/5, b = 5", "m = 5/2, b = -5"], "correcta_texto": "m = -2/5, b = 5", "t_max": 275},
        {"id": "C2", "mision": 1, "pregunta": "Determina la ecuación de la recta que pasa por los puntos de control A(-3, 1) y B(6, 7):", "opciones": ["y = 2/3x + 3", "y = -2/3x + 3", "y = 3/2x - 1", "y = 2/3x - 3"], "correcta_texto": "y = 2/3x + 3", "t_max": 275},
        {"id": "C3", "mision": 1, "pregunta": "Desde P(3, -4) sale un cable con pendiente m = -1/3. ¿Cuál es su ecuación (y = mx + b)?", "opciones": ["y = -1/3x - 3", "y = -1/3x + 3", "y = 1/3x - 3", "y = -3x - 3"], "correcta_texto": "y = -1/3x - 3", "t_max": 275},
        {"id": "C4", "mision": 1, "pregunta": "Una pista digital es y = -2/9x + 10. ¿Cuál de estas pistas es PARALELA?", "opciones": ["y = 9/2x + 10", "y = -2/9x - 4", "y = 2/9x + 4", "y = -9/2x + 1"], "correcta_texto": "y = -2/9x - 4", "t_max": 260},
        {"id": "C5", "mision": 1, "pregunta": "Una viga (y = 7/3x - 2) debe sostenerse con otra PERPENDICULAR. ¿Qué ecuación tiene la segunda viga?", "opciones": ["y = -3/7x + 6", "y = 3/7x + 6", "y = -7/3x - 2", "y = 7/3x + 4"], "correcta_texto": "y = -3/7x + 6", "t_max": 260},
        {"id": "C6", "mision": 1, "pregunta": "Halla la recta con m = -3/2 que pasa por P(4, -1) y señala su punto de corte con el eje Y:", "opciones": ["y = -3/2x + 5 (Corte en 5)", "y = 3/2x - 7 (Corte en -7)", "y = -3/2x - 1 (Corte en -1)", "y = 2/3x + 1 (Corte en 1)"], "correcta_texto": "y = -3/2x + 5 (Corte en 5)", "t_max": 280},
        # Problemas de tasas de cambio y comparación lineal (Misión 2)
        {"id": "C7", "mision": 2, "pregunta": "Un vehículo con 40L de combustible consume 5L cada 4 km. ¿Qué función modela el combustible restante (y) según los km recorridos (x)?", "opciones": ["y = 4/5x + 40", "y = -5/4x + 40", "y = 5/4x - 40", "y = -4/5x + 40"], "correcta_texto": "y = -5/4x + 40", "t_max": 290},
        {"id": "C8", "mision": 2, "pregunta": "Un servicio técnico cobra (pesos)15 base y (pesos)5 por cada 2 horas de labor. ¿Cuánto cuesta una reparación de 7 horas?", "opciones": ["(pesos)30.0", "(pesos)32.5", "(pesos)35.0", "(pesos)17.5"], "correcta_texto": "(pesos)32.5", "t_max": 290},
        {"id": "C9", "mision": 2, "pregunta": "Tanque A (100L inicial, pierde 10L c/3 min). Tanque B (20L inicial, gana 10L c/3 min). ¿En qué minuto se cruzan sus niveles?", "opciones": ["10", "12", "15", "18"], "correcta_texto": "12", "t_max": 290},
        {"id": "C10", "mision": 2, "pregunta": "Marta tiene (pesos)600 y gasta (pesos)40 cada 3 semanas. Luis tiene (pesos)1000 y gasta (pesos)120 cada 3 semanas. ¿En qué semana tendrán lo mismo?", "opciones": ["Semana 12", "Semana 15", "Semana 18", "Semana 20"], "correcta_texto": "Semana 15", "t_max": 290},

        # ================= TEMA D =================
        # Más aplicaciones de ecuaciones lineales en problemas prácticos
        {"id": "D1", "mision": 1, "pregunta": "Un puente recto une A=(-6, 1) con B=(6, 6). Halla su pendiente (m) y su intercepto (b):", "opciones": ["m = 5/12, b = 3.5", "m = -5/12, b = 3.5", "m = 12/5, b = -3", "m = 5/12, b = -3.5"], "correcta_texto": "m = 5/12, b = 3.5", "t_max": 275},
        {"id": "D2", "mision": 1, "pregunta": "Determina la ecuación de la recta que pasa por los puntos de anclaje A(-4, 8) y B(2, -1):", "opciones": ["y = 3/2x + 2", "y = -3/2x + 2", "y = -2/3x + 2", "y = 3/2x - 2"], "correcta_texto": "y = -3/2x + 2", "t_max": 275},
        {"id": "D3", "mision": 1, "pregunta": "Una rampa inicia en P(3, -4) con pendiente m = -1/3. ¿Cuál es su ecuación (y = mx + b)?", "opciones": ["y = -1/3x - 3", "y = -1/3x + 3", "y = 1/3x - 3", "y = -3x - 3"], "correcta_texto": "y = -1/3x - 3", "t_max": 275},
        {"id": "D4", "mision": 1, "pregunta": "Si un cable sigue la línea y = -5/6x - 1, ¿cuál de estas opciones es PARALELA?", "opciones": ["y = 6/5x + 4", "y = 5/6x - 1", "y = -5/6x + 9", "y = -6/5x + 2"], "correcta_texto": "y = -5/6x + 9", "t_max": 260},
        {"id": "D5", "mision": 1, "pregunta": "Una calle (y = -1/4x + 5) cruza con otra de forma PERPENDICULAR. ¿Cuál es la ecuación de la segunda calle?", "opciones": ["y = -4x + 2", "y = 1/4x - 5", "y = 4x - 8", "y = -4/1x + 3"], "correcta_texto": "y = 4x - 8", "t_max": 260},
        {"id": "D6", "mision": 1, "pregunta": "Halla la recta con m = 4/5 que pasa por P(5, 7) e indica su punto de corte con el eje Y:", "opciones": ["y = 4/5x + 3 (Corta en 3)", "y = -4/5x + 3 (Corta en 3)", "y = 4/5x - 3 (Corta en -3)", "y = 5/4x + 3 (Corta en 3)"], "correcta_texto": "y = 4/5x + 3 (Corta en 3)", "t_max": 280},
        # Problemas de tasas de cambio y comparación lineal (Misión 2)
        {"id": "D7", "mision": 2, "pregunta": "Un depósito de 80 galones pierde 3 galones cada 2 horas por una fuga. ¿Qué función describe el agua restante (y) tras 'x' horas?", "opciones": ["y = 3/2x + 80", "y = -2/3x + 80", "y = -3/2x + 80", "y = -3/2x - 80"], "correcta_texto": "y = -3/2x + 80", "t_max": 290},
        {"id": "D8", "mision": 2, "pregunta": "Un carpintero cobra (pesos)20 base y (pesos)15 por cada 4 horas de trabajo. ¿Cuánto cobrará por un proyecto de 12 horas?", "opciones": ["(pesos)45", "(pesos)65", "(pesos)35", "(pesos)70"], "correcta_texto": "(pesos)65", "t_max": 290},
        {"id": "D9", "mision": 2, "pregunta": "Globo A (10m de altura, sube 5m cada 4 seg). Globo B (40m de altura, baja 7m cada 4 seg). ¿En qué segundo se cruzan sus alturas?", "opciones": ["8", "10", "12", "15"], "correcta_texto": "10", "t_max": 290},
        {"id": "D10", "mision": 2, "pregunta": "Daniel tiene (pesos)500 y gasta (pesos)30 cada 2 semanas. Sofía tiene (pesos)800 y gasta (pesos)80 cada 2 semanas. ¿En qué semana tendrán lo mismo?", "opciones": ["6", "10", "12", "14"], "correcta_texto": "12", "t_max": 290}
    ]

# --- 4. Inicialización del Estado de la Sesión ---
# Se inicializan las variables de estado si no existen, para asegurar que la app funcione al primer inicio
if 'paso' not in st.session_state:
    # 'paso' controla qué pantalla se muestra: "registro", "examen", "feedback"
    st.session_state.paso = 'registro'

if 'mision' not in st.session_state:
    # 'mision' rastrea en qué misión está el jugador (1 o 2)
    st.session_state.mision = 1 # Empieza siempre en la Misión 1

# --- REFUERZO DE SEGURIDAD PARA MULTIUSUARIOS ---
if 'lista_examen' not in st.session_state:
    # Esto solo se ejecuta UNA VEZ al inicio. 
    # Si el app se refresca, no vuelve a sortear preguntas.
    pool = [p for p in st.session_state.banco_completo if p['mision'] == 1]
    st.session_state.lista_examen = random.sample(pool, 5)
    st.session_state.n_pregunta = 0
    st.session_state.aciertos = 0
    st.session_state.t_inicio_pregunta = time.time()

if 'n_pregunta' not in st.session_state:
    # 'n_pregunta' es el índice de la pregunta actual en 'lista_examen'
    st.session_state.n_pregunta = 0

if 'aciertos' not in st.session_state:
    # 'aciertos' cuenta las respuestas correctas del jugador
    st.session_state.aciertos = 0

if 't_inicio_pregunta' not in st.session_state:
    # 't_inicio_pregunta' guarda el timestamp de cuándo comenzó la pregunta actual (para el cronómetro)
    st.session_state.t_inicio_pregunta = time.time()

if 'power_5050' not in st.session_state:
    # 'power_5050' indica si el power-up 50/50 está disponible (True) o ya se usó (False)
    st.session_state.power_5050 = True

if 'usar_5050' not in st.session_state:
    # 'usar_5050' indica si el power-up 50/50 está ACTIVO para la pregunta actual
    st.session_state.usar_5050 = False

if 'datos_enviados' not in st.session_state:
    # 'datos_enviados' es un flag para evitar enviar la victoria múltiples veces
    st.session_state.datos_enviados = False

# Inicializamos 'nombre', 'curso' y 'txt_nombre' / 'sel_curso' en el registro
# Esto se hará dentro de la lógica de la pantalla de registro, cuando el usuario interactúe.
# Pero si quieres asegurarte de que existan, podrías ponerlos aquí:
# if 'nombre' not in st.session_state: st.session_state.nombre = ""
# if 'curso' not in st.session_state: st.session_state.curso = ""

# ----- FIN DE LA PARTE 2 -----


# Parte 3: Inicialización del Estado y Funciones de Utilidad

# --- 4. INICIALIZACIÓN DE ESTADO (EL CEREBRO DEL JUEGO) ---
# Se inicializan las variables de control si no existen en el session_state.
# Esto asegura que la aplicación tenga un estado inicial consistente.
if 'paso' not in st.session_state:
    st.session_state.update({
        'paso': 'registro',         # Controla la pantalla actual: 'registro', 'examen', 'feedback'
        'nombre': '',               # Almacena el nombre del estudiante
        'curso': '',                # Almacena el curso seleccionado
        'mision': 1,                # Misión actual del juego (1 o 2)
        'n_pregunta': 0,            # Índice de la pregunta actual dentro de 'lista_examen'
        'aciertos': 0,              # Contador de respuestas correctas
        'power_5050': True,         # Indica si el power-up 50/50 está disponible (True) o ya se usó (False)
        'usar_5050': False,         # Indica si el power-up 50/50 está ACTIVO para la pregunta actual
        'lista_examen': [],         # Contiene las 5 preguntas seleccionadas aleatoriamente para el intento actual
        't_inicio_pregunta': 0,     # Timestamp de inicio de la pregunta actual (para el cronómetro)
        'examen_finalizado': False, # Bandera para indicar si se completó el examen o se llegó al feedack
        'datos_enviados': False,     # Flag para evitar enviar datos duplicados al finalizar
		'datos_enviados_m1': False  # Flag para evitar enviar datos de Misión 1 duplicados

    })





# --- 5. FUNCIONES (MOTOR GRÁFICO Y LÓGICA DEL JUEGO) ---

def crear_imagen(texto, opciones, ocultas=[], idx_pregunta=None, id_pregunta=None):
    """
    Genera una imagen para la pregunta usando Matplotlib.
    Maneja opciones ocultas por el power-up 50/50 y limpia caracteres
    que podrían causar distorsión en el renderizado (como '(pesos)' o '$').
    
    Args:
        texto (str): El texto de la pregunta.
        opciones (list): Lista de strings con las opciones de respuesta (ej. ["A) texto", "B) texto"]).
        ocultas (list): Lista de letras de opciones a ocultar (ej. ['B', 'D']).
        idx_pregunta (int, optional): Índice de la pregunta actual. Útil para debugging. Por defecto es None.
        id_pregunta (str, optional): ID de la pregunta. Útil para debugging. Por defecto es None.
        
    Returns:
        io.BytesIO: Un buffer de bytes que contiene la imagen PNG generada.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('white') # Fondo blanco para la imagen generada

    # Preparamos las opciones para mostrar, ocultando las indicadas
    finales_render = []
    for opt_completo in opciones: # Formato esperado: "A) Opción de texto"
        letra_opcion = opt_completo[0] # Extrae la letra (ej. "A")
        
        # Si la letra de esta opción está en la lista de 'ocultas' y tenemos el índice de pregunta
        if letra_opcion in ocultas and idx_pregunta is not None:
            finales_render.append(f"{letra_opcion} [ ELIMINADA ]")
        else:
            # Limpiamos el texto de la opción para Matplotlib.
            # Reemplazamos '(moneda)' o '(pesos)' por un espacio para evitar problemas de renderizado.
            texto_limpio_opcion = opt_completo.replace('(moneda)', ' ').replace('(pesos)', ' ')
            finales_render.append(texto_limpio_opcion)

    # Construimos el cuerpo completo del texto (pregunta + opciones)
    # Añadimos dos saltos de línea para un espaciado claro entre pregunta y opciones.
    cuerpo_final = f"{texto}\n\n" + "\n".join(finales_render)

    # Determina el tamaño de fuente basado en la longitud del texto para mejorar legibilidad
    size_fuente = 16 if len(cuerpo_final) < 200 else 14

    # Limpieza adicional del texto para el renderizado visual en Matplotlib.
    # Esto asegura que caracteres como '$' o '(moneda)' no generen distorsiones.
    cuerpo_renderizado = cuerpo_final.replace('$', ' ').replace('(moneda)', ' ') # Más limpieza

    # Dibujamos el texto limpio en la celda del gráfico 'ax'.
    # va='top' para alinear el texto desde la parte superior.
    # ha='left' para alinear el texto a la izquierda.
    # linespacing=1.6 para un espaciado cómodo entre líneas.
    ax.text(0.05, 0.9, cuerpo_renderizado,
            fontsize=size_fuente,
            fontweight='bold',
            wrap=True, # Permite que el texto pase a la siguiente línea si es necesario
            va='top',
            ha='left',
            color='#2d0b2a', # Color oscuro para el texto principal
            family='sans-serif', # Fuente genérica sin serifa para compatibilidad
            linespacing=1.6)

    ax.axis('off') # Ocultamos los ejes de la gráfica (el borde blanco de la imagen)

    # Guardamos la imagen generada en un buffer de memoria (formato PNG).
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=120) # bbox_inches='tight' recorta el espacio sobrante
    plt.close(fig) # Cerramos la figura para liberar memoria del sistema
    buf.seek(0) # Movemos el puntero del buffer al inicio para que Streamlit pueda leerlo
    return buf


def reset_juego():
    """
    Limpia el estado del juego en session_state para permitir un nuevo intento
    desde la pantalla de registro.
    """
    st.session_state.update({
        'paso': 'registro',         
        'mision': 1,                
        'n_pregunta': 0,            
        'aciertos': 0,              
        'power_5050': True,         
        'usar_5050': False,         
        'lista_examen': [],         
        'examen_finalizado': False, 
        'datos_enviados': False,       # <-- Reiniciar flag de envío final
        'datos_enviados_m1': False     # <-- NUEVO: Reiniciar flag de envío Misión 1
    })
    # Limpiar claves específicas de preguntas de session_state
    claves_a_eliminar = [key for key in st.session_state.keys() if key.startswith(('q_opts_', 'q_cor_', 'inc_', 'ocultas_fix_', 'rad_valid_'))] # Añadir rad_valid_ aquí
    for key in claves_a_eliminar:
        del st.session_state[key]
	
def enviar_a_google(nombre, curso, mision, aciertos, powerup):
    """
    Envía los resultados del juego a una hoja de cálculo de Google Sheets
    usando un Google Apps Script desplegado.
    """
    # **IMPORTANTE**: Actualiza esta URL con la de tu ÚLTIMA implantación del script.
    url_script = "https://script.google.com/macros/s/AKfycbzhJCZfjy2QSZu2-rTyv5jgLJLv-1vjwMgTCfpG2e-IGK0OInXE2pzoEy1WnB_59PXY7g/exec"
    
    # Formato de los datos a enviar. 'powerup' se traduce a 'Sí' o 'No'.
    datos = {
        "nombre": nombre,
        "curso": curso,
        "mision": mision,
        "aciertos": aciertos,
        "powerup": "Sí" if not powerup else "No" # Si power_5050 es False, significa que se usó.
    }
    
    try:
        # Se envía la petición POST con los datos en formato JSON.
        response = requests.post(url_script, json=datos)
        # Imprimir en la consola (o logs) qué pasó
        print(f"--- Envío a Google Sheets ---")
        print(f"URL: {url_script}")
        print(f"Datos enviados: {datos}")
        print(f"Código de estado de respuesta: {response.status_code}")
        print(f"Texto de la respuesta: {response.text}")
        print(f"-------------------------------")
        # Se imprime en la consola para confirmar el envío o registrar errores.
        if response.status_code == 200:
            print(f"Datos enviados correctamente a Google Sheets para {nombre} - Misión {mision}.")
        else:
            print(f"Error al enviar datos a Google Sheets. Código: {response.status_code}")
            print(f"Respuesta del servidor: {response.text}")
            
    except requests.exceptions.RequestException as e:
        # Captura errores generales de red o conexión.
        print(f"Error de red o conexión al intentar enviar a Google Sheets: {e}")
    except Exception as e:
        # Captura cualquier otro error inesperado.
        print(f"Error inesperado al enviar a Google Sheets: {e}")
        
    # Nota: Si la función debe ser completamente silenciosa ante fallos,
    # puedes volver al 'pass' en el except. Sin embargo, es mejor registrar los errores.

# ----- FIN DE LA PARTE 3 -----

# Parte 4: Flujo del Juego - Pantallas y Lógica de Transición

# --- 4. INICIALIZACIÓN DE ESTADO (EL CEREBRO DEL JUEGO) --- (Este fragmento pertenece a la Parte 3, pero es necesario para que el código funcione)
# Asegúrate de que tus Partes 1, 2 y 3 estén correctas. Aquí sólo incluyo la inicialización de flags relevantes.

# --- 4. ESTADO DE SESIÓN (UNIFICADO Y REFORZADO) ---

def inicializar_estado():
    if 'paso' not in st.session_state:
        st.session_state.update({
            'paso': 'registro',         # Pantalla inicial
            'nombre': '',               
            'curso': '',                
            'mision': 1,                
            'n_pregunta': 0,            
            'aciertos': 0,              
            'power_5050': True,         
            'ocultar': [],              # Reemplaza a 'usar_5050' para mayor claridad
            'lista_examen': [],         # Aquí se "anclan" las 5 preguntas
            't_inicio_pregunta': time.time(),
            'examen_finalizado': False, 
            'datos_enviados': False,    # Evita duplicados en Misión 2
            'datos_enviados_m1': False  # Evita duplicados en Misión 1
        })

# Ejecutamos la función de inicio
inicializar_estado()


# Asegúrate que la función reset_juego() (de la Parte 3) también incluye:
# 'datos_enviados': False,       
# 'datos_enviados_m1': False     

# --- 5. FUNCIONES (MOTOR GRÁFICO Y LÓGICA DEL JUEGO) --- (Este fragmento pertenece a la Parte 3)
# Asegúrate de tener la versión actualizada de crear_imagen y enviar_a_google
# La función reset_juego() YA ESTÁ ACTUALIZADA EN LA RESPUESTA ANTERIOR.



# --- 5. FUNCIONES Y LÓGICA DE CARGA ---

def preparar_mision_blindada(n_mision):
    """
    Selecciona las preguntas una sola vez y las guarda 
    fírmemente en la sesión para que no 'salten'.
    """
    pool = [p for p in st.session_state.banco_completo if p['mision'] == n_mision]
    # Sorteamos 5 preguntas y las dejamos fijas
    st.session_state.lista_examen = random.sample(pool, min(5, len(pool)))
    st.session_state.n_pregunta = 0
    st.session_state.aciertos = 0
    st.session_state.t_inicio_pregunta = time.time()
    st.session_state.ocultar = []
    # Marcamos que ya tenemos una lista fija
    st.session_state.lista_lista = True

def crear_imagen(texto, opciones, ocultas=[]):
    """Genera la imagen del problema con formato de examen real"""
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('white')
    letras = ["A)", "B)", "C)", "D)"]
    finales = []
    
    for i, opt in enumerate(opciones):
        if letras[i][0] in ocultas:
            finales.append(f"{letras[i]} [ ELIMINADA ]")
        else:
            finales.append(f"{letras[i]} {opt}")
    
    cuerpo = f"{texto}\n\n" + "\n".join(finales)
    
    # Alineación a la izquierda y espaciado generoso para lectura clara
    ax.text(0.05, 0.9, cuerpo, fontsize=15, fontweight='bold', 
            wrap=True, va='top', ha='left', linespacing=1.6, color='#2d0b2a')
    
    ax.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    plt.close(fig)
    return buf

def enviar_a_google(nombre, curso, mision, aciertos):
    """Envío de datos al Sheets configurado"""
    url_script = "TU_URL_AQUI" 
    datos = {"nombre": nombre, "curso": curso, "mision": mision, "aciertos": aciertos}
    try:
        requests.post(url_script, json=datos, timeout=5)
    except:
        pass # Evita que la app se caiga si falla el internet de la escuela
		

# --- 6. PANTALLAS (FLUJO DE JUEGO) ---

# --- PANTALLA 1: REGISTRO (VERSIÓN ANTICHOQUE) ---
if st.session_state.paso == 'registro':
    st.markdown("<div class='status-panel'>MATH QUEST: REGISTRO DE GUERRERO</div>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='input-container'>", unsafe_allow_html=True)
        
        # Campos de entrada
        nom = st.text_input("Nombre del Guerrero:", key="txt_nombre")
        cur = st.selectbox("Misión del Curso:", ["901", "902", "903", "904", "908", "909", "910"], key="sel_curso")

        if st.button("¡INICIAR AVENTURA!"):
            if nom: 
                # 1. Filtramos el banco de preguntas para la Misión 1
                pool_m1 = [p for p in st.session_state.banco_completo if p['mision'] == 1]
                
                if len(pool_m1) >= 5:
                    # 2. SELECCIÓN ÚNICA: Elegimos las 5 preguntas AQUÍ y solo AQUÍ
                    preguntas_seleccionadas = random.sample(pool_m1, 5)
                    
                    # 3. ACTUALIZACIÓN MASIVA: Seteamos todo el estado de una vez
                    st.session_state.update({
                        'nombre': nom,
                        'curso': cur,
                        'paso': 'examen',          
                        'mision': 1,
                        'n_pregunta': 0,            
                        'aciertos': 0,              
                        'lista_examen': preguntas_seleccionadas, # Anclamos las preguntas
                        't_inicio_pregunta': time.time(),
                        'power_5050': True,         
                        'ocultar': [],
                        'datos_enviados_m1': False,
                        'datos_enviados': False
                    })
                    
                    # 4. LIMPIEZA DE MEMORIA: Borramos basura de sesiones anteriores
                    for key in list(st.session_state.keys()):
                        if key.startswith(('q_opts_', 'rad_m')):
                            del st.session_state[key]

                    st.rerun() 
                else:
                    st.error("Error técnico: El banco de preguntas no cargó correctamente.")
            else:
                st.warning("Escribe tu nombre para poder registrar tu nota.") 
        
        st.markdown("</div>", unsafe_allow_html=True)
# --- PANTALLA 2: EXAMEN ---
elif st.session_state.paso == 'examen':
    idx = st.session_state.n_pregunta 

    # --- Verificación de Fin de Ronda/Misión ---
    if idx >= len(st.session_state.lista_examen):
        st.session_state.paso = 'feedback'  
        st.rerun()  

    p = st.session_state.lista_examen[idx]

    # --- Lógica para Anclar Opciones y Preparar 50/50 ---
    if f"q_opts_{idx}" not in st.session_state:
        opts_mezcladas = p['opciones'].copy()
        random.shuffle(opts_mezcladas)

        letras = ["A)", "B)", "C)", "D)"] 

        st.session_state[f"q_opts_{idx}"] = [f"{letras[i]} {opts_mezcladas[i]}" for i in range(4)]

        try:
            indice_correcta = opts_mezcladas.index(p['correcta_texto'])
            st.session_state[f"q_cor_{idx}"] = ["A", "B", "C", "D"][indice_correcta]
            cor_letra = st.session_state[f"q_cor_{idx}"]
            st.session_state[f"inc_{idx}"] = [L for L in ["A", "B", "C", "D"] if L != cor_letra]
            
        except ValueError:
            error_msg = f"Error: La respuesta correcta '{p['correcta_texto']}' no se encontró en las opciones mezcladas para la pregunta ID {p.get('id', 'N/A')}. Opciones actuales: {opts_mezcladas}"
            print(error_msg) 
            st.error(f"Error interno de configuración de pregunta. Por favor, contacta al administrador. (Pregunta ID: {p.get('id', 'N/A')})")
            st.session_state[f"q_cor_{idx}"] = "A" 
            st.session_state[f"inc_{idx}"] = ["B", "C", "D"] 

    # --- UI: Panel de Estado Superior (Power-up) y Barra de Energía (Tiempo) ---
    msg = "⚡ 50/50 DISPONIBLE" if st.session_state.power_5050 else "¡SIN POWER-UPS activados!"
    if st.session_state.usar_5050: msg = "🔥 MODO 50/50 ACTIVADO"
    st.markdown(f"<div class='status-panel'>{msg}</div>", unsafe_allow_html=True)

    t_limite = p.get('t_max', 60) 
    t_actual = time.time() - st.session_state.t_inicio_pregunta
    porcentaje = max(0.0, (t_limite - t_actual) / t_limite) * 100 
    st.markdown(f"<div class='energy-container'><div class='energy-bar' style='width:{porcentaje:.2f}%'></div></div>", unsafe_allow_html=True)

    # --- Lógica para Ocultar Opciones con Power-up 50/50 ---
    ocultas_actuales = [] 
    if st.session_state.usar_5050: # Si el power-up está activo
        if f"ocultas_fix_{idx}" not in st.session_state: # Si aún no se han calculado las ocultas para esta pregunta
            st.session_state[f"ocultas_fix_{idx}"] = random.sample(st.session_state[f"inc_{idx}"], 2)
        ocultas_actuales = st.session_state[f"ocultas_fix_{idx}"]

    # --- Renderizado de la Pregunta Completa (Imagen) ---
    img_buf = crear_imagen(p['pregunta'], st.session_state[f"q_opts_{idx}"], ocultas_actuales)
    st.markdown("<div class='question-card'>", unsafe_allow_html=True)
    st.image(img_buf) 
    st.markdown("</div>", unsafe_allow_html=True)

    # --- Botón del Power-up 50/50 ---
    col_izq, col_der = st.columns([3, 1]) 
    with col_der:
        if st.session_state.power_5050: 
            if st.button("⚡ 50/50"):
                st.session_state.usar_5050 = True # Activa el power-up
                st.session_state.power_5050 = False # Marca como usado
                st.rerun() # Recarga para actualizar la UI y ocultar opciones

    # --- Selección de Respuesta por el Usuario y Filtro de Opciones Visibles ---
    opciones_para_radio = []
    letras_habilitadas = [] # Las letras que el usuario PUEDE seleccionar (A, B, C, D)
    opciones_reales = st.session_state[f"q_opts_{idx}"] # Las opciones completas (ej: "A) 65 (moneda)")
    
    # Filtramos las opciones para el radio button, excluyendo las ocultas por el 50/50
    for i, opt_completo in enumerate(opciones_reales):
        letra = opt_completo[0]
        if letra not in ocultas_actuales:
            opciones_para_radio.append(opt_completo) # Añade la opción visible
            letras_habilitadas.append(letra)      # Guarda la letra habilitada
            
    # --- st.radio ahora usa las opciones filtradas ---
    # Usamos la lista de LETRAS HABILITADAS para el índice del radio button
    ans_letra_input = st.radio("TU ELECCIÓN:", letras_habilitadas, key=f"rad_valid_{idx}", index=None, horizontal=True)
    
    # --- Botón de ENVIAR RESPUESTA y Lógica de Fin de Tiempo ---
    if st.button("ENVIAR RESPUESTA ➡️") or porcentaje <= 0.0:
        opcion_elegida_completa = "" # Variable para guardar la opción completa que el usuario seleccionó
        
        if ans_letra_input: # Si se seleccionó una letra válida
            # Buscamos la opción completa que empieza con la letra seleccionada
            for opt in opciones_reales:
                if opt.startswith(ans_letra_input + ")"):
                    opcion_elegida_completa = opt
                    break
            
            valor_respuesta_usuario = opcion_elegida_completa.split(") ", 1)[1]

    # --- LÓGICA DE COMPARACIÓN DE RESPUESTA ---
            if valor_respuesta_usuario == p['correcta_texto']:
                st.session_state.aciertos += 1 
                st.toast("¡Punto para ti!", icon="🔥") 
            else:
                st.toast("Incorrecto...", icon="❌")
        else:
            st.toast("Debes seleccionar una opción, o el tiempo se agotó.", icon="⚠️")
            # Si se agota el tiempo sin seleccionar, se considera incorrecta.
            # No se suma acierto, pero se avanza a la siguiente pregunta.

        # --- Preparación para la Siguiente Pregunta o Transición de Misión ---
        st.session_state.n_pregunta += 1 
        st.session_state.t_inicio_pregunta = time.time() 
        st.session_state.usar_5050 = False # Desactivar 50/50 para la siguiente pregunta

        # --- Verificación de Fin de Ronda/Misión ---
        if st.session_state.n_pregunta >= len(st.session_state.lista_examen):
            
            # --- Lógica de Transición entre Misiones ---
            if st.session_state.mision == 1: # Si se completó la Misión 1
                # Pasamos directamente a FEEDBACK. La pantalla de feedback decidirá si avanza a M2.
                st.session_state.paso = 'feedback' 
                st.rerun() # Recarga para mostrar el feedback de Misión 1
                
            else: # Si estábamos completando la Misión 2 (misión final)
                st.session_state.paso = 'feedback' # Pasar a la pantalla de feedback final
                st.rerun() # Recarga para mostrar feedback final
        
        # Si aún quedan preguntas en la misión actual, recargar para mostrar la siguiente.
        if st.session_state.n_pregunta < len(st.session_state.lista_examen):
            st.rerun()

    # --- Auto-refresh del Cronómetro ---
    if porcentaje > 0:
        time.sleep(1) 
        st.rerun() 

# --- PANTALLA 3: FEEDBACK (Resultado Final) ---
elif st.session_state.paso == 'feedback':
    st.markdown(f"<div class='status-panel'>RESULTADO FINAL</div>", unsafe_allow_html=True)
    st.markdown("<div class='question-card' style='text-align:center;'>", unsafe_allow_html=True)

    puntaje = st.session_state.aciertos
    mision_actual = st.session_state.mision

    st.markdown(f"## Resultado: {puntaje}/5")

    # --- Lógica de Aprobación y Mensajes, y Transición ---

    # CASO 1: Misión 1 completada
    if mision_actual == 1:
        if puntaje >= 3:
            st.success(f"¡Misión 1 Superada ({puntaje}/5)! ¿Deseas continuar a la Misión 2?")
            
            # --- Guardamos el resultado de Misión 1 ---
            if not st.session_state.get('datos_enviados_m1', False): 
                st.toast("Guardando resultado Misión 1...", icon="💾")
                enviar_a_google(
                    st.session_state.nombre, 
                    st.session_state.curso, 
                    "Misión 1", 
                    puntaje, 
                    st.session_state.power_5050
                )
                st.session_state.datos_enviados_m1 = True
                st.toast("Resultado Misión 1 guardado.", icon="✅")
            
            # --- Botón para Avanzar a Misión 2 ---
            # Este botón ahora se muestra SOLO si Misión 1 fue aprobada y
            # todavía no hemos avanzado a Misión 2.
            if st.button("CONTINUAR A MISIÓN 2"):
                # --- Preparar y Transicionar a Misión 2 ---
                pool_m2 = [p for p in st.session_state.banco_completo if p['mision'] == 2]
                num_preguntas_m2 = min(5, len(pool_m2))
                
                if num_preguntas_m2 > 0:
                    st.session_state.lista_examen = random.sample(pool_m2, num_preguntas_m2)
                    # Limpiar claves de preguntas de session_state ANTES de actualizar la misión
                    claves_a_eliminar = [key for key in st.session_state.keys() if key.startswith(('q_opts_', 'q_cor_', 'inc_', 'ocultas_fix_', 'rad_valid_'))]
                    for key in claves_a_eliminar:
                        del st.session_state[key]
                    
                    # Actualizar estado para iniciar Misión 2
                    st.session_state.update({
                        'mision': 2,
                        'n_pregunta': 0,
                        'aciertos': 0,
                        't_inicio_pregunta': time.time(),
                        'paso': 'examen', # Cambiar el paso a 'examen' para cargar las preguntas de Mision 2
                        'usar_5050': False # Asegura que el power-up esté desactivado al inicio de Mision 2
                    })
                    st.rerun() # Recarga para iniciar Misión 2
                else:
                    st.warning("No hay suficientes preguntas para la Misión 2. Finalizando el juego.")
                    # Si no hay M2, forzamos el fin del juego y volvemos al registro
                    reset_juego() 
                    st.rerun()
        
        else: # Misión 1 fallida
            st.error("No has logrado los aciertos mínimos (3/5) para avanzar a la Misión 2.")
            # Si falla M1, el juego termina para este intento. Solo queda el botón de reiniciar.

    # CASO 2: Misión 2 completada (Final del juego)
    elif mision_actual == 2:
        if puntaje >= 3: # Misión 2 aprobada
            st.balloons() 
            st.success("¡Misión 2 Cumplida! ¡Felicidades, Guerrero!")
            
            # --- ACCIÓN DE GUARDADO FINAL (Misión 2) ---
            if not st.session_state.get('datos_enviados', False): 
                st.toast("Guardando tu victoria final en la base de datos...", icon="💾")
                enviar_a_google(
                    st.session_state.nombre, 
                    st.session_state.curso, 
                    "Misión 2 (Final)", 
                    puntaje, 
                    st.session_state.power_5050
                )
                st.session_state.datos_enviados = True 
                st.toast("¡Datos finales guardados con éxito!", icon="✅")
        else: # Misión 2 fallida
            st.error("No has alcanzado la puntuación mínima (3/5) para aprobar la Misión 2.")
            # Aquí el juego también termina.

    # --- Botón para Reiniciar el Juego ---
    # Este botón siempre es visible para reiniciar. Si se está en feedback de M1
    # y se decide "Intentar de Nuevo" en lugar de "Continuar a Misión 2",
    # esto reseteará todo sin avanzar.
    if st.button("INTENTAR DE NUEVO"):
        reset_juego() 
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    # ----- FIN DE LA PARTE 4 -----
