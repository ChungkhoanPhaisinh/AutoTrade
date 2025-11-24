from json import dump, load
import os

def WriteFile(filename, content):
    """Write content to file, overwriting if exists"""
    try:
        filename = os.path.join(os.path.dirname(__file__), filename)
        with open(filename, 'w') as f:
            f.write(content)
    except FileNotFoundError:
        return ""

def ReadFile(filename):
    """Read content from json file, returns empty string if file doesn't exist"""
    try:
        filename = os.path.join(os.path.dirname(__file__), filename)
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return ""

def WriteJSONFile(filename, data):
    """Write content to json file, overwriting if exists"""
    try:
        filename = os.path.join(os.path.dirname(__file__), filename)
        with open(filename, "w") as f:
            dump(data, f)
        return True
    except:
        return False

def ReadJSONFile(filename):
    """Read content from json file, returns empty string if file doesn't exist"""
    try:
        filename = os.path.join(os.path.dirname(__file__), filename)
        with open(filename, "r") as f:
            return load(f)
    except FileNotFoundError:
        print("NOT found", filename)
        return {}
