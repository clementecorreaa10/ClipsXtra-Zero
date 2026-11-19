
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone

QUERIES = [
    "GTA 6 novedades",
    "GTA 6 gameplay",
    "GTA 6 reacciones",
    "Rubius GTA 6",
    "DJMariiO GTA 6",
    "TheGrefg GTA 6",
]

def buscar_youtube(query):
    url = (
        "https://www.youtube.com/results?search_query="
        + urllib.parse.quote(query)
    )

    return {
        "busqueda": query,
        "enlace": url,
        "fecha_revision": datetime.now(timezone.utc).isoformat()
    }

resultados = [buscar_youtube(q) for q in QUERIES]

os.makedirs("resultados", exist_ok=True)

with open("resultados/radar.json", "w", encoding="utf-8") as archivo:
    json.dump(resultados, archivo, ensure_ascii=False, indent=2)

print(f"Radar ejecutado: {len(resultados)} búsquedas preparadas.")
