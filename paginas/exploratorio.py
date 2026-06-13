import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


@st.cache_data
def cargar_dataset():
    ruta_base = Path(__file__).resolve().parent.parent
    ruta_archivo = ruta_base / "data" / "best_selling_video_games_limpio.xlsx"

    df = pd.read_excel(ruta_archivo)
    return df


def mostrar_exploratorio():
    st.title("Análisis Exploratorio de Datos")
    st.write(
        """
        En esta sección se realiza un análisis exploratorio del dataset de videojuegos más vendidos.
        Aquí se puede revisar la descripción del dataset, analizar campos específicos, navegar los datos,
        buscar registros, generar gráficos y validar hipótesis.
        """
    )

    try:
        df = cargar_dataset()
    except Exception as e:
        st.error("No se pudo cargar el dataset.")
        st.write("Error:", e)
        return

    submenu = st.sidebar.selectbox(
        "Submenú de Análisis Exploratorio",
        [
            "Descripción del dataset",
            "Descripción de los campos",
            "Navegador del dataset completo",
            "Buscador de registros",
            "Graficador exploratorio",
            "Hipótesis"
        ]
    )

    if submenu == "Descripción del dataset":
        st.header("Descripción del dataset")

        st.write(
            """
            Este dataset contiene información sobre algunos de los videojuegos más vendidos a nivel mundial.
            Incluye datos como el ranking, nombre del videojuego, plataforma, desarrollador, publicador,
            año de lanzamiento, ventas en millones y serie o franquicia a la que pertenece.
            """
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total de registros", df.shape[0])
        col2.metric("Total de columnas", df.shape[1])
        col3.metric("Ventas máximas", f"{df['SalesMillions'].max():.2f} M")
        col4.metric("Ventas promedio", f"{df['SalesMillions'].mean():.2f} M")

        st.subheader("Primeras filas del dataset")
        st.dataframe(df.head(10), use_container_width=True)

        st.subheader("Tipos de datos")
        tipos = pd.DataFrame({
            "Campo": df.columns,
            "Tipo de dato": df.dtypes.astype(str).values,
            "Valores vacíos": df.isnull().sum().values
        })

        st.dataframe(tipos, use_container_width=True)

    elif submenu == "Descripción de los campos":
        st.header("Descripción de los campos")

        descripciones = {
            "Rank": "Posición del videojuego dentro del ranking de ventas.",
            "Title": "Nombre del videojuego.",
            "Platform": "Plataforma o plataformas donde el videojuego está disponible.",
            "Developer": "Empresa o estudio que desarrolló el videojuego.",
            "Publisher": "Empresa encargada de publicar o distribuir el videojuego.",
            "ReleaseYear": "Año de lanzamiento del videojuego.",
            "SalesMillions": "Cantidad de ventas del videojuego expresada en millones.",
            "Series": "Serie, saga o franquicia a la que pertenece el videojuego.",
            "TableNumber": "Número de tabla o identificador interno del dataset."
        }

        campo = st.selectbox("Seleccione un campo:", df.columns)

        st.subheader(f"Campo seleccionado: {campo}")

        if campo in descripciones:
            st.write("**Descripción:**", descripciones[campo])
        else:
            st.write("No hay descripción registrada para este campo.")

        if pd.api.types.is_numeric_dtype(df[campo]):
            st.write("### Medidas estadísticas")
            st.dataframe(df[campo].describe().to_frame(), use_container_width=True)

            col1, col2, col3 = st.columns(3)
            col1.metric("Media", f"{df[campo].mean():.2f}")
            col2.metric("Mínimo", f"{df[campo].min():.2f}")
            col3.metric("Máximo", f"{df[campo].max():.2f}")

        else:
            st.write("### Valores posibles del campo")
            valores = df[campo].dropna().unique()
            st.write(f"Total de valores diferentes: **{len(valores)}**")
            st.dataframe(pd.DataFrame(valores, columns=[campo]), use_container_width=True)

            st.write("### Frecuencia de valores")
            frecuencia = df[campo].value_counts().reset_index()
            frecuencia.columns = [campo, "Cantidad"]
            st.dataframe(frecuencia, use_container_width=True)

    elif submenu == "Navegador del dataset completo":
        st.header("Navegador del dataset completo")

        st.write("En esta sección se puede visualizar el dataset completo de forma interactiva.")

        filas = st.slider(
            "Cantidad de filas a mostrar:",
            min_value=5,
            max_value=len(df),
            value=min(20, len(df))
        )

        st.dataframe(df.head(filas), use_container_width=True)

        st.write("### Dataset completo")
        st.dataframe(df, use_container_width=True)

    elif submenu == "Buscador de registros":
        st.header("Buscador de registros")

        st.write(
            """
            Este buscador permite encontrar videojuegos por nombre, ranking, plataforma,
            desarrollador o publicador.
            """
        )

        busqueda = st.text_input("Escriba el dato que desea buscar:")

        if busqueda:
            resultado = df[
                df.astype(str).apply(
                    lambda fila: fila.str.contains(busqueda, case=False, na=False).any(),
                    axis=1
                )
            ]

            st.write(f"Resultados encontrados: **{resultado.shape[0]}**")

            if not resultado.empty:
                st.dataframe(resultado, use_container_width=True)
            else:
                st.warning("No se encontraron registros con ese dato.")
        else:
            st.info("Escriba un texto para buscar dentro del dataset.")

    elif submenu == "Graficador exploratorio":
        st.header("Graficador exploratorio")

        st.write(
            """
            En esta sección se puede seleccionar un campo del dataset y generar un gráfico adecuado
            según el tipo de dato.
            """
        )

        campo = st.selectbox("Seleccione el campo que desea graficar:", df.columns)

        st.subheader(f"Gráfico del campo: {campo}")

        fig, ax = plt.subplots()

        if pd.api.types.is_numeric_dtype(df[campo]):
            ax.hist(df[campo].dropna(), bins=10)
            ax.set_xlabel(campo)
            ax.set_ylabel("Frecuencia")
            ax.set_title(f"Distribución de {campo}")
            st.pyplot(fig)

            st.write(
                """
                Este gráfico muestra cómo se distribuyen los valores numéricos del campo seleccionado.
                Permite observar si los datos se concentran en ciertos rangos o si existen valores muy altos o bajos.
                """
            )

        else:
            conteo = df[campo].value_counts().head(10)

            ax.bar(conteo.index.astype(str), conteo.values)
            ax.set_xlabel(campo)
            ax.set_ylabel("Cantidad")
            ax.set_title(f"Top 10 valores de {campo}")
            plt.xticks(rotation=45, ha="right")
            st.pyplot(fig)

            st.write(
                """
                Este gráfico muestra los valores más frecuentes del campo seleccionado.
                Es útil para analizar variables categóricas como plataformas, desarrolladores o series.
                """
            )

    elif submenu == "Hipótesis":
        st.header("Hipótesis del análisis")

        hipotesis = st.selectbox(
            "Seleccione una hipótesis:",
            [
                "Hipótesis 1: Los videojuegos con mayores ventas pertenecen a franquicias conocidas",
                "Hipótesis 2: Los videojuegos más antiguos no necesariamente tienen mayores ventas"
            ]
        )

        if hipotesis == "Hipótesis 1: Los videojuegos con mayores ventas pertenecen a franquicias conocidas":
            st.subheader("Hipótesis 1")
            st.write(
                """
                **Planteamiento:** Los videojuegos con mayores ventas pertenecen principalmente a series
                o franquicias reconocidas.
                """
            )

            top_ventas = df.sort_values(by="SalesMillions", ascending=False).head(10)

            st.write("### Top 10 videojuegos con mayores ventas")
            st.dataframe(
                top_ventas[["Title", "Series", "SalesMillions"]],
                use_container_width=True
            )

            fig, ax = plt.subplots()
            ax.bar(top_ventas["Title"], top_ventas["SalesMillions"])
            ax.set_xlabel("Videojuego")
            ax.set_ylabel("Ventas en millones")
            ax.set_title("Top 10 videojuegos más vendidos")
            plt.xticks(rotation=45, ha="right")
            st.pyplot(fig)

            st.success(
                """
                **Conclusión:** La hipótesis se valida parcialmente, ya que varios de los videojuegos
                con mayores ventas pertenecen a franquicias o series conocidas, como Minecraft, Grand Theft Auto,
                Mario, Pokémon o Wii. Esto demuestra que una franquicia reconocida puede influir positivamente
                en las ventas.
                """
            )

        elif hipotesis == "Hipótesis 2: Los videojuegos más antiguos no necesariamente tienen mayores ventas":
            st.subheader("Hipótesis 2")
            st.write(
                """
                **Planteamiento:** El año de lanzamiento no determina por sí solo que un videojuego tenga
                mayores ventas.
                """
            )

            df_ordenado = df.sort_values(by="ReleaseYear")

            st.write("### Relación entre año de lanzamiento y ventas")
            st.dataframe(
                df[["Title", "ReleaseYear", "SalesMillions"]].sort_values(
                    by="SalesMillions",
                    ascending=False
                ).head(15),
                use_container_width=True
            )

            fig, ax = plt.subplots()
            ax.scatter(df_ordenado["ReleaseYear"], df_ordenado["SalesMillions"])
            ax.set_xlabel("Año de lanzamiento")
            ax.set_ylabel("Ventas en millones")
            ax.set_title("Relación entre año de lanzamiento y ventas")
            st.pyplot(fig)

            correlacion = df["ReleaseYear"].corr(df["SalesMillions"])

            st.metric("Correlación entre año y ventas", f"{correlacion:.2f}")

            st.success(
                """
                **Conclusión:** La hipótesis se valida, porque se observa que no todos los videojuegos
                antiguos tienen mayores ventas. Existen videojuegos recientes con ventas muy altas y también
                videojuegos antiguos que mantienen un buen nivel de ventas. Por lo tanto, el éxito en ventas
                depende de varios factores, no solo del año de lanzamiento.
                """
            )