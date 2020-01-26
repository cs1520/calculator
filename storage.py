from google.cloud import storage, datastore

def create_storage_client():
    return storage.Client()

def get_metadata(blob):
    return {"date": blob.updated, "title": blob.id, "url": blob.public_url}

def list_slides(storage_client):
    """ Reads all of the slides from the storage client
    """
    bucket = storage_client.get_bucket("jake1520-slides")
    blobs = storage_client.list_blobs(bucket)
    
    return [get_metadata(blob) for blob in blobs]