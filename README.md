# 🎙️ Sales & E-Commerce Transcription Engine

Microservicio independiente, desacoplado y de alto rendimiento desarrollado en **Python 3.11+**, **FastAPI** y **faster-whisper** (CTranslate2). Especialmente calibrado para procesar **llamadas de ventas online, atención al cliente, soporte, auditoría de calidad y telemercadeo**.

---

## 🚀 Características Principales

1. **Agnóstico y Desacoplado:**  
   Puede integrarse con cualquier backend (Node.js, Python, Java, PHP, Go, etc.) o funcionar de manera autónoma recibiendo peticiones HTTP REST.

2. **Calibrado para Ventas Online y E-Commerce:**  
   Incorpora un sesgo acústico (`WHISPER_INITIAL_PROMPT`) para capturar con alta precisión marcas, métodos de pago (Stripe, PayPal, Mercado Pago, tarjetas), cotizaciones, objeciones y términos de logística/despacho.

3. **Separación de Hablantes (Diarización):**  
   Diferencia entre los turnos del **Asesor de Ventas** y el **Cliente/Comprador** (`SPEAKER_00` / `SPEAKER_01`) mediante análisis acústico y pausas conversacionales.

4. **Soporte Síncrono y Asíncrono (Webhooks):**  
   - `/v1/transcribe/sync`: Ideal para audios cortos (< 5 min), responde en tiempo real.
   - `/v1/transcribe`: Ideal para llamadas largas (15-60 min). Responde `202 Accepted` de inmediato y envía el resultado a un `callback_url` (webhook) al terminar.

5. **Aceleración y Prevención de Bloqueos:**  
   - `BatchedInferencePipeline` (acelera 3x a 5x audios largos).
   - Filtro VAD (descarta silencios).
   - Semáforos de concurrencia (`MAX_CONCURRENT_TRANSCRIPTIONS`) para proteger CPU/RAM.

---

## 🛠️ Cómo Ejecutar el Proyecto

### Opción 1: Entorno Virtual de Python (Local)

1. Clonar el repositorio y entrar en la carpeta:
   ```bash
   git clone https://github.com/KikeGitHub/transcript_phyton.git
   cd transcript_phyton
   ```

2. Crear y activar el entorno virtual:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Iniciar el servidor:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. Abrir la documentación interactiva en el navegador:
   👉 **Swagger UI:** `http://localhost:8000/docs`

---

### Opción 2: Con Docker

```bash
# Construir la imagen
docker build -t sales-transcription-engine:latest .

# Ejecutar el contenedor
docker run -d \
  --name sales-transcription \
  -p 8000:8000 \
  -v %cd%/models_cache:/app/models_cache \
  -v %cd%/tmp/transcriptions:/tmp/transcriptions \
  sales-transcription-engine:latest
```

---

## ⚙️ Configuración (.env)

| Variable | Valor Recomendado | Descripción |
| :--- | :--- | :--- |
| `APP_NAME` | `"Online Sales Transcription Engine"` | Nombre visible en `/docs` |
| `PORT` | `8000` | Puerto HTTP expuesto |
| `INTERNAL_API_KEY` | `"sales-secret-api-key-change-in-prod"` | Token en cabecera `X-Internal-API-Key` |
| `WHISPER_MODEL_SIZE` | `"base"` (o `"small"`, `"large-v3-turbo"`) | Modelo Whisper en uso |
| `WHISPER_DEVICE` | `"cpu"` (o `"cuda"`) | Hardware de cómputo |
| `WHISPER_INITIAL_PROMPT` | *Vocabulario de ventas* | Palabras clave para sesgar el reconocimiento |
| `DIARIZATION_MIN_SPEAKERS`| `2` | Mínimo de personas (Asesor + Cliente) |
| `DIARIZATION_MAX_SPEAKERS`| `2` | Máximo de personas (aumentar para llamadas grupales) |

---

## 📡 Endpoints de la API

* **`POST /v1/transcribe/sync`**: Envío de audio síncrono.
* **`POST /v1/transcribe`**: Envío asíncrono en background con callback webhook.
* **`GET /v1/health`**: Estado del modelo, CPU y slots disponibles.
* **`GET /v1/models`**: Lista de modelos compatibles en memoria.
* **`POST /v1/models/switch`**: Cambio en caliente de modelo en RAM sin reiniciar.
