import replicate

class ReplicateClient(object):
    def __init__(self, api_token=None):
        self.api_token = api_token

    def get_available_models(self):
        collections = [collection for page in replicate.paginate(replicate.collections.list) for collection in page]
        return collections
