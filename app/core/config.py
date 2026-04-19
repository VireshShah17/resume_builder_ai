import os
from dotenv import load_dotenv # Make sure you ran: pip install python-dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# 1. Dynamically find the exact path to the .env file
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
ENV_FILE_PATH = os.path.join(ROOT_DIR, ".env")

# 2. BRUTE FORCE LOAD IT into the OS environment before Pydantic starts
load_dotenv(ENV_FILE_PATH)

# 3. DEBUG PRINT: This will print to your terminal so we know what is happening
print(f"--- DEBUG: Looking for .env at: {ENV_FILE_PATH} ---")
print(f"--- DEBUG: Does file exist? {os.path.exists(ENV_FILE_PATH)} ---")

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Resume Builder API"
    VERSION: str = "1.0.0"
    
    DATABASE_URL: str 

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH, 
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()