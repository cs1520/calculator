from datetime import datetime, timezone, timedelta
from google.cloud import datastore
from student import Student


def create_datastore_client():
    """ This method lives in the "storage" package, so I don't have to import
    all of the google.cloud packages in my main.py

    In this project it isn't a huge concern, but in larger projects it is good
    to separate dependencies this way. If I want to change how I store data
    in the future, I can refactor these methods without changing the rest of my
    code.
    """
    return datastore.Client()


def create_view(metadata):
    utc_time_presented_at = metadata["presented_at"]
    local_time_presented_at = utc_time_presented_at - timedelta(hours=5)
    return {
        "date": local_time_presented_at,
        "title": metadata["title"],
        "url": metadata["public_url"],
    }


def list_slides(datastore_client):
    """ Reads all of the slides from the storage client
    """
    query = datastore_client.query(kind="Lecture")
    lectures = query.fetch()

    slideshows = [create_view(metadata) for metadata in lectures]
    return sorted(slideshows, key=lambda i: i["date"])


def store_quiz_answer(datastore_client, user, quiz_id, answers):
    quiz_key = datastore_client.key("QuizAnswer", str(user + "_quiz" + quiz_id))

    quiz_answer = datastore.Entity(key=quiz_key)
    for q, a in answers.items():
        quiz_answer[q] = a

    datastore_client.put(quiz_answer)


def read_student_info(datastore_client, student_id):
    student_key = datastore_client.key("Student", str(student_id))
    print("Searching for " + str(student_id))
    info = datastore_client.get(key=student_key)
    if info is None:
        return None
    s = Student(info["last_name"], info["first_name"], info["username"], student_id)
    return s


def save_new_user(datastore_client, username, pw_hash):
    user_key = datastore_client.key("User")
    user = datastore.Entity(key=user_key)
    user["username"] = username
    user["password"] = pw_hash
    datastore_client.put(user)


def existing_users(datastore_client):
    query = datastore_client.query(kind="User")
    users = query.fetch()
    return [u["username"] for u in users]
