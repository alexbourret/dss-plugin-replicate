import replicate
from replicate_common import (DSSSelectorChoices)

def do(payload, config, plugin_config, inputs):
    choices = DSSSelectorChoices()
    return choices.to_dss()
