# Comparador de Desperdicio Alimentario (PDF)

Esta app permite comparar informes de desperdicio alimentario en formato PDF (por ejemplo, los del Ministerio de Agricultura de España) entre dos años distintos.

## Funciones:

- 📄 Subida de 2 archivos PDF
- 📊 Comparación de datos clave (total, productos sin utilizar, recetas)
- 📈 Gráfico comparativo
- 💾 Exportar:
  - Gráfico como PNG
  - Tabla como Excel
  - Informe como PDF

## Cómo ejecutarlo localmente

```bash
pip install -r requirements.txt
streamlit run app_pdf_export.py
```

## Despliegue en Streamlit Cloud

1. Sube este repositorio a GitHub.
2. Ve a [https://streamlit.io/cloud](https://streamlit.io/cloud).
3. Selecciona este repositorio y archivo `app_pdf_export.py`.
4. ¡Tu app estará en línea!