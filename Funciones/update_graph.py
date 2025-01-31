import os
import json
import glob
import subprocess

# Ruta del grafo
GRAPH_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Grafo_Path.json'))  # Guardar en el directorio principal

# Directorio de la carpeta de conocimiento
KNOWLEDGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Conocimiento'))

# Crear grafo basado en archivos
def generate_knowledge_graph():
    graph = {
        "nodes": [],
        "edges": []
    }
    
    # Verificar si el directorio de conocimiento existe
    if not os.path.exists(KNOWLEDGE_DIR):
        print(f"El directorio {KNOWLEDGE_DIR} no existe.")
        return
    
    # Obtener lista de archivos en la carpeta de conocimiento
    files = glob.glob(os.path.join(KNOWLEDGE_DIR, "*"))
    print(f"Archivos encontrados en {KNOWLEDGE_DIR}: {files}")
    
    for file_path in files:
        file_name = os.path.basename(file_path)
        node = {
            "id": file_name,
            "path": os.path.relpath(file_path, os.path.dirname(GRAPH_FILE)).replace("\\", "/")  # Asegurar que las rutas usen barras normales
        }
        graph["nodes"].append(node)
    
    print(f"Nodos generados: {graph['nodes']}")

    # Guardar el grafo en formato JSON
    try:
        with open(GRAPH_FILE, "w", encoding="utf-8") as graph_file:
            json.dump(graph, graph_file, indent=4, ensure_ascii=False)
        print(f"Grafo actualizado y guardado en {os.path.abspath(GRAPH_FILE)}")
    except Exception as e:
        print(f"Error al guardar el archivo JSON: {e}")

# Actualizar el repositorio automáticamente
def git_commit_and_push():
    try:
        subprocess.run(["git", "add", "--all"], check=True)
        
        # Verificar si hay cambios para hacer commit
        result = subprocess.run(["git", "diff", "--cached", "--exit-code"], check=False)
        if result.returncode == 0:
            print("No hay cambios para hacer commit.")
            return
        
        subprocess.run(["git", "commit", "-m", "Actualización automática del grafo"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Cambios enviados a GitHub con éxito.")
    except subprocess.CalledProcessError as e:
        print("Error al hacer commit/push: ", e)

if __name__ == "__main__":
    generate_knowledge_graph()
    git_commit_and_push()