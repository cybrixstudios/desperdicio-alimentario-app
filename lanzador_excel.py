
import subprocess
import webbrowser
import time

# Iniciar servidor de Streamlit en segundo plano
subprocess.Popen(["streamlit", "run", "app_excel_comparador_export.py"])

# Esperar unos segundos para que el servidor arranque
time.sleep(3)

# Abrir navegador en la dirección local
webbrowser.open("http://localhost:8501")
