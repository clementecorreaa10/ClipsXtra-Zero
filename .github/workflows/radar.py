
import json
import os
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

QUERIES = [
    "GTA 6",
    "GTA 6 gameplay",
    "GTA 6 reacciones",
    "Rubius GTA 6",
    "DJMariiO GTA 6",
    "TheGrefg GTA 6",
]

ATOM = "{http://www.w3.org/2005/Atom}"
YT = "{http://www.youtube.com/xml/schemas/2015}"

def buscar_youtube(query):
    url = (
        "https://www.youtube.com/feeds/videos.xml?search_query="
        + urllib.parse.quote(query)
    )

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 ClipsXtraZero/1.0"}
    )

    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            xml = response.read()

        root = ET.fromstring(xml)
        videos = []

        for entry in root.findall(ATOM + "entry"):
            video_id = entry.findtext(YT + "videoId")
            if not video_id:
                continue

            videos.append({
                "titulo": entry.findtext(ATOM + "title"),
                "creador": entry.findtext(ATOM + "author/" + ATOM + "name"),
                "fecha": entry.findtext(ATOM + "published"),
                "video_id": video_id,
                "enlace": "https://www.youtube.com/watch?v=" + video_id,
                "busqueda": query
            })

        return videos

    except Exception as error:
        print(f"Error buscando {query}: {error}")
        return []

resultados = []
vistos = set()

for query in QUERIES:
    print(f"Buscando: {query}")
    for video in buscar_youtube(query):
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

with open("resultados/radar.json", "w", encoding="utf-8") as archivo:
    json.dump(resultados, archivo, ensure_ascii=False, indent=2)

print(f"Radar ejecutado: {len(resultados)} búsquedas preparadas.")
