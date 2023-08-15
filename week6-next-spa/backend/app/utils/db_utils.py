import MySQLdb
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path)

def create_connection():
    return MySQLdb.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USERNAME"),
        passwd=os.getenv("PASSWORD"),
        db=os.getenv("DATABASE"),
        autocommit=True,
        ssl_mode="VERIFY_IDENTITY",
        ssl={
            "ca": "/etc/ssl/cert.pem"
        }
    )