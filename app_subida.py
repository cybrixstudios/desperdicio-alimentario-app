
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Comparador de Desperdicio Alimentario", layout="wide")
st.title("📊 Comparador de Desperdicio Alimentario entre dos archivos Excel")

st.sidebar.header("Sube los archivos Excel a comparar")

archivo_2018 = st.sidebar.file_uploader("Archivo Excel Año 1 (por ejemplo 2018)", type=["xlsx"])
archivo_2023 = st.sidebar.file_uploader("Archivo Excel Año 2 (por ejemplo 2023)", type=["xlsx"])

if archivo_2018 and archivo_2023:
    xls_2018 = pd.ExcelFile(archivo_2018)
    xls_2023 = pd.ExcelFile(archivo_2023)

    st.sidebar.subheader("Selecciona tipo de comparación")

    # Buscar hojas comunes
    hojas_comunes = list(set(xls_2018.sheet_names).intersection(set(xls_2023.sheet_names)))
    hoja = st.sidebar.selectbox("Seleccionar hoja común para comparar", hojas_comunes)

    df18 = pd.read_excel(archivo_2018, sheet_name=hoja)
    df23 = pd.read_excel(archivo_2023, sheet_name=hoja)

    st.subheader(f"📄 Comparación de hoja: {hoja}")

    claves = ["Producto", "Receta", "Categoría", "Item", "Grupo", "Descripción"]
    col_key = None
    for col in df18.columns:
        if any(k.lower() in str(col).lower() for k in claves) and col in df23.columns:
            col_key = col
            break

    if col_key:
        df18 = df18.rename(columns={col_key: "Item"})
        df23 = df23.rename(columns={col_key: "Item"})

        num_col_18 = df18.select_dtypes(include="number").columns[0]
        num_col_23 = df23.select_dtypes(include="number").columns[0]

        df18 = df18[["Item", num_col_18]].dropna()
        df23 = df23[["Item", num_col_23]].dropna()
        df18.columns = ["Item", "Año1"]
        df23.columns = ["Item", "Año2"]

        df = pd.merge(df18, df23, on="Item", how="inner")
        df["Cambio (%)"] = ((df["Año2"] - df["Año1"]) / df["Año1"]) * 100

        st.dataframe(df)

        df_plot = df.melt(id_vars="Item", value_vars=["Año1", "Año2"], var_name="Año", value_name="Kg")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=df_plot, x="Item", y="Kg", hue="Año", ax=ax)
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig)

        st.success("✅ Comparación realizada correctamente.")
    else:
        st.warning("⚠️ No se encontró una columna clave común para comparar.")
else:
    st.info("Por favor, sube los dos archivos Excel para comenzar.")
