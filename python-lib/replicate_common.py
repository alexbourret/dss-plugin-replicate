import requests


MANUAL_SELECT_ENTRY = {"label": "✍️ Enter manually", "value": "dku_manual_select"}
COLUMN_SELECT_ENTRY = {"label": "🏛️ Get from column", "value": "dku_column_select"}


class DSSSelectorChoices(object):

    def __init__(self):
        self.choices = []

    def append(self, label, value):
        self.choices.append(
            {
                "label": label,
                "value": value
            }
        )

    def append_alphabetically(self, new_label, new_value):
        index = 0
        new_choice = {
            "label": new_label,
            "value": new_value
        }
        for choice in self.choices:
            choice_label = choice.get("label")
            if choice_label < new_label:
                index += 1
            else:
                break
        self.choices.insert(index, new_choice)

    def append_manual_select(self):
        self.choices.append(MANUAL_SELECT_ENTRY)

    def start_with_manual_select(self):
        self.choices.insert(0, MANUAL_SELECT_ENTRY)

    def _build_select_choices(self, choices=None):
        if not choices:
            return {"choices": []}
        if isinstance(choices, str):
            return {"choices": [{"label": "{}".format(choices)}]}
        if isinstance(choices, list):
            return {"choices": choices}
        if isinstance(choices, dict):
            returned_choices = []
            for choice_key in choices:
                returned_choices.append({
                    "label": choice_key,
                    "value": choices.get(choice_key)
                })
            return returned_choices

    def text_message(self, text_message):
        return self._build_select_choices(text_message)

    def to_dss(self):
        return self._build_select_choices(self.choices)


def get_api_token(config):
    token = None
    auth_type = config.get("auth_type", "service-api-token")
    if auth_type == "service-api-token":
        token = config.get("service_token", {}).get("api_token")
    return token


def get_prompt_template(config):
    prompt_type = config.get("prompt_type", "body")
    if prompt_type == "body":
        return config.get("prompt_body_template", ""), None
    else:
        return None, config.get("prompt_column", "")


def get_prompt_from_column(input_row, prompt_column):
    return input_row.get(prompt_column)


def format_prediction_output(prediction):
    raw_prediction_output = prediction.get("output")
    if isinstance(raw_prediction_output, list):
        prediction_output = ""
        for output_token in raw_prediction_output:
            prediction_output += output_token
    else:
        prediction_output = raw_prediction_output
    return prediction_output


def process_template(template, dictionnary):
    template = str(template)
    for key in dictionnary:
        replacement = str(dictionnary.get(key, ""))
        template = template.replace("{{{{{}}}}}".format(key), str(replacement))
    return template


def download_file(url_to_file, folder_handle):
    tokens = url_to_file.split("/")
    file_name = "_".join(tokens[-2:])

    response = requests.get(url_to_file, stream=True)
    with folder_handle.get_writer(file_name) as file_handle:
        for chunk in response.iter_content(chunk_size=1024): 
            if chunk:
                file_handle.write(chunk)
