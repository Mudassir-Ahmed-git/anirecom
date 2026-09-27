import json
import time
import urllib.request
import urllib.error

def get_anime(id, max_retries=5, timeout=10):
    url = f"https://api.jikan.moe/v4/anime/{id}/full"
    backoff = 1  # seconds

    for attempt in range(max_retries):
        try:
            resp = urllib.request.urlopen(url, timeout=timeout)
            return json.loads(resp.read())["data"]

        except urllib.error.HTTPError as err:
            if err.code == 429:
                retry_after = err.headers.get("Retry-After")
                wait = float(retry_after) if retry_after else backoff
                time.sleep(wait)
                backoff *= 2
                continue
            elif err.code in (500, 502, 503, 504):
                # transient upstream failure, worth retrying
                time.sleep(backoff)
                backoff *= 2
                continue
            else:
                # 404, 400, etc. — retrying won't help
                raise

        except urllib.error.URLError:
            # DNS failure, connection refused, socket timeout, etc.
            time.sleep(backoff)
            backoff *= 2
            continue

    raise RuntimeError(f"Failed to fetch anime {id} after {max_retries} retries")