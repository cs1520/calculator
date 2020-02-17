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
from random import randint
import json
import hashlib

from storage import (
    create_datastore_client,
    list_slides,
    store_quiz_answer,
    read_student_info,
    save_new_user,
    existing_users,
    load_user,
)
from quiz import Quiz

app = Flask(__name__)
app.secret_key = b"20072012f35b38f51c782e21b478395891bb6be23a61d70a"

# Initialization code for our storage layer
datastore_client = create_datastore_client()


@app.route("/")
def root():
    """Generate the homepage

    Gets a random number from the randint function, passing it to the
    template.

    The render_template function reads an HTML file from the "templates"
    directory and fills in any variables.
    """
    fun_number = randint(45, 121)
    user = session.get("user")
    return render_template("index.html", num=fun_number, homepage=True, user=user)


@app.route("/syllabus")
def syllabus():
    """Generate a page that contains the course syllabus

    Just like the root() function, but it's annotated with a different route.
    """
    return render_template("syllabus.html")


@app.route("/lecture")
def handle_lecture():
    """Generate a page with a list of lectures

    In this iteration, the data is read from Datastore. It generates links our to Object Storage.
    """
    lectures = list_slides(datastore_client)
    return render_template("lectures.html", lectures=lectures)


@app.route("/about")
def handle_about():
    """Generate a page with a description of how this website works.

    Includes a link to this website's GitHub page.
    """
    return render_template("about.html")


@app.route("/quiz/<id>", methods=["GET"])
def show_quiz(id):
    """Presents a quiz to a user

    This is a hardcoded quiz, but in the future I will present different quizzes based on id
    """
    quiz = Quiz(
        "Week 4 Quiz",
        id,
        [
            {
                "description": "What markup language describes the structure of web pages?"
            },
            {"description": "What language is used to style web pages?"},
            {
                "description": "What file can be used to serve static resources in App Engine?"
            },
            {
                "description": "What file did the Cow Clicker project store all of the style markup in?"
            },
            {
                "description": "What property can we set on HTML elements to run our own JavaScript when clicked?"
            },
            {"description": "What assignment is due next week?"},
            {"description": "What is the username of your first group member?"},
            {"description": "What is the username of your second group member?"},
            {"description": "What is the username of your third group member?"},
        ],
    )
    return render_template("quiz.html", quiz=quiz)


@app.route("/quiz/<id>", methods=["POST"])
def process_quiz_answer(id):
    student_id = request.form.get("student-id", "No ID provided")
    store_quiz_answer(datastore_client, student_id, quiz_id=id, answers=request.form)
    return render_template(
        "quiz_response.html", quiz_title="Week 4 Quiz", answers=request.form
    )


@app.route("/student/<id>", methods=["GET"])
def show_student_api(id):
    if len(str(id)) != 7:
        return abort(404)
    student = read_student_info(datastore_client, id)
    if student is None:
        return abort(404)
    output = {"name": student.name, "email": student.email}
    return jsonify(output)


@app.route("/auth/signup", methods=["GET"])
def show_signup_form():
    return render_template("signup.html", auth=True)


@app.route("/auth/signup", methods=["POST"])
def handle_signup():
    username = request.form.get("username")
    password = get_password_hash(request.form.get("password"))
    confirm = get_password_hash(request.form.get("confirm-password"))
    if username in existing_users(datastore_client):
        return render_template(
            "signup.html", auth=True, error="A user with that username already exists"
        )
    if password != confirm:
        return render_template(
            "signup.html",
            auth=True,
            error="password does not match password confirmation",
        )
    save_new_user(datastore_client, username, password)
    session["user"] = username
    return redirect("/")


@app.route("/auth/login", methods=["GET"])
def show_login_form():
    return render_template("login.html", auth=True)


@app.route("/auth/login", methods=["POST"])
def handle_login():
    username = request.form.get("username")
    password = get_password_hash(request.form.get("password"))
    user = load_user(datastore_client, username, password)
    if not user:
        return render_template("login.html", auth=True, error="Password did not match.")
    session["user"] = user["username"]
    return redirect("/")


def get_password_hash(pw):
    """This will give us a hashed password that will be extremlely difficult to 
    reverse.  Creating this as a separate function allows us to perform this
    operation consistently every time we use it."""
    encoded = pw.encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def get_user():
    """If our session has an identified user (i.e., a user is signed in), then
    return that username."""
    return session.get("user", None)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
