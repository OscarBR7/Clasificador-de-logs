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
    Devuelve UNICAMENTE un JSON válido con este formato:

    {{
    "etiquetas": ["etiqueta1", "etiqueta2"]
    }}

    Sin texto adicional, sin explicaciones, sin comentarios.
    Texto a analizar:

    \"\"\"{texto}\"\"\"
    """

        try:
            respuesta = self.model.generate_content(prompt)
            texto_respuesta = respuesta.text.strip()

            
            data = json.loads(texto_respuesta)
            return data.get("etiquetas", [])

        except Exception as e:
            print("Error en llamada a Gemini:", e)
            return []

