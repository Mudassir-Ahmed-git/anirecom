from flask import request
import json, urllib

def get_anime(id):
    url = f"https://api.jikan.moe/v4/anime/{id}/full"
    try:
        resp = urllib.request.urlopen(url)

        while id:
            resp = urllib.request.urlopen(url)
            if resp.status == 200:
                jsonData = json.loads(resp.read())["data"]
                return jsonData

    except urllib.error.HTTPError as err:
        id += 1
        url = f"https://api.jikan.moe/v4/anime/{id}/full"
        return get_anime(id)
