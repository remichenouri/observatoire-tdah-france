# src/config.py
from pathlib import Path
from dotenv import load_dotenv
import os

# Chargement du .env
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# Variables principales
DATA_SOURCE_PATH = os.getenv("DATA_SOURCE_PATH", "data/raw")

# Seuils de qualité depuis .env ou valeurs par défaut
MISSING_RATE_MAX = float(os.getenv("MISSING_RATE_MAX", "0.3"))
OUTLIER_ZSCORE = float(os.getenv("OUTLIER_ZSCORE", "2.5"))
CORRELATION_THRESHOLD = float(os.getenv("CORRELATION_THRESHOLD", "0.9"))

# APIs (vides pour l'instant)
API_KEY = os.getenv("API_KEY", "")
CLINIC_CONFIG_URL = os.getenv("CLINIC_CONFIG_URL", "")
