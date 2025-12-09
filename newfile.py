import json, urllib

id = 1
url = f"https://api.jikan.moe/v4/anime/{id}/full"
resp = urllib.request.urlopen(url)

data = json.loads(resp.read())

print(data)