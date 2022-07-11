from starlette.config import Config

config = Config(".env")

DATABASE_URL = config("DATABASE_URL", cast=str, default="mongodb://localhost:27017/")
DATABASE_NAME = config("DATABASE_NAME", cast=str, default="mongodb")
APP_ADDR = config("APP_ADDR", cast=str, default="127.0.0.1")
APP_PORT = config("APP_PORT", cast=int, default=50051)
