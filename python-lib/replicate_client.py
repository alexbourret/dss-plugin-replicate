import requests
import time
from replicate_auth import ReplicateAuth


class ReplicateSession(object):
    def __init__(self, api_token=None):
        self.session = requests.Session()
        self.session.auth = ReplicateAuth(access_token=api_token)

    def get_available_models(self):
        url = "https://api.replicate.com/v1/models"
        for item in self.get_next_item(url=url):
            yield item

    def get_model_versions(self, model_name):
        url = "https://api.replicate.com/v1/models/{}/versions".format(model_name)
        for item in self.get_next_item(url=url):
            yield item

    def get_next_item(self, url=None):
        for page in self.get_next_page(url=url):
            rows = page.get("results", [])
            for row in rows:
                yield row

    def get_prediction(self, model_name, model_version, prompt):
        if model_version:
            url = "https://api.replicate.com/v1/predictions"
            json = {
                "version": model_version,
                "input": {
                    "prompt": prompt
                }
            }
        else:
            url = "https://api.replicate.com/v1/{}/predictions".format(model_name)
            json = {
                "input": {
                    "prompt": prompt,
                    "prompt_template": "<s>[INST] {{prompt}} [/INST] ",
                }
            }
        response = self.post(url=url, json=json)
        json_response = response.json()
        get_url = json_response.get("urls", {}).get("get")
        while json_response.get("status") == "starting":
            time.sleep(5)
            response = self.get(url=get_url)
            json_response = response.json()
        return json_response

    def get_next_page(self, url=None):
        next_page_url = url
        while next_page_url:
            response = self.get(url=next_page_url)
            json_response = safe_json(response)
            next_page_url = json_response.get("next", None)
            yield json_response

    def get(self, **kwargs):
        response = self.session.get(**kwargs)
        return response

    def post(self, **kwargs):
        response = self.session.post(**kwargs)
        return response


def safe_json(response):
    return response.json()
