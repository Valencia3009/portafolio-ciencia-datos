import streamlit as st
import pandas as pd
from pathlib import Path


@st.cache_data
def cargar_dataset():
    ruta_base = Path(__file__).resolve().parent.parent
    ruta_archivo = ruta_base / "data" / "best_selling_video_games_limpio.xlsx"

    df = pd.read_excel(ruta_archivo)

    return df


def mostrar_inicio():
    st.markdown(
        """
        <style>
        .main-title {
            font-size: 42px;
            font-weight: bold;
            color: #6C63FF;
            text-align: center;
            margin-bottom: 5px;
        }

        .subtitle {
            font-size: 22px;
            color: #444;
            text-align: center;
            margin-bottom: 30px;
        }

        .card {
            background-color: #f7f7fb;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
            margin-bottom: 20px;
        }

        .section-title {
            color: #6C63FF;
            font-size: 26px;
            font-weight: bold;
            margin-top: 20px;
        }

        .info-text {
            font-size: 17px;
            text-align: justify;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="main-title">Portafolio Profesional de Ciencia de Datos</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Proyecto desarrollado en Streamlit | Videojuegos más vendidos</div>', unsafe_allow_html=True)

    st.divider()

    col_foto, col_info = st.columns([1, 2])

    with col_foto:
        ruta_base = Path(__file__).resolve().parent.parent
        ruta_foto = ruta_base / "assets" / "foto.jpg"

        if ruta_foto.exists():
            st.image(str(ruta_foto), use_container_width=True)
        else:
            st.info("Aquí irá tu fotografía personal.")
            st.write("Guarda tu foto en:")
            st.code("assets/foto.jpg")

    with col_info:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("Jonathan Alexander Carrillo Valencia")

        st.write(
            """
            Soy estudiante de Ingeniería en Sistemas y Redes Informáticas y en este portafolio se presenta un
            proyecto de Ciencia de Datos desarrollado en Streamlit, utilizando un dataset sobre los videojuegos
            más vendidos. A través de esta aplicación se integran análisis exploratorio, aprendizaje automático,
            recomendación, carga de archivos, scraping, análisis de sentimientos e inteligencia artificial.
            """
        )

        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    st.markdown('<div class="section-title">Data Storytelling</div>', unsafe_allow_html=True)

    st.write(
        """
        En esta sección se presenta un video demostrativo donde se explica el análisis realizado sobre el dataset,
        mostrando los principales hallazgos, gráficos, hipótesis y resultados del aprendizaje automático.
        """
    )

    video_url = "https://youtu.be/9zDSwc7pZac"

    st.video(video_url)

    st.divider()

    st.markdown('<div class="section-title">Navegación del portafolio</div>', unsafe_allow_html=True)

    st.write(
        """
        Este portafolio permite navegar entre las diferentes secciones desarrolladas para la Tarea 1,
        Tarea 2 y Parcial de Ciencia de Datos.
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            **Tarea 1**

            - Análisis Exploratorio  
            - Aprendizaje Automático  
            - Sistema de Recomendación  
            """
        )

    with col2:
        st.markdown(
            """
            **Tarea 2**

            - Carga de Archivos  
            - Scraping  
            - Análisis de Sentimientos  
            """
        )

    with col3:
        st.markdown(
            """
            **Complemento**

            - Prompts de IA  
            - Consulta inteligente del dataset  
            - Respuestas con Gemini  
            """
        )

    st.divider()

    st.title("Proyecto de Ciencia de Datos")
    st.subheader("Análisis de los videojuegos más vendidos")

    st.write(
        """
        Bienvenido a esta aplicación desarrollada en Streamlit para la asignatura 
        Técnica Electiva I - Ciencia de Datos.

        En este proyecto se utiliza un dataset sobre los videojuegos más vendidos, 
        el cual permite realizar análisis exploratorio, aprendizaje automático, 
        sistema de recomendación, carga de archivos, scraping y análisis de sentimientos.
        """
    )

    st.divider()

    try:
        df = cargar_dataset()

        st.subheader("Información general del dataset")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total de registros", df.shape[0])
        col2.metric("Total de columnas", df.shape[1])

        if "SalesMillions" in df.columns:
            total_ventas = df["SalesMillions"].sum()
            col3.metric("Ventas totales", f"{total_ventas:.2f} millones")
        else:
            col3.metric("Ventas totales", "No disponible")

        st.write("### Vista previa del dataset")
        st.dataframe(df.head(10), use_container_width=True)

        st.write("### Columnas del dataset")
        st.write(list(df.columns))

    except Exception as e:
        st.error("No se pudo cargar el dataset.")
        st.info(
            "Verifica que el archivo `best_selling_video_games_limpio.xlsx` esté dentro de la carpeta `data`."
        )
        st.write("Error:", e)

    st.divider()

    st.subheader("Secciones de la aplicación")

    st.write(
        """
        La aplicación está organizada en las siguientes opciones:

        - **Inicio:** Portafolio profesional de Ciencia de Datos.
        - **Análisis Exploratorio:** Revisión del dataset, campos, gráficos e hipótesis.
        - **Aprendizaje Automático:** Modelos para analizar variables del dataset.
        - **Sistema de Recomendación:** Recomendación de videojuegos según criterios seleccionados.
        - **Carga de Archivos:** Carga de archivos externos para analizarlos.
        - **Análisis de Sentimientos y Scraping:** Extracción de opiniones y análisis de sentimiento.
        - **Prompts de IA:** Consultas inteligentes sobre el dataset mediante Gemini.
        """
    )