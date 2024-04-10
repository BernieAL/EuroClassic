"""
extract request and responses
as well as their sizes, and calculate data exchanged
log all requests and responses and data used
"""

import os
import json

current_script_dir = os.path.dirname(os.path.abspath(__file__)) #backend/
har_log_file_path = os.path.join(current_script_dir,'HAR_request_log.json')


transaction_total = 0

with open(har_log_file_path,'r') as f:
    data = json.load(f)

    for entry in data['log']['entries']:

        """
        -each size value is returned as  a set with only 1 element {entry['request']['headersSize']} -> {1178}

        -then do tuple unpacking to extract the element from the set -> [element] = myset
            Ex. [response_headerSize] = {entry['response']['headersSize']}

                Result: [1178] = {1178}

        """ 
        request_url = {entry['request']['url']}
        [request_headerSize] = {entry['request']['headersSize']}
        [request_bodySize] = {entry['request']['bodySize']}
        
        response_redirectURL = {entry['response']['redirectURL']}
        [response_headerSize] = {entry['response']['headersSize']}
        [response_bodySize] = {entry['response']['bodySize']}

        
        request_size = request_headerSize + request_bodySize
        response_size = response_headerSize + response_bodySize

        total_size_per_request_bytes = request_size + response_size
        total_size_per_request_mb = (total_size_per_request_bytes / 1024) / 1024 
        transaction_total += total_size_per_request_mb

        print(f"Total request size (request+response): {total_size_per_request_mb} - {request_url} \n ------")
            
        # print(f"request url: {request_url}")
        # print(f"request header size {request_headerSize}")
        # print(f"response redirectURL {response_redirectURL}")
        # print(f"response header size  {response_headerSize}")
        # print(f"response body size {response_bodySize}")
        # print('-----------------')
print(f"Transaction Total (mb) - {transaction_total}")



