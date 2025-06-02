# config.py

DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "your_database"

SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

