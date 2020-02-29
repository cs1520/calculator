class Quiz:
    def __init__(self, title, id, given_at, questions):
        self.title = title
        self.id = id
        self.given_at = given_at
        self.questions = questions


class QuizStore:
    def __init__(self, datastore_client):
        self.ds = datastore_client

    def load_quiz(self, id):
        quiz_key = self.ds.key("Quiz", int(id))
        quiz = self.ds.get(quiz_key)
        print(quiz)
        if not quiz:
            return None
        query = self.ds.query(kind="QuizQuestion", ancestor=quiz_key)
        # query.order("number")
        results = list(query.fetch())
        results = sorted(results, key=lambda x: x["number"])
        return Quiz(quiz["title"], id, quiz["given_at"], results)
