import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


@st.cache_data
def cargar_dataset():
    ruta_base = Path(__file__).resolve().parent.parent
    ruta_archivo = ruta_base / "data" / "best_selling_video_games_limpio.xlsx"

    df = pd.read_excel(ruta_archivo)
    return df


def mostrar_aprendizaje():
    st.title("🤖 Aprendizaje Automático")
    st.write(
        """
        En esta sección se aplican algoritmos de aprendizaje automático para analizar
        la relación entre variables del dataset de videojuegos más vendidos.
        """
    )

    try:
        df = cargar_dataset()
    except Exception as e:
        st.error("No se pudo cargar el dataset.")
        st.write("Error:", e)
        return

    st.divider()

    st.subheader("⚙️ Configuración del modelo")

    variables_numericas = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    if len(variables_numericas) < 2:
        st.warning("El dataset necesita por lo menos dos variables numéricas para aplicar aprendizaje automático.")
        return

    algoritmo = st.selectbox(
        "Seleccione el algoritmo:",
        [
            "Regresión Lineal",
            "Árbol de Decisión Regresor"
        ]
    )

    variable_independiente = st.selectbox(
        "Seleccione la variable independiente (X):",
        variables_numericas
    )

    opciones_dependientes = [col for col in variables_numericas if col != variable_independiente]

    variable_dependiente = st.selectbox(
        "Seleccione la variable a analizar o predecir (Y):",
        opciones_dependientes
    )

    porcentaje_entrenamiento = st.slider(
        "Porcentaje de datos para entrenamiento:",
        min_value=50,
        max_value=90,
        value=70,
        step=5
    )

    porcentaje_prueba = 100 - porcentaje_entrenamiento

    col1, col2 = st.columns(2)
    col1.metric("Datos de entrenamiento", f"{porcentaje_entrenamiento}%")
    col2.metric("Datos de prueba", f"{porcentaje_prueba}%")

    st.divider()

    datos_modelo = df[[variable_independiente, variable_dependiente]].dropna()

    X = datos_modelo[[variable_independiente]]
    y = datos_modelo[variable_dependiente]

    if len(datos_modelo) < 5:
        st.warning("No hay suficientes datos para entrenar el modelo.")
        return

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        train_size=porcentaje_entrenamiento / 100,
        random_state=42
    )

    if algoritmo == "Regresión Lineal":
        modelo = LinearRegression()
    else:
        modelo = DecisionTreeRegressor(random_state=42)

    modelo.fit(X_train, y_train)

    predicciones = modelo.predict(X_test)

    mae = mean_absolute_error(y_test, predicciones)
    mse = mean_squared_error(y_test, predicciones)
    r2 = r2_score(y_test, predicciones)

    st.subheader("📊 Resultados del modelo")

    col1, col2, col3 = st.columns(3)
    col1.metric("MAE", f"{mae:.2f}")
    col2.metric("MSE", f"{mse:.2f}")
    col3.metric("R²", f"{r2:.2f}")

    if algoritmo == "Regresión Lineal":
        coeficiente = modelo.coef_[0]
        intercepto = modelo.intercept_

        col4, col5 = st.columns(2)
        col4.metric("Coeficiente", f"{coeficiente:.2f}")
        col5.metric("Intercepto", f"{intercepto:.2f}")
    else:
        st.metric("Profundidad del árbol", modelo.get_depth())

    st.divider()

    st.subheader("📈 Gráfica de entrenamiento y predicción")

    fig, ax = plt.subplots()

    ax.scatter(
        X_train[variable_independiente],
        y_train,
        label="Datos de entrenamiento"
    )

    ax.scatter(
        X_test[variable_independiente],
        y_test,
        label="Datos reales de prueba"
    )

    ax.scatter(
        X_test[variable_independiente],
        predicciones,
        label="Predicciones"
    )

    ax.set_xlabel(variable_independiente)
    ax.set_ylabel(variable_dependiente)
    ax.set_title(f"{algoritmo}: {variable_dependiente} según {variable_independiente}")
    ax.legend()

    st.pyplot(fig)

    st.divider()

    st.subheader("🧾 Tabla comparativa de resultados")

    resultados = X_test.copy()
    resultados["Valor real"] = y_test.values
    resultados["Predicción"] = predicciones
    resultados["Diferencia"] = resultados["Valor real"] - resultados["Predicción"]

    st.dataframe(resultados, use_container_width=True)

    st.divider()

    st.subheader("✅ Interpretación")

    if variable_dependiente == "SalesMillions":
        st.write(
            """
            En este caso, el modelo intenta predecir las ventas en millones de los videojuegos
            a partir de la variable independiente seleccionada. Esto permite observar si existe
            una relación entre esa variable y el nivel de ventas.
            """
        )
    else:
        st.write(
            """
            El modelo analiza la relación entre las variables seleccionadas y genera predicciones
            con base en los datos de entrenamiento.
            """
        )

    if r2 >= 0.7:
        st.success(
            """
            El valor de R² indica que el modelo tiene un buen nivel de ajuste para los datos seleccionados.
            Esto significa que la variable independiente explica una parte importante del comportamiento
            de la variable dependiente.
            """
        )
    elif r2 >= 0.3:
        st.info(
            """
            El valor de R² indica que el modelo tiene un ajuste moderado. La variable independiente
            ayuda a explicar parte del comportamiento de la variable dependiente, pero no completamente.
            """
        )
    else:
        st.warning(
            """
            El valor de R² indica que el modelo tiene un ajuste bajo. Esto significa que la variable
            independiente seleccionada no explica de forma fuerte el comportamiento de la variable dependiente.
            """
        )