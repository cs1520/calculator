from google.cloud import datastore


class User:
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    def key(self, datastore_client):
        return datastore_client.key("User", self.username)
