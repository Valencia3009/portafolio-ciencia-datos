import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def leer_archivo(archivo):
    nombre = archivo.name.lower()

    if nombre.endswith(".csv"):
        try:
            df = pd.read_csv(archivo)
        except:
            archivo.seek(0)
            df = pd.read_csv(archivo, sep=";")
        return df

    elif nombre.endswith(".xlsx") or nombre.endswith(".xls"):
        df = pd.read_excel(archivo)
        return df

    else:
        return None


def mostrar_carga_archivos():
    st.title("Análisis de Datos por Carga de Archivos")

    st.write(
        """
        En esta sección el usuario puede cargar un archivo desde su computadora
        en formato CSV o Excel. Luego la aplicación muestra información general
        del archivo y permite generar un gráfico exploratorio.
        """
    )

    st.divider()

    archivo = st.file_uploader(
        "Seleccione un archivo CSV o Excel:",
        type=["csv", "xlsx", "xls"]
    )

    if archivo is None:
        st.info("Sube un archivo para comenzar el análisis.")
        return

    try:
        df = leer_archivo(archivo)

        if df is None:
            st.error("Formato de archivo no compatible.")
            return

    except Exception as e:
        st.error("No se pudo leer el archivo.")
        st.write("Error:", e)
        return

    st.success("Archivo cargado correctamente.")

    st.divider()

    st.subheader("Información general del archivo")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total de filas", df.shape[0])
    col2.metric("Total de columnas", df.shape[1])
    col3.metric("Celdas vacías", int(df.isnull().sum().sum()))

    st.subheader("Vista previa del archivo")
    st.dataframe(df.head(10), use_container_width=True)

    st.subheader("Tipos de datos")
    tipos = pd.DataFrame({
        "Campo": df.columns,
        "Tipo de dato": df.dtypes.astype(str).values,
        "Valores vacíos": df.isnull().sum().values
    })

    st.dataframe(tipos, use_container_width=True)

    st.divider()

    st.subheader("Generador de gráficos")

    columnas = df.columns.tolist()

    columna = st.selectbox(
        "Seleccione una columna para graficar:",
        columnas
    )

    fig, ax = plt.subplots()

    if pd.api.types.is_numeric_dtype(df[columna]):
        st.write("La columna seleccionada es numérica, por eso se genera un histograma.")

        ax.hist(df[columna].dropna(), bins=10)
        ax.set_xlabel(columna)
        ax.set_ylabel("Frecuencia")
        ax.set_title(f"Distribución de {columna}")

        st.pyplot(fig)

        st.write("### Estadísticas de la columna")
        st.dataframe(df[columna].describe().to_frame(), use_container_width=True)

    else:
        st.write("La columna seleccionada es categórica, por eso se genera un gráfico de barras.")

        conteo = df[columna].dropna().astype(str).value_counts().head(10)

        ax.bar(conteo.index, conteo.values)
        ax.set_xlabel(columna)
        ax.set_ylabel("Cantidad")
        ax.set_title(f"Top 10 valores de {columna}")
        plt.xticks(rotation=45, ha="right")

        st.pyplot(fig)

        st.write("### Frecuencia de valores")
        frecuencia = conteo.reset_index()
        frecuencia.columns = [columna, "Cantidad"]
        st.dataframe(frecuencia, use_container_width=True)

    st.divider()

    st.subheader("Conclusión")

    st.write(
        """
        Esta sección permite cargar archivos externos y realizar un análisis básico
        de forma automática. Esto facilita explorar rápidamente un conjunto de datos
        sin necesidad de modificar el código fuente de la aplicación.
        """
    )