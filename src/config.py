from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    model: str = "gemini-1.5-pro"
    temperature: float = 0.2
    google_api_key: str
    out_dir: str = "./outputs"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
#    model: str = "gpt-4o-mini"
#    temperature: float = 0.1
#    out_dir: str = "outputs"
#
#settings = Settings()
