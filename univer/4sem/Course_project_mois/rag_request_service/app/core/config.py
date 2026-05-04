from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    use_llm: bool = True
    llm_provider: str = "deepseek"

    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com"
    deepseek_model: str = "deepseek-v4-flash"

    llm_timeout: int = 15

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()