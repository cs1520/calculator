from flask import (
    Flask,
    Response,
    abort,
    render_template,
    request,
    jsonify,
    redirect,
    session,
)
from google.cloud import datastore
import json

from auth import blueprint as auth_blueprint
from calculate import calculate as calc

app = Flask(__name__)
app.secret_key = b"20072012f35b38f51c782e21b478395891bb6be23a61d70a"

app.register_blueprint(auth_blueprint, url_prefix="/auth")

datastore_client = datastore.Client()

@app.route("/")
def root():
    """Generate the homepage

    The render_template function reads an HTML file from the "templates"
    directory and fills in any variables.
    """
    user = get_user()
    return render_template("index.html", homepage=True, user=user)


@app.route("/calculate", methods=["POST"])
def calculate():
    """Reads a formula submitted by the user and shows the results
    """
    formula = request.form.get("formula")
    result = calc(formula)
    return render_template("formula_results.html", formula=formula, result=result)


@app.route("/fave", methods=["POST"])
def favorite():
    user = get_user()
    if not user:
        redirect('/')
    fave_key = datastore_client.key("Favorite")
    fave = datastore.Entity(key=fave_key)
    fave["owner"] = user
    fave["formula"] = request.form.get("formula")
    fave["result"] = request.form.get("result")
    fave["note"] = request.form.get("note")
    datastore_client.put(fave)

@app.route("/fave", methods=["GET"])
def show_faves():
    user = get_user()
    q = datastore_client.query(kind="Favorite")
    q.add_filter("owner", "=", user)
    faves = q.fetch()
    return render_template("faves.html", faves=faves)

def get_user():
    """If our session has an identified user (i.e., a user is signed in), then
    return that username."""
    return session.get("user", None)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
