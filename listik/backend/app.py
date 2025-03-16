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
