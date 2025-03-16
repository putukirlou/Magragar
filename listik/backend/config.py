import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/mars_db")
API_URL = "https://olimp.miet.ru/ppo_it/api"