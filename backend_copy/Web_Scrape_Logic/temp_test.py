"""

this file is for checking path to api_log_file.txt from this dir

"""

import os


api_log_file_path = os.path.join(os.path.dirname(__file__),'..','api_log.txt')
print(api_log_file_path)

file = open(api_log_file_path,'a')

file.write('test')