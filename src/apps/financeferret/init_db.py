import os, configparser

from sqlalchemy import create_engine, text

from src.apps.financeferret.models import Base

from src.common.env_loader import load_env

load_env()

env = os.environ.get("APP_ENV")

# Create a ConfigParser instance
config = configparser.ConfigParser()

if env == "dev":

    # Read the INI file
    config.read('.env/secrets.ini')
    
    # Access the username and password from the 'postgres' section
    USERNAME = config.get('postgres', 'USERNAME')
    PASSWORD = config.get('postgres', 'PASSWORD')

# Read the INI file
config.read('config/db_config.ini')

# Access the username from the 'credentials' section
DB_ENGINE = config.get(env, 'DB_ENGINE')
DB_HOST = config.get(env, 'DB_HOST')
DB_PORT = config.get(env, 'DB_PORT')

print(f"DB_ENGINE: {DB_ENGINE}")

DATABASE_URL = (
    f"{DB_ENGINE}://{USERNAME}:{PASSWORD}@{DB_HOST}:{DB_PORT}/data_coven"
)


engine = create_engine(DATABASE_URL)


with engine.begin() as connection:
    connection.execute(text("CREATE SCHEMA IF NOT EXISTS financeferret"))
    Base.metadata.create_all(connection)


print("FinanceFerret database objects created.")