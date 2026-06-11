import streamlit as st
import pandas as pd
from pathlib import Path


@st.cache_data
def cargar_dataset():
    ruta_base = Path(__file__).resolve().parent.parent
    ruta_archivo = ruta_base / "data" / "best_selling_video_games_limpio.xlsx"

    df = pd.read_excel(ruta_archivo)
    return df


def responder_pregunta(pregunta, df):
    pregunta = pregunta.lower()

    if "cuántas columnas" in pregunta or "cuantas columnas" in pregunta:
        return f"El dataset tiene {df.shape[1]} columnas."

    elif "cuántos registros" in pregunta or "cuantos registros" in pregunta or "cuántas filas" in pregunta or "cuantas filas" in pregunta:
        return f"El dataset tiene {df.shape[0]} registros o filas."

    elif "media" in pregunta and ("venta" in pregunta or "sales" in pregunta):
        media = df["SalesMillions"].mean()
        return f"La media de ventas es de {media:.2f} millones."

    elif "promedio" in pregunta and ("venta" in pregunta or "sales" in pregunta):
        promedio = df["SalesMillions"].mean()
        return f"El promedio de ventas es de {promedio:.2f} millones."

    elif "mayor venta" in pregunta or "más vendido" in pregunta or "mas vendido" in pregunta:
        fila = df.sort_values(by="SalesMillions", ascending=False).iloc[0]
        return f"El videojuego más vendido es {fila['Title']}, con {fila['SalesMillions']} millones de ventas."

    elif "menor venta" in pregunta or "menos vendido" in pregunta:
        fila = df.sort_values(by="SalesMillions", ascending=True).iloc[0]
        return f"El videojuego con menor venta dentro del dataset es {fila['Title']}, con {fila['SalesMillions']} millones de ventas."

    elif "año más antiguo" in pregunta or "anio mas antiguo" in pregunta or "año menor" in pregunta:
        anio = int(df["ReleaseYear"].min())
        return f"El año de lanzamiento más antiguo en el dataset es {anio}."

    elif "año más reciente" in pregunta or "anio mas reciente" in pregunta or "año mayor" in pregunta:
        anio = int(df["ReleaseYear"].max())
        return f"El año de lanzamiento más reciente en el dataset es {anio}."

    elif "columnas" in pregunta or "campos" in pregunta:
        columnas = ", ".join(df.columns.tolist())
        return f"Las columnas del dataset son: {columnas}."

    elif "total de ventas" in pregunta or "ventas totales" in pregunta:
        total = df["SalesMillions"].sum()
        return f"El total de ventas registradas en el dataset es de {total:.2f} millones."

    elif "desarrollador" in pregunta and "más frecuente" in pregunta:
        desarrollador = df["Developer"].value_counts().idxmax()
        cantidad = df["Developer"].value_counts().max()
        return f"El desarrollador que más aparece en el dataset es {desarrollador}, con {cantidad} videojuego(s)."

    elif "plataforma" in pregunta and "más frecuente" in pregunta:
        plataforma = df["Platform"].value_counts().idxmax()
        cantidad = df["Platform"].value_counts().max()
        return f"La plataforma que más aparece en el dataset es {plataforma}, con {cantidad} videojuego(s)."

    else:
        return (
            "No pude interpretar esa pregunta. Puedes probar con preguntas como: "
            "'¿Cuántas columnas tiene el dataset?', "
            "'¿Cuál es la media de ventas?', "
            "'¿Cuál es el videojuego más vendido?' o "
            "'¿Cuáles son las columnas del dataset?'."
        )


def mostrar_prompts_ia():
    st.title("🧠 Prompts de IA")
    st.write(
        """
        En esta sección el usuario puede escribir preguntas sobre el dataset y la aplicación
        genera una respuesta automática. Esta interfaz simula una consulta inteligente sobre los datos.
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

    pregunta = st.text_input(
        "Escribe tu pregunta:",
        placeholder="Ejemplo: ¿Cuál es el videojuego más vendido?"
    )

    if st.button("Responder"):
        if not pregunta.strip():
            st.warning("Escribe una pregunta para poder responder.")
        else:
            respuesta = responder_pregunta(pregunta, df)

            st.subheader("Respuesta")
            st.success(respuesta)

    st.divider()

    st.subheader("📌 Preguntas de ejemplo")

    ejemplos = [
        "¿Cuántas columnas tiene el dataset?",
        "¿Cuántos registros tiene el dataset?",
        "¿Cuál es la media de ventas?",
        "¿Cuál es el videojuego más vendido?",
        "¿Cuál es el videojuego menos vendido?",
        "¿Cuál es el año más antiguo?",
        "¿Cuál es el año más reciente?",
        "¿Cuáles son las columnas del dataset?",
        "¿Cuál es el total de ventas?",
        "¿Cuál es el desarrollador más frecuente?",
        "¿Cuál es la plataforma más frecuente?"
    ]

    for ejemplo in ejemplos:
        st.write(f"- {ejemplo}")

    st.divider()

    st.subheader("✅ Conclusión")

    st.write(
        """
        Esta sección permite consultar información del dataset mediante preguntas escritas.
        Aunque no utiliza una API externa de inteligencia artificial, funciona como una interfaz
        de consulta inteligente basada en reglas y condiciones programadas.
        """
    )