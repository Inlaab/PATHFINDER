import os
import json
import glob
import subprocess
import csv
import unicodedata
import re

# Ruta del archivo de grafo
GRAPH_FILE = "Grafo_Path.json"

# Directorio de la carpeta de conocimiento
KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "..", "Conocimiento")

def normalize_filename(filename):
    """
    Normaliza el nombre del archivo eliminando tildes y caracteres especiales.
    """
    # Eliminar acentos y normalizar caracteres
    nfkd_form = unicodedata.normalize('NFKD', filename)
    normalized_name = u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
    # Remover cualquier carácter no permitido en nombres de archivo
    return re.sub(r'[^a-zA-Z0-9._\-]', '_', normalized_name)

def rename_files_in_knowledge_dir():
    """
    Renombra archivos en el directorio de conocimiento para normalizar sus nombres.
    """
    for root, _, files in os.walk(KNOWLEDGE_DIR):
        for file in files:
            normalized_name = normalize_filename(file)
            if file != normalized_name:
                original_path = os.path.join(root, file)
                new_path = os.path.join(root, normalized_name)
                os.rename(original_path, new_path)
                print(f"Renombrado: {original_path} a {new_path}")

def convert_csv_to_md(csv_path):
    """
    Convierte un archivo CSV a Markdown para su inclusión en el grafo.
    """
    md_path = csv_path.replace(".csv", ".md")
    with open(csv_path, "r", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file)
        with open(md_path, "w", encoding="utf-8") as md_file:
            for row in csv_reader:
                md_file.write("| " + " | ".join(row) + " |\n")
    print(f"Convertido {csv_path} a {md_path}")

def convert_all_csv_to_md():
    """
    Busca y convierte todos los archivos CSV dentro del directorio de conocimiento.
    """
    csv_files = glob.glob(os.path.join(KNOWLEDGE_DIR, "**/*.csv"), recursive=True)
    for csv_file in csv_files:
        convert_csv_to_md(csv_file)

# Crear grafo basado en archivos
def generate_knowledge_graph():
    graph = {
        "nodes": [],
        "edges": []
    }

    # Obtener lista de todos los archivos en la carpeta de conocimiento
    files = glob.glob(os.path.join(KNOWLEDGE_DIR, "**"), recursive=True)

    for file_path in files:
        # Validar si es un archivo regular
        if os.path.isfile(file_path):
            file_name = os.path.basename(file_path)
            relative_path = os.path.relpath(file_path, os.path.dirname(__file__))
            node = {
                "id": file_name,
                "path": relative_path
            }
            graph["nodes"].append(node)

    # Guardar el grafo en formato JSON en la raíz del repositorio
    graph_output_path = os.path.join(os.path.dirname(__file__), "..", GRAPH_FILE)
    with open(graph_output_path, "w", encoding="utf-8") as graph_file:
        json.dump(graph, graph_file, indent=4, ensure_ascii=False)

    print(f"Grafo actualizado y guardado en {graph_output_path}")

# Actualizar el repositorio automáticamente
def git_commit_and_push():
    try:
        subprocess.run(["git", "add", "--all"], check=True)
        subprocess.run(["git", "commit", "-m", "Actualización automática del grafo"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Cambios enviados a GitHub con éxito.")
    except subprocess.CalledProcessError as e:
        print("Error al hacer commit/push: ", e)

if __name__ == "__main__":
    # Normalizar nombres de archivo eliminando tildes
    rename_files_in_knowledge_dir()
    # Convertir archivos CSV a Markdown antes de generar el grafo
    convert_all_csv_to_md()
    generate_knowledge_graph()
    # git_commit_and_push()
