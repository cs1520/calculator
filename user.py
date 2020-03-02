from google.cloud import datastore, storage

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
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("utf-8")
    password_hash = hash_password(password, salt)
    return UserCredential(username, password_hash, salt)


def hash_password(password, salt):
    """This will give us a hashed password that will be extremlely difficult to 
    reverse.  Creating this as a separate function allows us to perform this
    operation consistently every time we use it."""
    encoded = password.encode("utf-8")
    return hashlib.pbkdf2_hmac("sha256", encoded, salt, 100000)


class UserProfile:
    def __init__(self, username, bio, avatar_id, avatar_url=None):
        self.username = username
        self.bio = bio
        self.avatar_id = avatar_id  # Id of the blob in Cloud Storage
        self.avatar_url = avatar_url


# https://cloud.google.com/storage/docs/access-control/signing-urls-with-helpers#storage-signed-url-object-python


class UserStore:
    """This class will serve as our Data Access Object
    All of the methods to access the database will be here
    """

    def __init__(self, datastore_client, storage_client):
        self.ds = datastore_client
        self.s = storage_client

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

    def store_new_profile(self, profile, txn=None):
        profile_key = self.ds.key("UserProfile", profile.username)
        p = datastore.Entity(key=profile_key)
        p["username"] = profile.username
        p["bio"] = profile.bio
        if profile.avatar_id:
            p["avatar_id"] = profile.avatar_id
        self.ds.put(p)

    def load_user_profile(self, username, txn=None):
        profile_key = self.ds.key("UserProfile", username)
        profile = self.ds.get(profile_key)
        if "avatar_id" in profile.keys():
            avatar_id = profile["avatar_id"]
            avatar_url = self.create_avatar_display_url(image_name=profile["avatar_id"])
        else:
            avatar_id = None
            avatar_url = None
        return UserProfile(
            profile["username"], profile["bio"], avatar_id, avatar_url=avatar_url,
        )

    def list_existing_users(self, txn=None):
        query = self.ds.query(kind="UserProfile")
        users = query.fetch()
        return [u["username"] for u in users]

    def create_avatar_upload_url(self, image_name, content_type):
        bucket = self.s.bucket("jake1520.appspot.com")
        blob = bucket.blob(image_name)

        url = blob.generate_signed_url(
            version="v4",
            # This URL is valid for 15 minutes
            expiration=datetime.timedelta(minutes=15),
            # Allow PUT requests using this URL
            method="PUT",
            content_type=content_type,
        )
        return url

    def create_avatar_display_url(self, image_name):
        bucket = self.s.bucket("jake1520.appspot.com")
        blob = bucket.blob(image_name)

        url = blob.generate_signed_url(
            version="v4",
            # This URL is valid for 15 minutes
            expiration=datetime.timedelta(minutes=15),
            # Allow GET requests using this URL
            method="GET",
            # Note that when content type information is encoded in the blob
            content_type=blob.content_type,
        )
        return url

