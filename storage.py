from google.cloud import datastore


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
    print(metadata)
    return {
        "date": metadata["presented_at"],
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

