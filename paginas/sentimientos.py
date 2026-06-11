import streamlit as st
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob


def analizar_sentimiento(texto):
    blob = TextBlob(texto)
    polaridad = blob.sentiment.polarity

    if polaridad >= 0:
        sentimiento = "Positivo"
    else:
        sentimiento = "Negativo"

    return polaridad, sentimiento


def extraer_textos_web(url, tipo_texto):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code != 200:
        return None, f"No se pudo acceder a la página. Código: {response.status_code}"

    soup = BeautifulSoup(response.text, "html.parser")

    textos = []

    if tipo_texto == "Párrafos":
        elementos = soup.find_all("p")
    elif tipo_texto == "Títulos":
        elementos = soup.find_all(["h1", "h2", "h3"])
    else:
        elementos = soup.find_all(["p", "h1", "h2", "h3"])

    for elemento in elementos:
        texto = elemento.get_text(strip=True)

        if texto and len(texto) > 30:
            textos.append(texto)

    return textos, None


def mostrar_sentimientos():
    st.title("💬 Análisis de Sentimientos y Scraping")

    st.write(
        """
        En esta sección se realiza scraping de texto desde una página web y luego
        se aplica un análisis de sentimientos para clasificar los textos como positivos,
        negativos o neutros.
        """
    )

    st.divider()

    st.subheader("🌐 Extracción de opiniones o textos desde una página web")

    url = st.text_input(
        "Ingrese la URL del sitio web:",
        value="https://es.wikipedia.org/wiki/Historia_de_los_videojuegos"
    )

    tipo_texto = st.selectbox(
        "Seleccione el tipo de texto que desea extraer:",
        [
            "Párrafos",
            "Títulos",
            "Párrafos y títulos"
        ]
    )

    cantidad = st.slider(
        "Cantidad máxima de textos a analizar:",
        min_value=1,
        max_value=20,
        value=10
    )

    if st.button("Extraer y analizar textos"):
        if not url.strip():
            st.warning("Debe ingresar una URL válida.")
            return

        try:
            with st.spinner("Extrayendo información de la página web..."):
                textos, error = extraer_textos_web(url, tipo_texto)

            if error:
                st.error(error)
                return

            if not textos:
                st.warning("No se encontraron textos suficientes para analizar.")
                return

            textos = textos[:cantidad]

            st.success(f"Se extrajeron {len(textos)} textos para analizar.")

            resultados = []

            for i, texto in enumerate(textos, start=1):
                polaridad, sentimiento = analizar_sentimiento(texto)

                resultados.append({
                    "N°": i,
                    "Texto": texto,
                    "Polaridad": round(polaridad, 3),
                    "Sentimiento": sentimiento
                })

            st.divider()

            st.subheader("📋 Opiniones o textos leídos")

            for item in resultados:
                st.markdown(f"### Texto {item['N°']}")
                st.write(item["Texto"])
                st.write(f"**Polaridad:** {item['Polaridad']}")
                st.write(f"**Sentimiento detectado:** {item['Sentimiento']}")
                st.write("---")

            st.subheader("📊 Resumen del análisis de sentimientos")

            positivos = sum(1 for item in resultados if item["Sentimiento"] == "Positivo")
            negativos = sum(1 for item in resultados if item["Sentimiento"] == "Negativo")

            col1, col2 = st.columns(2)

            col1.metric("Positivos", positivos)
            col2.metric("Negativos", negativos)

            resumen = {
                "Sentimiento": ["Positivo", "Negativo"],
                "Cantidad": [positivos, negativos]
            }

            import pandas as pd
            import matplotlib.pyplot as plt

            df_resumen = pd.DataFrame(resumen)

            fig, ax = plt.subplots()
            ax.bar(df_resumen["Sentimiento"], df_resumen["Cantidad"])
            ax.set_xlabel("Sentimiento")
            ax.set_ylabel("Cantidad")
            ax.set_title("Resumen de sentimientos detectados")

            st.pyplot(fig)

            st.dataframe(df_resumen, use_container_width=True)

            st.divider()

            st.subheader("✅ Conclusión")

            sentimiento_dominante = df_resumen.sort_values(
                by="Cantidad",
                ascending=False
            ).iloc[0]["Sentimiento"]

            st.write(
                f"""
                Según los textos extraídos de la página web, el sentimiento que más se repite es
                **{sentimiento_dominante}**. Esto permite tener una idea general del tono del contenido
                analizado, aunque el resultado puede variar dependiendo del sitio web y del tipo de texto
                seleccionado.
                """
            )

        except requests.exceptions.MissingSchema:
            st.error("La URL no es válida. Debe iniciar con `http://` o `https://`.")
        except Exception as e:
            st.error("Ocurrió un error al procesar la página.")
            st.write("Error:", e)