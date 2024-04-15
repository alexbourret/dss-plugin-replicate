import requests
from replicate_auth import ReplicateAuth


class ReplicateSession(object):
    def __init__(self, api_token=None):
        self.session = request.Session()
        self.session.auth = ReplicateAuth(access_token=api_token)

    def get_available_models(self):
        for item in get_next_item():
            yield item

    def get_next_item(self, url=None):
        for page in self.get_next_page(url=url):
            rows = page.get("results", [])
            for row in rows:
                yield row

    def get_next_page(self, url=None):
        response = self.get()

    def get(self, **kwargs):
        response = self.session.get(**kwargs)
        return response
