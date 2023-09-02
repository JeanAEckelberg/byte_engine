import json

"""
This file contain the method ``write_json_file``. It opens the a file with the given name and writes all the given data 
to the file.
"""
def write_json_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent='\t')
