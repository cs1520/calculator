class VideoStore:
    def __init__(self, datastore_client):
        self.ds = datastore_client

    def fetch_videos(self):
        videos = self.ds.query(kind="Video").fetch()
        return list(videos)
