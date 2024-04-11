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


# LX:do:payload={'parameterType': 'SELECT', 'parameterName': 'model', 'customChoices': True, 'rootModel': {'auth_type': 'service-api-token', 'parameter2': 42, 'service_token': {'mode': 'PRESET', 'name': 'Alex B'}}}, config={'auth_type': 'service-api-token', 'parameter2': 42, 'service_token': {'api_token': 'blaa'}}
def get_api_token(config):
    token = None
    print("ALX:1")
    auth_type = config.get("auth_type", "service-api-token")
    print("ALX:2:{}".format(auth_type))
    if auth_type == "service-api-token":
        print("ALX:3")
        token = config.get("service_token", {}).get("api_token")
        print("ALX:4:{}".format(token))
    return token
