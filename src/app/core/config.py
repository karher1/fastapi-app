from pydantic_settings import BaseSettings
import os

#base settings handles loading environment variables from the .env file
class Settings(BaseSettings):
    DATABASE_URL: str 
    OPENAI_API_KEY: str 

    class Config:
        env_file = ".env" #this tells pydantic to look for environment variables in the .env file

settings = Settings()

# Debug prints
print("Environment variables:")
print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")
print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY')}")
print(f"OPEN_API_KEY: {os.getenv('OPEN_API_KEY')}")
print("\nSettings object:")
print(f"settings.DATABASE_URL: {settings.DATABASE_URL}")
print(f"settings.OPENAI_API_KEY: {settings.OPENAI_API_KEY}")
