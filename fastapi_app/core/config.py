from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = ""
    SECRET_KEY: str = "siddharth"

    PROJECT_NAME: str = "RIITUDE ASSESSMENT"

    class Config:
        case_sensitive = True


settings = Settings()
