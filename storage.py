from google.cloud import storage

def create_storage_client():
    return storage.Client()

def create_view(blob):
    return {"date": blob.updated, "title": blob.id, "url": blob.public_url}

def list_slides(client):
    bucket = client.get_bucket("jake1520-slides")
    blobs = client.list_blobs(bucket)
    
    return [create_view(blob) for blob in blobs]