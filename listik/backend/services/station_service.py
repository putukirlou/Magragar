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