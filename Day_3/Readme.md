# Day 3 — File Handling & JSON in Python

## What I Built
Continued building a **Student Record Management System**, this time upgrading it 
from an in-memory dictionary to persistent storage using JSON files, so student 
records are saved to disk instead of disappearing when the program exits.

## What i Learnt Today

- How to read from and write to files in Python using `open()` with `"r"` and `"w"` modes
- How to use `json.load()` to read JSON data from a file into a Python dictionary
- How to use `json.dump()` to write a Python dictionary back into a file as JSON
- How to check if a file exists using `os.path.exists()` before trying to read it, 
  and create it with default content (`{}`) if it doesn't
- Formatting saved JSON readably using `json.dump(data, f, indent=4)`
- Structuring file operations into reusable `load()` and `save()` helper functions

## How File Handling and JSON Work Together

- `json.load(f)` needs an actual **file object** (`f`) to read from — not just being 
  called on its own
- JSON only supports **string keys**. Even if you store data using an `int` key like 
  `101`, it gets converted to `"101"` the moment it's written to a JSON file
- This means every time data is loaded back with `json.load()`, all keys come back 
  as strings — so lookups, searches, and updates must consistently use strings, 
  not integers, or they will silently fail to match

## Challenges I Faced While Implementing the Project

- **Missing file argument:** Initially called `json.load()` without passing the file 
  object, which crashes since `json.load()` has no way to know what to read
- **Int vs. string key mismatch:** Converted roll numbers to `int` on input (e.g. 
  `int(input("Enter roll_no: "))`), but since JSON always stores keys as strings, 
  lookups like `data[101]` never matched `data["101"]` — searches quietly returned 
  `None` or "No record found" even when the record existed
- **Missing return in `load()`:** The function created the file if it didn't exist 
  but forgot to `return` anything in that branch, so on the very first run it 
  returned `None` instead of an empty dictionary, crashing later code that expected 
  a dict
- **Indentation errors:** A misplaced `else:` block had its body left un-indented, 
  causing a Python `IndentationError` that stopped the whole script from running
- **Leftover variable bug:** Reused a loop variable (`x`) from a `for` loop elsewhere 
  in the script inside `search()` and `delete()` instead of the actual input variable, 
  causing incorrect or crashing lookups


