import json
import xml.etree.ElementTree as ET
from spotipy.oauth2 import SpotifyOAuth
import spotipy

CLIENT_ID = ""          # From spotify for developers
CLIENT_SECRET = ""      # From spotify for developers
REDIRECT_URI = ""       # Recommend some simple url e.g. iltalehti.com # this is needed for personalised authorization code for your spotify for developers porject
SCOPE = "playlist-read-private playlist-read-collaborative"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

def get_all_playlists():
    playlists = []
    results = sp.current_user_playlists(limit=50)
    while results:
        playlists.extend(results["items"])
        if results["next"]:
            results = sp.next(results)
        else:
            results = None
    return playlists

def get_all_tracks(playlist_id):
    tracks = []
    results = sp.playlist_tracks(playlist_id, limit=100)
    while results:
        for item in results["items"]:
            track = item.get("track")
            if track:
                tracks.append({
                    "name": track["name"],
                    "album": track["album"]["name"],
                    "artist": ", ".join([a["name"] for a in track["artists"]])
                })
        if results["next"]:
            results = sp.next(results)
        else:
            results = None
    return tracks

def export_to_json(playlists_data, filename="playlists.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(playlists_data, f, ensure_ascii=False, indent=2)
    print(f" Saved {filename}")

def export_to_xml(playlists_data, filename="playlists.xml"):
    root = ET.Element("playlists")

    for pl in playlists_data:
        pl_el = ET.SubElement(root, "playlist", name=pl["name"], id=pl["id"])
        for track in pl["tracks"]:
            tr_el = ET.SubElement(pl_el, "track")
            ET.SubElement(tr_el, "name").text = track["name"]
            ET.SubElement(tr_el, "album").text = track["album"]
            ET.SubElement(tr_el, "artist").text = track["artist"]

    tree = ET.ElementTree(root)
    tree.write(filename, encoding="utf-8", xml_declaration=True)
    print(f"Saved {filename}")

def main():
    playlists = get_all_playlists()
    print(f"Found {len(playlists)} playlists.")

    all_playlists_data = []
    for playlist in playlists:
        print(f"Getting playlist: {playlist['name']}")
        tracks = get_all_tracks(playlist["id"])
        all_playlists_data.append({
            "name": playlist["name"],
            "id": playlist["id"],
            "tracks": tracks
        })

    export_to_json(all_playlists_data, "playlists.json")
    export_to_xml(all_playlists_data, "playlists.xml")

if __name__ == "__main__":
    main()
