import warnings
warnings.filterwarnings("ignore")

import json
import os
from task_interpreter import *

def demo():
    messages = [{"role": "assistant", "content": "Welcome to DA4DTE! Please enter your request.",
                         'image': ''}]
    while True:
        # read users_input file
        file = input("INSERT FILE NUMBER:  1-8. Type 'exit' to exit.")

        if file=='exit':
          for m in messages:
            print(m)
          break

        with open(os. getcwd() +"\examples\example"+file+".json", "r") as file:
          user_input = json.load(file)

        print('\nUser:')
        print(user_input)

        messages.append({"role": "user", "content": user_input['text'],
                         'image': user_input['image']})

        if type(digital_assistant_to_engine(user_input))== str: # meaning that disambiguation is needed
            answer = digital_assistant_to_engine(user_input)

        else:
            engine_input = digital_assistant_to_engine(user_input)
            # the engine_input json file is available
            #[... waiting for the engine to respond ...]
            print(engine_input)
            engine_output = engine_input['engine'] ## temporarily
            # TI reads engine_output json file
            answer = response_enhancement(engine_output,'')
            # the output_to_user file is available

        print('DA4DTE:')
        print(answer+'\n')

        messages.append({"role": "assistant", "content": answer, "image":''})

demo()