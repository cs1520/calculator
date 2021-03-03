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

from calculator.auth import blueprint as auth_blueprint
from calculator.calculate import calculate as c

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
    return render_template("index.html", homepage=True)


@app.route("/calculate", methods=["POST"])
def calculate():
    """Reads a formula submitted by the user and shows the results
    """
    formula = request.form.get("formula")
    result = c(formula)
    return render_template("formula_results.html", formula=formula, result=result)


def get_user():
    """If our session has an identified user (i.e., a user is signed in), then
    return that username."""
    return session.get("user", None)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
