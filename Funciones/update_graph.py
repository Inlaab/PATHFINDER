import os
import json
import glob
import subprocess

# Ruta del archivo de grafo
GRAPH_FILE = "Grafo_Path.json"

# Directorio de la carpeta de conocimiento
KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "..", "Conocimiento")

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
    generate_knowledge_graph()
    # git_commit_and_push()
