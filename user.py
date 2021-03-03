from google.cloud import datastore

import datetime
import hashlib
import os


class UserCredential:
    """Container class for user credentials"""

    def __init__(self, username, password_hash, salt):
        self.username = username
        self.password_hash = password_hash
        self.salt = salt


def generate_creds(username, password):
    print(password)
    """This is a helper method for creating a new credential record
    """
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("utf-8")
    password_hash = hash_password(password, salt)
    return UserCredential(username, password_hash, salt)


def hash_password(password, salt):
    print(password)
    print(salt)
    """This will give us a hashed password that will be extremlely difficult to 
    reverse.  Creating this as a separate function allows us to perform this
    operation consistently every time we use it."""
    encoded = password.encode("utf-8")
    return hashlib.pbkdf2_hmac("sha256", encoded, salt, 100000)


class UserStore:
    """This class will serve as our Data Access Object
    All of the methods to access the database will be here
    """

    def __init__(self, datastore_client):
        self.ds = datastore_client

    def verify_password(self, username, password, txn=None):
        """Load a user based on the password hash. If the hash doesn't match the
        username, then this should return None."""
        user_key = self.ds.key("UserCredential", username)
        user = self.ds.get(user_key)
        if not user:
            # No user found in database
            return None
        hash_attempt = hash_password(password, user["salt"])
        if hash_attempt != user["password_hash"]:
            # Password hash didn't match
            return None
        return UserCredential(user["username"], user["password_hash"], user["salt"])

    def store_new_credentials(self, creds, txn=None):
        user_key = self.ds.key("UserCredential", creds.username)
        user = datastore.Entity(key=user_key)
        user["username"] = creds.username
        user["password_hash"] = creds.password_hash
        user["salt"] = creds.salt
        self.ds.put(user)

    def list_existing_users(self, txn=None):
        query = self.ds.query(kind="UserCredential")
        users = query.fetch()
        return [u["username"] for u in users if "username" in u]
