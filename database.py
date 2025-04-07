import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

# PostgreSQL için ek bağlantı argümanına gerek yok
engine = create_engine(DATABASE_URL)

try:
    with engine.connect():
        print("Database connection established")
except Exception as e:
    print("Database connection failed")
    print(e)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#Northwind veritabanından veri çekilecek.

def fetch_table(table_name):
    df = pd.read_sql_table(table_name, engine)
    return df