
Сейчас напишу полный код проекта, включая backend (Flask + PostgreSQL) и frontend (HTML + JS). Начнем с получения карты, хранения данных и визуализации.

1. Установка зависимостей
Перед запуском установите зависимости:

bash
Копировать
Редактировать
pip install flask flask_sqlalchemy requests numpy matplotlib opencv-python gunicorn
Backend (Flask + PostgreSQL)
Структура проекта

csharp
Копировать
Редактировать
mars_project/
│── backend/
│   │── app.py  # Основной сервер Flask
│   │── config.py  # Настройки API и БД
│   │── db.py  # Управление БД
│   │── models.py  # SQLAlchemy модели
│   │── services/
│   │   │── map_service.py  # Запрос тайлов, сборка карты
│   │   │── station_service.py  # Оптимизация базовых станций
│   │── routes/
│   │   │── map_routes.py  # Эндпоинты для карты
│   │   │── station_routes.py  # Эндпоинты для станций
│── frontend/
│   │── templates/
│   │   │── index.html
│   │── static/
│   │   │── styles.css
│   │   │── scripts.js
1. config.py (Настройки)
python
Копировать
Редактировать
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/mars_db")
API_URL = "https://olimp.miet.ru/ppo_it/api"
2. db.py (Подключение к БД)
python
Копировать
Редактировать
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
3. models.py (Модели БД)
python
Копировать
Редактировать
from db import db

class Tile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)
    data = db.Column(db.JSON, nullable=False)

class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String, nullable=False)
4. services/map_service.py (Получение и сборка карты)
python
Копировать
Редактировать
import requests
import numpy as np
from config import API_URL
from models import Tile, db

def fetch_tile():
    response = requests.get(f"{API_URL}/")
    return response.json()["message"]["data"] if response.status_code == 200 else None

def assemble_map():
    tiles = []
    for _ in range(16):
        tile_data = fetch_tile()
        if tile_data:
            tiles.append(np.array(tile_data, dtype=np.uint8))
    
    full_map = np.block([
        [tiles[0], tiles[1], tiles[2], tiles[3]],
        [tiles[4], tiles[5], tiles[6], tiles[7]],
        [tiles[8], tiles[9], tiles[10], tiles[11]],
        [tiles[12], tiles[13], tiles[14], tiles[15]],
    ])
    
    return full_map

def save_map_to_db(full_map):
    for i in range(4):
        for j in range(4):
            tile = Tile(x=i, y=j, data=full_map[i*64:(i+1)*64, j*64:(j+1)*64].tolist())
            db.session.add(tile)
    db.session.commit()
5. services/station_service.py (Оптимизация станций)
python
Копировать
Редактировать
import numpy as np
from models import Station, db

def find_peaks(height_map):
    peaks = []
    for i in range(1, height_map.shape[0] - 1):
        for j in range(1, height_map.shape[1] - 1):
            if height_map[i, j] == np.max(height_map[i-1:i+2, j-1:j+2]):
                peaks.append((i, j))
    return peaks

def place_stations(height_map):
    peaks = find_peaks(height_map)
    for x, y in peaks:
        station_type = "Engel" if x % 2 == 0 else "Cuper"
        station = Station(x=x, y=y, type=station_type)
        db.session.add(station)
    db.session.commit()
6. routes/map_routes.py
python
Копировать
Редактировать
from flask import Blueprint, jsonify
from services.map_service import assemble_map, save_map_to_db

map_bp = Blueprint("map", __name__)

@map_bp.route("/generate_map", methods=["GET"])
def generate_map():
    full_map = assemble_map()
    save_map_to_db(full_map)
    return jsonify({"message": "Карта успешно создана"})
7. routes/station_routes.py
python
Копировать
Редактировать
from flask import Blueprint, jsonify
from services.station_service import place_stations

station_bp = Blueprint("stations", __name__)

@station_bp.route("/generate_stations", methods=["GET"])
def generate_stations():
    place_stations()
    return jsonify({"message": "Станции успешно установлены"})
8. app.py (Запуск Flask)
python
Копировать
Редактировать
from flask import Flask
from db import db
from config import DATABASE_URL
from routes.map_routes import map_bp
from routes.station_routes import station_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
db.init_app(app)

app.register_blueprint(map_bp, url_prefix="/map")
app.register_blueprint(station_bp, url_prefix="/stations")

if __name__ == "__main__":
    app.run(debug=True)
Frontend (HTML + JS)
1. index.html
html
Копировать
Редактировать
<!DOCTYPE html>
<html>
<head>
    <title>Марсианская связь</title>
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <h1>Карта Марса</h1>
    <button onclick="generateMap()">Сгенерировать карту</button>
    <button onclick="generateStations()">Разместить станции</button>
    <div id="map"></div>
    <script src="{{ url_for('static', filename='scripts.js') }}"></script>
</body>
</html>
2. styles.css
css
Копировать
Редактировать
body {
    font-family: Arial, sans-serif;
}
button {
    margin: 10px;
    padding: 10px;
}
3. scripts.js
js
Копировать
Редактировать
function generateMap() {
    fetch("/map/generate_map")
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => console.error("Ошибка:", error));
}

function generateStations() {
    fetch("/stations/generate_stations")
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => console.error("Ошибка:", error));
}
Запуск проекта
Настроить БД (PostgreSQL):
bash
Копировать
Редактировать
psql -U user -c "CREATE DATABASE mars_db;"
Запустить сервер Flask:
bash
Копировать
Редактировать
python backend/app.py
Перейти в браузере на http://localhost:5000.
Что реализовано
✅ Запрос данных из API
✅ Сборка 16 тайлов в карту
✅ Сохранение карты в БД
✅ Поиск пиковых точек и установка станций
✅ Запуск через Flask
✅ Веб-интерфейс для управления

Запускай и тестируй!
