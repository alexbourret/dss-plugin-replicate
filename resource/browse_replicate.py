import replicate
from replicate_common import (DSSSelectorChoices)

def do(payload, config, plugin_config, inputs):
    print("ALX:do:payload={}, config={}".format(payload, config))
    choices = DSSSelectorChoices()
    return choices.to_dss()
