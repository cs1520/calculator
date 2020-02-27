import csv
from datetime import datetime as dt
from google.cloud import datastore
from student import Student

from quiz import Quiz


def upload_students():
    students = list()

    with open("student_info.csv", newline="") as csvfile:
        r = csv.reader(csvfile, delimiter=",")
        _headers = next(r)
        for row in r:
            s = Student(row[0], row[1], row[2], row[3])
            students.append(s)

    client = datastore.Client()
    student_entities = list()
    for s in students:
        print(s.id_num + ": " + s.name + " " + s.email)
        student_key = client.key("Student", str(s.id_num))
        student_entity = datastore.Entity(key=student_key)
        student_entity["last_name"] = s.last_name
        student_entity["first_name"] = s.first_name
        student_entity["username"] = s.username
        student_entities.append(student_entity)
    client.put_multi(student_entities)


def upload_quiz_questions():
    entities = []

    quiz = Quiz(
        "Week 4 Quiz",
        dt.today(),
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
    client = datastore.Client()
    quiz_key = client.key("Quiz", 4)
    quiz_entity = datastore.Entity(key=quiz_key)
    quiz_entity["title"] = quiz.title
    entities.append(quiz_entity)
    for i, q in enumerate(quiz.questions, start=1):
        quiz_question_key = client.key("QuizQuestion", parent=quiz_key)
        qq_entity = datastore.Entity(key=quiz_question_key)
        qq_entity["number"] = i
        qq_entity["description"] = q["description"]
        entities.append(qq_entity)

    client.put_multi(entities)


def check():
    client = datastore.Client()
    query = client.query(kind="QuizQuestion", ancestor=client.key("Quiz", 4))
    results = query.fetch()
    for r in results:
        print(r)


def main():
    check()


if __name__ == "__main__":
    main()
