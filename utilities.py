import json
import time
import urllib.request
import urllib.error

def get_anime(id, max_retries=5):
    url = f"https://api.jikan.moe/v4/anime/{id}/full"
    backoff = 1  # seconds

    for attempt in range(max_retries):
        try:
            resp = urllib.request.urlopen(url)
            return json.loads(resp.read())["data"]

        except urllib.error.HTTPError as err:
            if err.code == 429:
                retry_after = err.headers.get("Retry-After")
                wait = float(retry_after) if retry_after else backoff
                time.sleep(wait)
                backoff *= 2  # exponential backoff
                continue
            else:
                # not a rate-limit error, don't retry blindly
                raise

    raise RuntimeError(f"Failed to fetch anime {id} after {max_retries} retries")