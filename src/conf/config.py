from pydantic import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str = "postgresql+psycopg2://worker:worker@localhost:5432/FastAPIz13a"
    secret_key: str = "worker"
    algorithm: str = "HS256"
    mail_username: str = "example@meta.ua"
    mail_password: str = "password"
    mail_from: str = "example@meta.ua"
    mail_port: int = 465
    mail_server: str = "smtp.meta.ua"

    redis_host: str = 'localhost'
    redis_port: int = 6379
    cloudinary_name: str = "dldekq0gl"
    cloudinary_api_key: str = "359586647227746"
    cloudinary_api_secret: str = "OETDUUBtkMqEazgOQIqAN69JPBA"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
