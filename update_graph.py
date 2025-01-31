import os
import json
import glob
import subprocess

# Ruta del grafo
GRAPH_FILE = "Grafo_Path.json"  # Guardar en el directorio principal

# Directorio de la carpeta de conocimiento
KNOWLEDGE_DIR = "Conocimiento"

# Crear grafo basado en archivos
def generate_knowledge_graph():
    graph = {
        "nodes": [],
        "edges": []
    }
    
    # Obtener lista de archivos en la carpeta de conocimiento
    files = glob.glob(os.path.join(KNOWLEDGE_DIR, "*"))
    
    for file_path in files:
        file_name = os.path.basename(file_path)
        node = {
            "id": file_name,
            "path": file_path
        }
        graph["nodes"].append(node)

    # Guardar el grafo en formato JSON
    with open(GRAPH_FILE, "w", encoding="utf-8") as graph_file:
        json.dump(graph, graph_file, indent=4, ensure_ascii=False)

    print(f"Grafo actualizado y guardado en {os.path.abspath(GRAPH_FILE)}")

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
