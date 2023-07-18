import warnings
warnings.filterwarnings("ignore")

import json
from task_interpreter import *

def main():
    messages = [{"role": "assistant", "content": "Welcome to DA4DTE! Please enter your request.",
                         'image': ''}]
    while True:
        # read users_input file
        messages.append({"role": "user", "content": users_input['text'],
                         'image': users_input['image']})

        if type(digital_assistant_to_engine(users_input))== str: # meaning that disambiguation is needed
          answer = digital_assistant_to_engine(users_input)

        else:
          engine_input = digital_assistant_to_engine(users_input)
          # the engine_input json file is available
          #[... waiting for the engine to respond ...]
          # TI reads engine_output json file
          answer = response_enhancement(engine_output)
          # the output_to_user file is available

        messages.append({"role": "assistant", "content": answer, "image":''})
