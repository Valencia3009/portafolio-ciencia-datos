import streamlit as st

from paginas.inicio import mostrar_inicio
from paginas.exploratorio import mostrar_exploratorio
from paginas.aprendizaje import mostrar_aprendizaje
from paginas.recomendacion import mostrar_recomendacion
from paginas.carga_archivos import mostrar_carga_archivos
from paginas.sentimientos import mostrar_sentimientos
from paginas.prompts_ia import mostrar_prompts_ia


st.set_page_config(
    page_title="Proyecto Ciencia de Datos",
    page_icon="🎮",
    layout="wide"
)


st.sidebar.title("🎮 Menú Principal")

opcion = st.sidebar.radio(
    "Seleccione una opción:",
    [
        "Inicio",
        "Análisis Exploratorio",
        "Aprendizaje Automático",
        "Sistema de Recomendación",
        "Carga de Archivos",
        "Análisis de Sentimientos y Scraping",
        "Prompts de IA"
    ]
)


if opcion == "Inicio":
    mostrar_inicio()

elif opcion == "Análisis Exploratorio":
    mostrar_exploratorio()

elif opcion == "Aprendizaje Automático":
    mostrar_aprendizaje()

elif opcion == "Sistema de Recomendación":
    mostrar_recomendacion()

elif opcion == "Carga de Archivos":
    mostrar_carga_archivos()

elif opcion == "Análisis de Sentimientos y Scraping":
    mostrar_sentimientos()

elif opcion == "Prompts de IA":
    mostrar_prompts_ia()