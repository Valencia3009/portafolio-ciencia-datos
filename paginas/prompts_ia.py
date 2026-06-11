import streamlit as st
import pandas as pd
from pathlib import Path
from google import genai


@st.cache_data
def cargar_dataset():
    ruta_base = Path(__file__).resolve().parent.parent
    ruta_archivo = ruta_base / "data" / "best_selling_video_games_limpio.xlsx"

    df = pd.read_excel(ruta_archivo)
    return df


def crear_contexto_dataset(df):
    contexto = f"""
    Dataset: videojuegos más vendidos.

    Columnas del dataset:
    {", ".join(df.columns.tolist())}

    Total de registros: {df.shape[0]}
    Total de columnas: {df.shape[1]}

    Ventas totales: {df["SalesMillions"].sum():.2f} millones.
    Promedio de ventas: {df["SalesMillions"].mean():.2f} millones.
    Venta máxima: {df["SalesMillions"].max():.2f} millones.
    Venta mínima: {df["SalesMillions"].min():.2f} millones.

    Año más antiguo: {int(df["ReleaseYear"].min())}
    Año más reciente: {int(df["ReleaseYear"].max())}

    Primeros 25 registros del dataset:
    {df.head(25).to_string(index=False)}
    """

    return contexto


def responder_con_gemini(pregunta, df):
    api_key = st.secrets["GEMINI_API_KEY"]

    client = genai.Client(api_key=api_key)

    contexto = crear_contexto_dataset(df)

    prompt = f"""
    Eres un asistente de ciencia de datos.
    Responde en español, de forma clara, sencilla y útil para una exposición académica.

    Debes responder usando únicamente la información del dataset proporcionado.
    Si la pregunta no se puede responder con el dataset, dilo claramente.

    Contexto del dataset:
    {contexto}

    Pregunta del usuario:
    {pregunta}
    """

    respuesta = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return respuesta.text


def mostrar_prompts_ia():
    st.title("🧠 Prompts de IA con Gemini")

    st.write(
        """
        En esta sección el usuario puede escribir preguntas abiertas sobre el dataset.
        La aplicación utiliza Gemini para generar respuestas basadas en los datos de videojuegos.
        """
    )

    try:
        df = cargar_dataset()
    except Exception as e:
        st.error("No se pudo cargar el dataset.")
        st.write("Error:", e)
        return

    st.divider()

    st.subheader("💬 Realiza una pregunta sobre el dataset")

    pregunta = st.text_area(
        "Escribe tu pregunta:",
        placeholder="Ejemplo: ¿Qué relación puede existir entre el ranking y las ventas?"
    )

    if st.button("Preguntar a Gemini"):
        if not pregunta.strip():
            st.warning("Escribe una pregunta para poder responder.")
            return

        try:
            with st.spinner("Gemini está analizando el dataset..."):
                respuesta = responder_con_gemini(pregunta, df)

            st.subheader("Respuesta de Gemini")
            st.success(respuesta)

        except Exception as e:
            st.error("No se pudo obtener respuesta de Gemini.")
            st.info(
                "Verifica que tu API Key esté bien escrita en `.streamlit/secrets.toml`, "
                "que tengas conexión a internet y que instalaste `google-genai`."
            )
            st.write("Error:", e)

    st.divider()

    st.subheader("📌 Preguntas que puedes probar")

    st.write(
        """
        - ¿Cuál es el videojuego más vendido?
        - ¿Qué relación puede existir entre el ranking y las ventas?
        - ¿Qué conclusión general se puede obtener del dataset?
        - ¿Qué desarrolladores aparecen en los videojuegos más vendidos?
        - ¿Qué juegos recomendarías analizar más a fondo?
        - ¿El año de lanzamiento influye en las ventas?
        """
    )

    st.divider()

    st.subheader("✅ Conclusión")

    st.write(
        """
        Esta sección permite hacer consultas abiertas sobre el dataset utilizando una API de inteligencia artificial.
        De esta forma, el usuario puede obtener respuestas más flexibles que las preguntas programadas manualmente.
        """
    )