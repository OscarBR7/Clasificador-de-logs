# Clasificador de Logs con Gemini

## Descripción

Script en Python que utiliza Google Gemini para analizar y clasificar automáticamente logs de sistemas, identificando su temática y asignando etiquetas descriptivas.

## Estructura del Proyecto
```
├── main.py                 # Script principal
├── logs.txt                # Archivo de entrada con logs
├── output.json             # Resultado de la clasificación
├── requirements.txt        # Dependencias del proyecto
├── README.md              # Este archivo
└── utils/
    ├── __init__.py
    └── cliente_gemini.py  # Cliente para interactuar con la API de Gemini
```

## Requisitos Previos

- Python 3.8 o superior
- API Key de Google Gemini (gratuita)
- Conexión a internet

## Instalación

### 1. Clonar o descargar el proyecto

### 2. Crear entorno virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar API Key de Gemini

#### Obtener tu API Key:
1. Ve a [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Inicia sesión con tu cuenta de Google
3. Haz clic en "Create API Key"
4. Copia tu API Key

#### Configurar la variable de entorno:

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="tu-api-key-aqui"
```

**Windows (CMD):**
```cmd
set GEMINI_API_KEY=tu-api-key-aqui
```

**Linux/Mac:**
```bash
export GEMINI_API_KEY="tu-api-key-aqui"
```

## Ejecución
```bash
python main.py
```

### Salida esperada:
```
Gemini disponible: True
Archivo output.json creado correctamente
```

## Formato de Salida

El script genera un archivo `output.json` con la siguiente estructura:
```json
[
  {
    "log_id": 1,
    "texto": "[Texto completo del log]",
    "etiquetas": ["sql_query", "data_retrieval"]
  },
  {
    "log_id": 2,
    "texto": "[Texto completo del log]",
    "etiquetas": ["timeout_error", "slow_query"]
  }
]
```

## Lista de Etiquetas

El sistema clasifica los logs en las siguientes categorías:

| Etiqueta | Descripción |
|----------|-------------|
| `sql_query` | Consultas SQL a bases de datos |
| `data_retrieval` | Recuperación de información |
| `update_operation` | Operaciones de actualización |
| `permission_denied` | Errores de permisos |
| `timeout_error` | Errores por tiempo de espera agotado |
| `slow_query` | Consultas lentas (> 3 segundos) |
| `diagnostic` | Diagnósticos y pruebas del sistema |
| `semantic_retrieval` | Búsquedas semánticas con IA |
| `malformed_input` | Entradas con formato incorrecto |
| `version_check` | Verificación de versiones |
| `cleanup_operation` | Operaciones de limpieza/mantenimiento |
| `file_not_found` | Archivos no encontrados |
| `user_instruction` | Instrucciones del usuario |
| `llm_response` | Respuestas generadas por modelos LLM |

### Consideraciones
- Si Gemini no está disponible o falla, el sistema utiliza un clasificador local basado en reglas (palabras clave)
- Esto garantiza que el script siempre produzca resultados

## Autor

[Oscar Briones]  
