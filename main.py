from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
import os
import lyricsgenius

# ===============================
# Configuración de Genius
# ===============================
API_KEY = os.environ.get("GENIUS_API_KEY")
if not API_KEY:
    raise ValueError("GENIUS_API_KEY no está definida en las variables de entorno")
genius = lyricsgenius.Genius(access_token=API_KEY)
genius.verbose = False
genius.remove_section_headers = True

# ===============================
# Inicializar FastAPI
# ===============================
app = FastAPI(title="Lyrics API con Frontend")

# ===============================
# Redirigir raíz al frontend
# ===============================
@app.get("/")
def root():
    return RedirectResponse(url="/lyrics-ui")

# ===============================
# Servir frontend HTML
# ===============================
@app.get("/lyrics-ui", response_class=HTMLResponse)
def serve_frontend():
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

# ===============================
# Endpoint de API para obtener letras
# ===============================
@app.get("/lyrics")
def get_lyrics(artist: str, song: str):
    song_obj = genius.search_song(song, artist)
    if song_obj is None:
        raise HTTPException(status_code=404, detail=f"No se encontró la canción '{song}' de '{artist}'")
    return {"artist": artist, "song": song, "lyrics": song_obj.lyrics}
