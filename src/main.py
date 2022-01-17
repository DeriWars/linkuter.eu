from flask import Flask, render_template, request, redirect, session
from waitress import serve
from socket import gethostname, gethostbyname
from random import choices
import string

from objects.sql import Database

app = Flask("linkutter")
app.secret_key = "linkuter-fzfvazfd1sq5f1065eza1f1dsq0f"

DATABASE = Database("./static/data/urls.db")
AVAILABLE_CHARACTERS = string.ascii_uppercase + string.ascii_lowercase + string.digits

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        cut = "".join(choices(AVAILABLE_CHARACTERS, k=5))
        
        while DATABASE.get_url(cut) is not None:
            cut = "".join(choices(AVAILABLE_CHARACTERS, k=5))
        
        DATABASE.add_cut(url, cut)
        return render_template("index.html", success=f"http://linkutter.eu/{cut}")
    
    return render_template("index.html")

@app.route("/<cut>")
def redirect_cut(cut: str) -> str:
    url = DATABASE.get_url(cut)
    
    return "404 - Not found!" if url is None else redirect(url[0])
    
def main():
    app.run(host=gethostbyname(gethostname()), port=8080, debug=True) # Debug server
    # serve(app, host=gethostbyname(gethostname()), port=8080) # Production server

if __name__ == "__main__":
    main()
