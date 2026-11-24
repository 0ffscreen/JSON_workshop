"""In this file you will be playing with basics of JSON"""
import json

def example0():
    """A standard JSON string you will be dealing with will look something like this:
    '{"key": "value", "key2": "value2"}'
    """
    example_json = '{"name": "John", "age": 30, "city": "New York"}'
    print(example_json)
    print(type(example_json))  # This will print <class 'str'> because it is a string
# example0() # run this function to see the output

def example1():
    """You can convert a JSON string into a Python dictionary using json.loads()"""
    example_json = '{"name": null, "age": 30, "city": "New York"}'
    example_dict = json.loads(example_json)
    print(example_dict)
    print(type(example_dict))  # This will print <class 'dict'> because it is now a dictionary
    print(example_dict["name"])  # This will print "John" because you can access the value using the key

# example1() # run this function to see the output

def example2():
    """You can convert a Python dictionary into a JSON string using json.dumps()"""
    example_dict = {"name": "John", "age": 30, "city": "New York"}
    example_json = json.dumps(example_dict)
    print(example_json)
    print(type(example_json))  # This will print <class 'str'> because it is now a string

# example2() # run this function to see the output

def example3():
    """You can also convert a Python dictionary into a nicely formatted JSON string using json.dumps() with indent parameter"""
    example_dict = {"name": "John", "age": 30, "city": "New York"}
    example_json = json.dumps(example_dict, indent=4)
    print(example_json)  # This will print a nicely formatted JSON string

# example3() # run this function to see the output

""" you can try playing with the above examples and see how they work. You can also try to create your own JSON strings 
and convert them to dictionaries and vice versa, after all the best way to learn anything is by doing it yourself."""