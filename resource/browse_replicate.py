import replicate
from replicate_common import (DSSSelectorChoices, get_api_token)
from replicate_client import (ReplicateClient)

def do(payload, config, plugin_config, inputs):
    print("ALX:do:payload={}, config={}".format(payload, config))
    # LX:do:payload={'parameterType': 'SELECT', 'parameterName': 'model', 'customChoices': True, 'rootModel': {'auth_type': 'service-api-token', 'parameter2': 42, 'service_token': {'mode': 'PRESET', 'name': 'Alex B'}}}, config={'auth_type': 'service-api-token', 'parameter2': 42, 'service_token': {'api_token': 'r8_ehs227RNtM3VNUQ8RqiuPdWHoCeO5Zc4PGGPF'}}
    api_token = get_api_token(config)
    choices = DSSSelectorChoices()
    parameter_name = payload.get("parameterName")
    if parameter_name == "model":
        client = ReplicateClient(api_token=api_token)
        models = client.get_available_models()
        print("ALX:models={}".format(models))
        return choices.text_message(api_token)
    return choices.to_dss()
