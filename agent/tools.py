from datetime import datetime
import os
import inspect
from typing import get_type_hints, List, Dict, Optional
from config import VAULT_PATH

class ToolExecutionError(Exception):
    pass

# agent/tools.py
from typing import Dict, Callable

# TOOLS: Dict[str, Callable] = {}

# def tool(name: str):
#     def wrapper(fn):
#         TOOLS[name] = fn
#         return fn
#     return wrapper
TOOLS: List[Dict] = []

def python_type_to_json(py_type):
    if py_type in (str,):
        return "string"
    if py_type in (int,):
        return "integer"
    if py_type in (float,):
        return "number"
    if py_type in (bool,):
        return "boolean"
    if py_type in (list,):
        return "array"
    if py_type in (dict,):
        return "object"
    return "string"

def tool(description: Optional[str] = None):
    def decorator(fn):
        sig = inspect.signature(fn)
        type_hints = get_type_hints(fn)

        properties = {}
        required = []

        for name, param in sig.parameters.items():
            if name == "self":
                continue

            param_type = type_hints.get(name, str)

            properties[name] = {
                "type": python_type_to_json(param_type),
                "description": "",
            }

            if param.default is inspect.Parameter.empty:
                required.append(name)

        schema = {
            "type": "function",
            "name": fn.__name__,
            "description": description or (fn.__doc__ or "").strip(),
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
            },
        }

        TOOLS.append(schema)

        return fn
    return decorator


@tool(description="Get the current date and time. Format: yyyy/mm/dd h:m:s")
def get_current_date_time():
    return datetime.now().strftime("%Y/%m/%d %H:%M:%S")

@tool(description="List the directories and files in the mardown vault.")
def get_file_structure():
    path = VAULT_PATH
    try:
        return {
            "status": "success",
            "directories": [f for f in os.listdir(path) if not os.path.isfile(os.path.join(path, f))],
            "files": [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        }
    except OSError as e:
        return {
            "status": "fail",
            "message": f"{e}"
        }

@tool(description="create plan for execution")
def make_plan(steps: list, next_state: str):
    pass



if __name__ == "__main__":
    # print(get_file_structure(os.getcwd()))
    # print(get_file_structure("agent"))
    # print(get_file_structure("a"))
    print(TOOLS)