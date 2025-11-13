import os
import json

#Try catch para manejar las excepciones si la librería no está instalada
try:
    import google.generativeai as genai
except ImportError:
    genai = None 

#Creación de la clase GeminiClient
class GeminiClient:
    """
    Se crea un cliente para llamar a Google Gemini
    y así poder usar el modelo
    """

    def __init__(self, api_key, model_name="gemini-2.0-flash"):
        self.api_key = api_key
        self.model_name = model_name
        self.available = False

        if api_key and genai:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(model_name)
            self.available = True

    def classify(self, texto):
        """
        Envía el texto al modelo y devuelve una lista de etiquetas,
        si no lo puede enviar, devuelve una lista vacía
        """

        prompt = f"""
    Eres un clasificador de logs.
    Devuelve ÚNICAMENTE un JSON válido con este formato:

    {{
    "etiquetas": ["etiqueta1", "etiqueta2"]
    }}

    Sin texto adicional, sin explicaciones, sin comentarios, sin markdown.
    Texto a analizar:

    \"\"\"{texto}\"\"\"
    """

        try:
            respuesta = self.model.generate_content(prompt)
            texto_respuesta = respuesta.text.strip()
            
            # Print: Para ver la respuesta de Gemini
            print(f"Respuesta raw de Gemini: {texto_respuesta[:200]}")
            
            # Limpiar respuesta generada tipo markdown
            if texto_respuesta.startswith('```'):
                texto_respuesta = texto_respuesta.split('```')[1]
                if texto_respuesta.startswith('json'):
                    texto_respuesta = texto_respuesta[4:].strip()
            
            #Retornar las etiquetas parseadas desde JSON
            data = json.loads(texto_respuesta)
            return data.get("etiquetas", [])

        except json.JSONDecodeError as e:
            print(f"Error parseando JSON: {e}")
            print(f"Texto recibido: {texto_respuesta[:500]}")
            return []
        except Exception as e:
            print(f"Error en llamada a Gemini: {e}")
            return []