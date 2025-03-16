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