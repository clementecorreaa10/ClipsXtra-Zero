
import json
import os
import urllib.parse
import urllib.request
import urllib.error
from datetime import datetime, timezone

API_KEY = os.environ.get("YOUTUBE_API_KEY")

QUERIES = [
    "GTA 6",
    "GTA 6 gameplay",
    "GTA 6 reacciones",
    "Rubius GTA 6",
    "DJMariiO GTA 6",
    "TheGrefg GTA 6",
]

def buscar_videos(query):
    if not API_KEY:
        raise RuntimeError("Falta configurar YOUTUBE_API_KEY")

    params = urllib.parse.urlencode({
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 10,
        "order": "date",
        "key": API_KEY
    })

    url = "https://www.googleapis.com/youtube/v3/search?" + params
    request = urllib.request.Request(url)

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))

        videos = []

        for item in data.get("items", []):
            snippet = item["snippet"]
            video_id = item["id"]["videoId"]

            videos.append({
                "titulo": snippet["title"],
                "creador": snippet["channelTitle"],
                "fecha": snippet["publishedAt"],
                "video_id": video_id,
                "enlace": f"https://www.youtube.com/watch?v={video_id}",
                "busqueda": query
            })

        return videos

    except urllib.error.HTTPError as error:
        detalle = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"YouTube API error {error.code}: {detalle}")

resultados = []
vistos = set()

for query in QUERIES:
    print(f"Buscando: {query}")
    for video in buscar_videos(query):
        if video["video_id"] not in vistos:
            vistos.add(video["video_id"])
            resultados.append(video)

os.makedirs("resultados", exist_ok=True)

salida = {
    "fecha_revision": datetime.now(timezone.utc).isoformat(),
    "total_videos": len(resultados),
    "videos": resultados
}

with open("resultados/radar.json", "w", encoding="utf-8") as archivo:
    json.dump(salida, archivo, ensure_ascii=False, indent=2)

print(f"Radar terminado. Videos encontrados: {len(resultados)}")

