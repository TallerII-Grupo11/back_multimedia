from app.adapters import __version__
from fastapi.testclient import TestClient
from app.main import app

from main import settings

client = TestClient(app)

SONG_EXAMPLE = {
                "title": "Cancion Animal",
                "artists": [
                    {
                        "artist_id": "id_soda",
                        "artist_name": "Soda Stereo",
                    }
                ],
                "description": "Song",
                "song_file": "file_name",
                "genre": "rock"
                }


def test_read_main():
    response = client.post("/songs", json=SONG_EXAMPLE)
    assert response.status_code == 201
    assert response.json().title == SONG_EXAMPLE.title
    assert response.json().genre == SONG_EXAMPLE.genre