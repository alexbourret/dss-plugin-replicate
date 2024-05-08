from replicate_common import (DSSSelectorChoices, get_api_token)
from replicate_client import (ReplicateSession)

def do(payload, config, plugin_config, inputs):
    api_token = get_api_token(config)
    choices = DSSSelectorChoices()
    parameter_name = payload.get("parameterName")
    if parameter_name == "model_version":
        if not api_token:
            return choices.text_message("Pick a preset")
        model_name = config.get("model_name")
        if model_name:
            client = ReplicateSession(api_token=api_token)
            versions = client.get_model_versions(model_name)
            for version in versions:
                version_id = version.get("id")
                cog_version = version.get("cog_version")
                created_at = version.get("created_at")
                choices.append(
                    "{} ({})".format(cog_version, created_at),
                    version_id
                )
        else:
            return choices.text_message("Set a model name")
    return choices.to_dss()
