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