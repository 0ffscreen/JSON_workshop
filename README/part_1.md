# Introduction to JSON with Python

Welcome to the **JSON Workshop!**

In this workshop, you will learn who is JSON, how it works, and how to use it within Python. 
We'll explore two specific concepts in this workshop: 
- storing data in files 
- exchanging data through APIs.


## 1. Workshop Overview

### Part 1 — JSON Fundamentals

Learn the syntax, data types and basic rules of JSON.

### Part 2 — JSON in Python

Practise creating, converting, reading and modifying JSON data.

### Part 3 — JSON for Data Storage

Learn how a Python application can save information in a `.json` file and retrieve it later.

### Part 4 — JSON and APIs

Explore how JSON is used to exchange data between applications.

We'll demonstrate this using a **Tic-Tac-Toe bot**, with a premade Python function that accepts a board state and returns the bot's next move.

This will simulate an API-style interaction, preparing us for the following API workshop.

### Part 5 — Further Exploration

For those interested, the repository includes the source code of the Tic-Tac-Toe bot, demonstrating a small project that uses JSON to store and reload its game data.

##  What You'll Learn

By the end of the workshop, you should understand:

- Who in the world is JSON and why it is useful.
- How JSON data is structured.
- How to use Python's `json` library.
- How to store and retrieve data using JSON files.
- Why JSON is commonly used in APIs.

**Prerequisites:** Basic Python knowledge, including variables, lists, dictionaries and functions.

## 2. Who is JSON?

**JSON (JavaScript Object Notation)** is a lightweight, text-based format used to store and exchange structured data.

Json is language-independent and widely used in Python, Java, JavaScript and many other languages.

JSON is commonly used for:

- **Data storage:** Saving information that a program can retrieve later.
- **APIs:** Transferring structured information between applications.
- **Configuration:** Storing application settings and preferences.

### Example

```json
{
  "name": "Gale",
  "age": 20,
  "student": true,
  "subjects": ["Python", "Java", "SQL"]
}
```

JSON stores data as **keys and values** which is similar to maps in java and dict in py.

In this example, `name` is a key, and `"Gale"` is its value.

## 3. JSON Syntax and Rules

JSON supports six data types:

| Type | Example | Python equivalent |
|---|---|---|
| String | `"Hello"` | `str` |
| Number | `42`, `3.14` | `int`, `float` |
| Boolean | `true`, `false` | `True`, `False` |
| Null | `null` | `None` |
| Array | `[1, 2, 3]` | `list` |
| Object | `{"name": "Gale"}` | `dict` |

### Important rules

1. **Keys must be strings** enclosed in double quotes (`" "`).
2. **Strings must use double quotes**(`" "`), not single quotes (`' '`).
3. **Key-value pairs** are separated using a colon (`:`).
4. **Multiple items** are separated using commas (`,`).
5. **Objects** (dict) use curly braces `{ }`, while **arrays** (list) use square brackets `[ ]`.
6. **Trailing commas are not allowed**.
7. **Comments are not supported** in standard JSON.
8. **Boolean and null values** are lowercase: `true`, `false`, and `null`.

JSON can contain nested objects and arrays, allowing us to represent more complex information.
```json
{
  "name": "Gale",
  "grades": {"exam 1": 20 , "exam 2": 30, "exam 3": null}
}
```

## 4. JSON in Python

json can be created as a string, conventionally enclosed in **single quotes**(`' '`) following all the prior mentioned rules, alternatively.

Python provides a built-in library called `json`, this library can be used to convert data into json format 

```python
import json
```

Four key functions we'll explore:

| Function | Purpose |
|---|---|
| `json.dumps()` | Convert Python data into a JSON string |
| `json.loads()` | Convert a JSON string into Python data |
| `json.dump()` | Write Python data as JSON into a file |
| `json.load()` | Read JSON data from a file into Python |

