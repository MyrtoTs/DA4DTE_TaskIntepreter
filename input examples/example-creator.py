import json
import os

file_number = '6'
users_input_x = {'text' :'Give me an image with vessels, near Genoa port.',
               'image' : ''}
# Serializing json
json_object = json.dumps(users_input_x, indent=4)

# Writing to user_request_x.json
with open(os. getcwd() +"\examples\example"+file_number+".json", "w") as outfile:
    outfile.write(json_object)