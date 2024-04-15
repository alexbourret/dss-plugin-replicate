import requests
from replicate_auth import ReplicateAuth


class ReplicateSession(object):
    def __init__(self, api_token=None):
        self.session = request.Session()
        self.session.auth = ReplicateAuth(access_token=api_token)

    def get_available_models(self):
        collections = [collection for page in replicate.paginate(replicate.collections.list) for collection in page]
        return collections
