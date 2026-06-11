import streamlit as st
import pandas as pd
from pathlib import Path


@st.cache_data
def cargar_dataset():
    ruta_base = Path(__file__).resolve().parent.parent
    ruta_archivo = ruta_base / "data" / "best_selling_video_games_limpio.xlsx"

    df = pd.read_excel(ruta_archivo)
    return df


def mostrar_recomendacion():
    st.title("🎯 Sistema de Recomendación de Videojuegos")

    st.write(
        """
        En esta sección se implementa un sistema de recomendación de videojuegos.
        El usuario puede seleccionar sus preferencias y la aplicación recomendará juegos
        que coincidan con esos criterios.
        """
    )

    try:
        df = cargar_dataset()
    except Exception as e:
        st.error("No se pudo cargar el dataset.")
        st.write("Error:", e)
        return

    st.divider()

    st.subheader("🎮 Selecciona tus preferencias")

    plataformas = sorted(df["Platform"].dropna().unique().tolist())
    series = sorted(df["Series"].dropna().unique().tolist())
    desarrolladores = sorted(df["Developer"].dropna().unique().tolist())

    plataforma = st.selectbox(
        "Seleccione una plataforma:",
        ["Cualquiera"] + plataformas
    )

    serie = st.selectbox(
        "Seleccione una serie o franquicia:",
        ["Cualquiera"] + series
    )

    desarrollador = st.selectbox(
        "Seleccione un desarrollador:",
        ["Cualquiera"] + desarrolladores
    )

    ventas_minimas = st.slider(
        "Ventas mínimas en millones:",
        min_value=float(df["SalesMillions"].min()),
        max_value=float(df["SalesMillions"].max()),
        value=float(df["SalesMillions"].min()),
        step=1.0
    )

    anio_minimo = st.slider(
        "Año mínimo de lanzamiento:",
        min_value=int(df["ReleaseYear"].min()),
        max_value=int(df["ReleaseYear"].max()),
        value=int(df["ReleaseYear"].min()),
        step=1
    )

    st.divider()

    recomendaciones = df.copy()

    if plataforma != "Cualquiera":
        recomendaciones = recomendaciones[
            recomendaciones["Platform"].astype(str).str.contains(plataforma, case=False, na=False)
        ]

    if serie != "Cualquiera":
        recomendaciones = recomendaciones[
            recomendaciones["Series"].astype(str).str.contains(serie, case=False, na=False)
        ]

    if desarrollador != "Cualquiera":
        recomendaciones = recomendaciones[
            recomendaciones["Developer"].astype(str).str.contains(desarrollador, case=False, na=False)
        ]

    recomendaciones = recomendaciones[
        (recomendaciones["SalesMillions"] >= ventas_minimas) &
        (recomendaciones["ReleaseYear"] >= anio_minimo)
    ]

    recomendaciones = recomendaciones.sort_values(by="SalesMillions", ascending=False)

    st.subheader("📌 Resultados de recomendación")

    if recomendaciones.empty:
        st.warning("No se encontraron videojuegos con esos criterios.")
        st.info("Prueba usando opciones más generales, por ejemplo dejando plataforma, serie o desarrollador en 'Cualquiera'.")
    else:
        st.success(f"Se encontraron {len(recomendaciones)} videojuego(s) recomendado(s).")

        columnas_mostrar = [
            "Rank",
            "Title",
            "Platform",
            "Developer",
            "Publisher",
            "ReleaseYear",
            "SalesMillions",
            "Series"
        ]

        st.dataframe(
            recomendaciones[columnas_mostrar],
            use_container_width=True
        )

        st.subheader("🏆 Top recomendaciones")

        top = recomendaciones.head(5)

        for i, fila in top.iterrows():
            st.markdown(
                f"""
                ### 🎮 {fila['Title']}
                **Plataforma:** {fila['Platform']}  
                **Desarrollador:** {fila['Developer']}  
                **Publicador:** {fila['Publisher']}  
                **Año de lanzamiento:** {int(fila['ReleaseYear'])}  
                **Ventas:** {fila['SalesMillions']} millones  
                **Serie:** {fila['Series']}  
                """
            )
            st.write("---")

    st.divider()

    st.subheader("🧠 ¿Cómo funciona este sistema de recomendación?")

    st.write(
        """
        Este sistema utiliza un método basado en filtros de contenido.
        Es decir, recomienda videojuegos que coinciden con las preferencias seleccionadas por el usuario.

        Los criterios utilizados son:

        - Plataforma del videojuego.
        - Serie o franquicia.
        - Desarrollador.
        - Ventas mínimas.
        - Año mínimo de lanzamiento.

        Luego, los resultados se ordenan de mayor a menor según sus ventas en millones.
        """
    )