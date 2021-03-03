from flask import Blueprint, request, session, redirect, render_template
from google.cloud import datastore

from .user import UserStore, generate_creds, hash_password

blueprint = Blueprint('auth', __name__)

datastore = datastore.Client()
userstore = UserStore(datastore)

@blueprint.route("/signup", methods=["GET"])
def show_signup_form():
    user = get_user()
    if user:
        redirect("/")
    return render_template("signup.html", auth=True)


@blueprint.route("/signup", methods=["POST"])
def handle_signup():
    username = request.args.get("username") or request.form.get("username")
    password = request.args.get("password") or request.form.get("password")
    print("handler: " + username)
    print("handler: " + password)
    if username in userstore.list_existing_users():
        return render_template(
            "signup.html", auth=True, error="A user with that username already exists"
        )
    userstore.store_new_credentials(generate_creds(username, password))
    session["user"] = username
    return redirect("/")


@blueprint.route("/login", methods=["GET"])
def show_login_form():
    user = get_user()
    if user:
        redirect("/")
    return render_template("login.html", auth=True)


@blueprint.route("/login", methods=["POST"])
def handle_login():
    username = request.form.get("username")
    password = request.form.get("password")
    user = userstore.verify_password(username, password)
    if not user:
        return render_template("login.html", auth=True, error="Password did not match.")
    session["user"] = user.username
    return redirect("/")


@blueprint.route("/logout")
def handle_logout():
    session.clear()
    return redirect("/")


def get_user():
    return session.get("user", None)