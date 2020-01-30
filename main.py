from flask import Flask, render_template, request
from random import randint

from storage import create_datastore_client, list_slides, store_quiz_answer
from quiz import Quiz

app = Flask(__name__)

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
    return render_template("index.html", num=fun_number)


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


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
