import os
import pathlib
# from dotenv import load_dotenv

# current_path = pathlib.Path(__file__).parent.absolute()
# load_dotenv(dotenv_path=current_path / ".env")

SECRET_KEY = os.environ.get("SECRET_KEY")
DATABASE_URL = os.environ.get("DATABASE_URL")
DATABASE_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASS"),
    "database": os.environ.get("DB_NAME")
}

# class Config:
#     DEBUG = True
