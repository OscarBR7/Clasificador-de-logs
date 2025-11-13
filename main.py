from utils.cliente_gemini import GeminiClient
import os
import json

# Lista de etiquetas permitidas
TAXONOMIA = [
  "sql_query",
  "data_retrieval",
  "update_operation",
  "permission_denied",
  "timeout_error",
  "slow_query",
  "diagnostic",
  "semantic_retrieval",
  "malformed_input",
  "version_check",
  "cleanup_operation",
  "file_not_found",
  "user_instruction",
  "llm_response"
]

#Función para leer el archivo logs.txt
def leer_archivo_logs(archivo_logs):
  '''Se abre el archivo logs.txt, y se lee su contenido para retornarlo
  y poder dividirlo en bloques posteriormente.'''
  with open(archivo_logs, 'r', encoding='utf-8') as file:
    return file.read()

#Función para dividir los logs en bloques
def separar_logs_bloques(texto):
  bloques_separados = texto.split('\n\n')
  bloques = []
  for bloque in bloques_separados:
    bloque_limpio = bloque.strip()
    if bloque_limpio !="":
      bloques.append(bloque_limpio)
  return bloques

def clasificar_por_etiquetas(texto):
  """
  Clasifica el bloque usando palabras clave
  Devuelve una lista de etiquetas pertenecientes a TAXONOMIA.
  """
  etiquetas = set()
  t = texto.lower()

  # SQL
  if "[sql]" in t or "select " in t or "update " in t or "insert " in t:
      etiquetas.add("sql_query")

  # Recuperación de datos
  if "retrieved" in t or "results" in t or "encontré" in t or "aquí tienes" in t:
      etiquetas.add("data_retrieval")

  # Actualizaciones
  if "update " in t or "actualiza" in t or "estatus" in t:
      etiquetas.add("update_operation")

  # Errores comunes
  if "permission denied" in t:
      etiquetas.add("permission_denied")

  if "timeout" in t:
      etiquetas.add("timeout_error")

  if "slow query" in t or "lentitud" in t or "3.8s" in t:
      etiquetas.add("slow_query")

  # Diagnóstico
  if "diagnostic" in t or "testing db connection" in t or "heartbeat" in t:
      etiquetas.add("diagnostic")

  # Búsqueda semántica
  if "semantic retrieval" in t or "tokenizing input" in t:
      etiquetas.add("semantic_retrieval")

  # Inputs incompletos
  if "malformed" in t or "incomplete sql" in t or "no pude interpretar" in t:
      etiquetas.add("malformed_input")

  # Versión
  if "version" in t or "motor de inferencia" in t:
      etiquetas.add("version_check")

  # Limpieza
  if "cleanup" in t or "cache" in t:
      etiquetas.add("cleanup_operation")

  # Archivo no encontrado
  if "filenotfounderror" in t or "not found" in t:
      etiquetas.add("file_not_found")

  # Usuario
  if "[user input]" in t or "“" in t or '"' in t:
      etiquetas.add("user_instruction")

  # Respuesta LLM
  if "[llm response]" in t:
      etiquetas.add("llm_response")

  # Ordenamos según TAXONOMIA
  return [e for e in TAXONOMIA if e in etiquetas]




#Función principal del script
if __name__ == "__main__":
  # Iniciar proceso de lectura y clasificación de logs
  archivo_logs = 'logs.txt'
  texto = leer_archivo_logs(archivo_logs)
  bloques_de_logs = separar_logs_bloques(texto) 
  
  # Crear cliente de Gemini
  api_key = os.getenv("GEMINI_API_KEY")
  gemini = GeminiClient(api_key)
  print("Gemini disponible:", gemini.available)

  archivo_json = []

  for i, bloque in enumerate(bloques_de_logs, start=1):
    #Verficar si Gemini está disponible
    if gemini.available:
        etiquetas = gemini.classify(bloque)
        #Verificar si Gemini retornó JSON válido
        if not etiquetas:
            print("Gemini no retorno JSON, usando clasificador local")
            etiquetas = clasificar_por_etiquetas(bloque)
    else:
        print("Gemini no esta disponible, usando clasificador local")
        etiquetas = clasificar_por_etiquetas(bloque)
  
  # Construir el objeto para el archivo JSON 
    archivo_json.append({
      "log_id": i,
      "texto": bloque,
      "etiquetas": etiquetas
    })
  # Guardar el resultado en output.json
  with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(archivo_json, f, ensure_ascii=False, indent=2)
  print("Archivo output.json creado correctamente")