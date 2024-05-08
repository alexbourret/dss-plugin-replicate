import dataiku
import pandas
import json
from dataiku.customrecipe import get_input_names_for_role
from dataiku.customrecipe import get_output_names_for_role
from dataiku.customrecipe import get_recipe_config
from replicate_client import ReplicateSession
from replicate_common import (
    get_prompt_template, get_api_token, get_prompt_from_column, format_prediction_output,
    process_template, download_file
)


input_A_names = get_input_names_for_role('input_A_role')
input_A_datasets = [dataiku.Dataset(name) for name in input_A_names]

input_B_names = get_input_names_for_role('input_B_role')

output_A_names = get_output_names_for_role('main_output')

output_folder = get_output_names_for_role('output_folder')

Source = input_A_datasets[0]
Source_df = Source.get_dataframe()

config = get_recipe_config()

prompt_body_template = config.get("prompt_body_template", "")

model_name = config.get("model_name")
model_version = config.get("model_version")
prompt_template, prompt_column = get_prompt_template(config)
api_token = get_api_token(config)
session = ReplicateSession(api_token=api_token)
predictions = []
output = dataiku.Dataset(output_A_names[0])
first_dataframe = True

if output_folder:
    output_folder_handle = dataiku.Folder(output_folder[0])

with output.get_writer() as writer:
    for index, input_parameters_row in Source_df.iterrows():
        input_row = input_parameters_row.to_json()
        input_row = json.loads(input_row)
        if prompt_column:
            prompt_template = get_prompt_from_column(input_row, prompt_column)
        prompt = process_template(prompt_template, input_row)
        prediction = session.get_prediction(model_name, model_version, prompt)
        prediction_output = format_prediction_output(prediction)
        output_row = input_row.copy()
        output_row.update({"prediction": prediction.get("output")})
        output_row_dataframe = pandas.DataFrame([output_row])
        if first_dataframe:
            output.write_schema_from_dataframe(output_row_dataframe)
            first_dataframe = False
        if not output_row_dataframe.empty:
            writer.write_dataframe(output_row_dataframe)
        if output_folder:
            output_urls = prediction.get("output", [])
            for output_url in output_urls:
                download_file(output_url, output_folder_handle)
