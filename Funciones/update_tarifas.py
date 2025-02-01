import os
import re

# Ruta del archivo
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Conocimiento', 'Tarifas_Ciencuadras_2025.md'))

# Leer el contenido del archivo
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Reemplazar las barras verticales en las tarifas por puntos
updated_content = re.sub(r'(\$\s*\d+)\s*\|\s*(\d+)\s*\|', r'\1.\2', content)

# Guardar el contenido actualizado en el archivo
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(updated_content)

print(f"Archivo actualizado y guardado en {file_path}")