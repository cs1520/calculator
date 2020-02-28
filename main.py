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

from storage import (
    create_datastore_client,
    create_storage_client,
    list_slides,
    store_quiz_answer,
)
from quiz import Quiz
import user
import student

app = Flask(__name__)
app.secret_key = b"20072012f35b38f51c782e21b478395891bb6be23a61d70a"

# Initialization code for our storage layer
datastore_client = create_datastore_client()
storage_client = create_storage_client()
userstore = user.UserStore(datastore_client, storage_client)


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
    s = student.read_student_info(datastore_client, id)
    if s is None:
        return abort(404)
    output = {"name": s.name, "email": s.email}
    return jsonify(output)


@app.route("/auth/signup", methods=["GET"])
def show_signup_form():
    return render_template("signup.html", auth=True)


@app.route("/auth/signup", methods=["POST"])
def handle_signup():
    username = request.form.get("username")
    password = request.form.get("password")
    bio = request.form.get("bio")
    if username in userstore.list_existing_users():
        return render_template(
            "signup.html", auth=True, error="A user with that username already exists"
        )
    # TODO: make this transactional so that we don't have a user without a profile
    userstore.store_new_credentials(user.generate_creds(username, password))
    userstore.store_new_profile(user.UserProfile(username, bio))
    session["user"] = username
    return redirect("/")


@app.route("/auth/login", methods=["GET"])
def show_login_form():
    return render_template("login.html", auth=True)


@app.route("/auth/login", methods=["POST"])
def handle_login():
    username = request.form.get("username")
    password = request.form.get("password")
    user = userstore.verify_password(username, password)
    if not user:
        return render_template("login.html", auth=True, error="Password did not match.")
    session["user"] = user.username
    return redirect("/")


@app.route("/auth/logout")
def handle_logout():
    session.clear()
    return redirect("/")


@app.route("/user")
def check_user_exists():
    """This is a weird one, I'm only really calling this function to check for duplicate usernames."""
    username = request.args.get("username")
    # TODO: make this faster than loading all users and iterating each time
    return jsonify({"exists": username in userstore.list_existing_users()})


@app.route("/profile")
def show_profile():
    user = get_user()
    if not user:
        redirect("/auth/login")
    return render_template("profile.html")


@app.route("/profile/edit")
def edit_profile():
    user = get_user()
    if not user:
        redirect("/auth/login")
    return render_template("profile_edit.html", user=user)

@app.route("/profile/generate_avatar_url", methods=["PUT"])
def generate_avatar_url():
    """This endpoint expects 1. a filename and 2. a content type
    """
    print(request.is_json)
    print(request.data)
    print(request.is_json)
    if not request.is_json:
        abort(404)
    filename = request.json["filename"]
    content_type = request.json["contentType"]
    if not (filename and content_type):
        # One of the fields was missing in the JSON request
        abort(404)
    avatar_url = userstore.create_avatar_upload_url(filename, content_type)
    return jsonify({"signedUrl": avatar_url})

def get_user():
    """If our session has an identified user (i.e., a user is signed in), then
    return that username."""
    return session.get("user", None)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
