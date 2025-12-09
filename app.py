###########################
## Random Anime Recommender  ##
###########################

#Required imports
from flask import Flask, request, url_for, render_template, redirect, session
import random, urllib, json


def get_anime(id):
    url =  f"https://api.jikan.moe/v4/anime/{id}/full"
    try :
        resp = urllib.request.urlopen(url)
    
        while id :
            resp = urllib.request.urlopen(url)
            if resp.status == 200:
                jsonData = json.loads(resp.read())["data"]
                return jsonData
                        
    except urllib.error.HTTPError as err:
            id += 1
            url =  f"https://api.jikan.moe/v4/anime/{id}/full"
            return get_anime(id)
            
                  
#Initialize Flask App
app = Flask(__name__)
app.config["SECRET_KEY"] = "hdhd"

#Total number of ids
all_ids = [id for id in range(1,1000)]

#Route 1
#Route for starting page
@app.route("/", methods=["POST","GET"])
def index():
    if request.method == "POST":
        #Picking random ID to give to API
        id = random.choice(all_ids)
        session["id"] = id

        #Redirecting to Show anime
        return redirect(url_for("show_anime"))
        
    return render_template("index.html")

#Route 2
#Route to Show Anime
@app.route("/show-anime")
def show_anime():
    id = session["id"]
    url = f"https://api.jikan.moe/v4/anime/{id}/full"
    jsonData = get_anime(id)
    
    return render_template("show_anime.html",anime=jsonData)

#Running App with debug-mode ON
if __name__ == "__main__":
    app.run(debug=True)
    