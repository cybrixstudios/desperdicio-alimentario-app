

import streamlit as st
import pdfplumber
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import io
from fpdf import FPDF

st.set_page_config(page_title="Comparador PDF con exportación", layout="wide")
st.title("📄 Comparador de Desperdicio Alimentario desde archivos PDF")

st.sidebar.header("Sube los archivos PDF para comparar")
pdf_2018 = st.sidebar.file_uploader("Archivo PDF Año 1 (Ej: 2018)", type=["pdf"])
pdf_2023 = st.sidebar.file_uploader("Archivo PDF Año 2 (Ej: 2023)", type=["pdf"])

def extraer_datos_pdf(pdf_file):
    datos = {
        "Total desperdiciado": None,
        "Productos sin utilizar": None,
        "Recetas": None
    }

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            total = re.search(r"total de alimentos desperdiciados.*?([0-9\.,]+)\s*kg", text, re.IGNORECASE)
            productos = re.search(r"productos sin utilizar.*?([0-9\.,]+)\s*kg", text, re.IGNORECASE)
            recetas = re.search(r"recetas.*?([0-9\.,]+)\s*kg", text, re.IGNORECASE)

            if total:
                datos["Total desperdiciado"] = float(total.group(1).replace(".", "").replace(",", "."))
            if productos:
                datos["Productos sin utilizar"] = float(productos.group(1).replace(".", "").replace(",", "."))
            if recetas:
                datos["Recetas"] = float(recetas.group(1).replace(".", "").replace(",", "."))

    return datos

if pdf_2018 and pdf_2023:
    datos_2018 = extraer_datos_pdf(pdf_2018)
    datos_2023 = extraer_datos_pdf(pdf_2023)

    df = pd.DataFrame({
        "Categoría": ["Total desperdiciado", "Productos sin utilizar", "Recetas"],
        "Año1": [datos_2018["Total desperdiciado"], datos_2018["Productos sin utilizar"], datos_2018["Recetas"]],
        "Año2": [datos_2023["Total desperdiciado"], datos_2023["Productos sin utilizar"], datos_2023["Recetas"]]
    })

    df["Cambio (%)"] = ((df["Año2"] - df["Año1"]) / df["Año1"]) * 100

    st.subheader("📊 Comparación de datos extraídos")
    st.dataframe(df)

    # Gráfico
    df_plot = df.melt(id_vars="Categoría", value_vars=["Año1", "Año2"], var_name="Año", value_name="Kg")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=df_plot, x="Categoría", y="Kg", hue="Año", ax=ax)
    plt.title("Comparación de desperdicio alimentario por categoría")
    plt.xticks(rotation=20)
    st.pyplot(fig)

    # Exportar gráfico como imagen PNG
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    st.download_button("⬇️ Descargar gráfico como PNG", buf.getvalue(), file_name="grafico_comparacion.png", mime="image/png")

    # Exportar tabla como Excel
    excel_buf = io.BytesIO()
    with pd.ExcelWriter(excel_buf, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="Comparacion")
    st.download_button("⬇️ Descargar datos como Excel", excel_buf.getvalue(), file_name="comparacion_datos.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Exportar informe como PDF (simple con texto + tabla)
    def generar_pdf(df):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Informe de comparación de desperdicio alimentario", ln=True, align='C')
        pdf.ln(10)
        for i, row in df.iterrows():
            texto = f"{row['Categoría']}: Año1 = {row['Año1']:.2f} kg, Año2 = {row['Año2']:.2f} kg, Cambio = {row['Cambio (%)']:.2f}%"
            pdf.cell(0, 10, txt=texto, ln=True)
        output = io.BytesIO()
        pdf.output(output)
        return output.getvalue()

    pdf_bytes = generar_pdf(df)
    st.download_button("⬇️ Descargar informe como PDF", pdf_bytes, file_name="informe_comparacion.pdf", mime="application/pdf")

    st.success("✅ Comparación realizada con opciones de descarga.")
else:
    st.info("⬅️ Por favor sube los dos archivos PDF para comenzar.")
