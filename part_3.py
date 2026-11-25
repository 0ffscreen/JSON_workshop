"""
    so far json was saved in memory which is not persistent, but we can actually save it into a file and read it back.
    .json is a common file extension for JSON files. You can use the json.dump() and json.load()
    functions to write to and read from JSON files respectively.
"""

import json

def example4():
    """You can write a Python dictionary to a JSON file using json.dump()"""
    example_dict = {"name": "John", "age": 30, "city": "New York"}
    with open("example.json", "w") as json_file:
# "w" mode is used to write to a file. If the file does not exist, it will be created. If it does exist, it will be overwritten.
        json.dump(example_dict, json_file)
    print("JSON data has been written to example.json")

# example4() # run this function to see the output

def example5():
    """You can read a JSON file and convert it back into a Python dictionary using json.load()"""
    with open("example.json", "r") as json_file:
# "r" mode is used to read from a file. If the file does not exist, it will raise an error.
        example_dict = json.load(json_file)
    print(example_dict)
    print(example_dict["name"])  # This will print "John" because you can access the value using the key
    print(type(example_dict))  # This will print <class 'dict'> because it is now a dictionary  

# make sure you ran example4() before running example5() otherwise it will throw an error because the file does not exist yet.
# example5() # run this function to see the output
"""
one way you can update the json file is to read it into a dict, update the dict and then write it back to the file
"""

def example6():
    """ 
    try making a function that can update the json file with a new key-value pair.

    you can update an exxisting dict with-> dict["new_key"] = "new_value"
    """

# example6() # run this function to see the output


"""
alternatively you can just convert the dict into JSON string and save that string using normal file handling methods,
similarly you can read the string back and convert it into dict using json.loads()
"""
