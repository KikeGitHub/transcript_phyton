import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application Info
    APP_NAME: str = "Online Sales Transcription Engine"
    APP_VERSION: str = "1.0.0"
    ENV: str = "production"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Security
    INTERNAL_API_KEY: str = "sales-secret-api-key-change-in-prod"

    # Faster Whisper Configuration
    WHISPER_MODEL_SIZE: str = "base"
    WHISPER_DEVICE: str = "cpu"
    WHISPER_COMPUTE_TYPE: str = "int8"
    WHISPER_DOWNLOAD_ROOT: Optional[str] = "./models_cache"

    # Performance & Long Audio Optimization
    WHISPER_CPU_THREADS: int = 4
    WHISPER_NUM_WORKERS: int = 1
    WHISPER_BEAM_SIZE: int = 2
    WHISPER_USE_BATCHED: bool = True
    WHISPER_BATCH_SIZE: int = 8
    WHISPER_CONDITION_ON_PREVIOUS_TEXT: bool = False
    WHISPER_VAD_MIN_SILENCE_DURATION_MS: int = 500

    # Contexto acústico para Ventas Online y E-commerce (sesga el vocabulario hacia términos comerciales).
    # Whisper lo usa como "texto previo" para orientar el reconocimiento; no se transcribe.
    # Dejar vacío en .env para desactivar.
    WHISPER_INITIAL_PROMPT: str = (
        "Llamada o conversación de ventas online y atención al cliente en español entre asesor y comprador. "
        "Cotización, catálogo de productos, precio, descuento, promoción, carrito de compras, pasarela de pago, "
        "tarjeta de crédito, débito, transferencia bancaria, Mercado Pago, PayPal, Stripe, envío a domicilio, "
        "paquetería, guía de rastreo, entrega, factura fiscal, garantía, devolución, cierre de venta, objeciones."
    )

    # Concurrency Management
    MAX_CONCURRENT_TRANSCRIPTIONS: int = 2

    # Speaker Diarization Settings
    ENABLE_ACOUSTIC_DIARIZATION: bool = True
    HF_TOKEN: Optional[str] = None
    DIARIZATION_MIN_SPEAKERS: int = 2
    DIARIZATION_MAX_SPEAKERS: int = 2

    # Storage & Temporary Files
    TEMP_DIR: str = "./tmp/transcriptions"

    # Webhook / Callback Settings
    CALLBACK_TIMEOUT_SECONDS: float = 30.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def ensure_directories(self) -> None:
        """Ensure necessary working directories exist."""
        Path(self.TEMP_DIR).mkdir(parents=True, exist_ok=True)
        if self.WHISPER_DOWNLOAD_ROOT:
            Path(self.WHISPER_DOWNLOAD_ROOT).mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_supported_model_profiles(cls, active_model: str) -> list:
        """
        Retorna catálogo de modelos Whisper con sus perfiles de uso técnico y comercial.
        """
        return [
            {
                "name": "base",
                "description": "Modelo ultraligero (74M parámetros). Máxima velocidad en CPU.",
                "size_mb": 140,
                "recommended_for": "Desarrollo local rápido, pruebas y llamadas de audio nítido.",
                "is_active": (active_model == "base"),
            },
            {
                "name": "small",
                "description": "Modelo equilibrado (244M parámetros). Buena precisión general.",
                "size_mb": 460,
                "recommended_for": "Entornos de producción con CPU moderada que requieren buen balance.",
                "is_active": (active_model == "small"),
            },
            {
                "name": "large-v3-turbo",
                "description": "Modelo OpenAI Turbo (809M parámetros). Máxima fidelidad en español, acentos, nombres de productos y marcas de e-commerce.",
                "size_mb": 809,
                "recommended_for": "PRODUCCIÓN: transcripción de alta fidelidad para llamadas de ventas, soporte y webinars.",
                "is_active": (active_model in ("large-v3-turbo", "turbo")),
            },
            {
                "name": "large-v3",
                "description": "Modelo OpenAI Large v3 completo (1550M parámetros).",
                "size_mb": 3100,
                "recommended_for": "Servidores dedicados con aceleración GPU (NVIDIA CUDA).",
                "is_active": (active_model in ("large-v3", "large")),
            },
        ]


settings = Settings()
settings.ensure_directories()