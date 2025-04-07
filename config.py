import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Ortam değişkeninden veritabanı bağlantı URL'sini al
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
db_host = os.getenv("db_host", "localhost")
db_port = os.getenv("db_port", "5432")
db_name = os.getenv("db_name")

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


