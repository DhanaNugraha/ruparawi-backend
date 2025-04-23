from dotenv import load_dotenv
import os
from pathlib import Path

def configure_app():
    # Determine which .env file to load
    env_path = Path(".") / ".env"
    
    if os.environ.get("FLASK_CONFIG") != "config.local":
        env_path = Path(".") / ".env.testing"
  
    load_dotenv(env_path, override=True)


