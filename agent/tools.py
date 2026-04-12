# agent/tools.py

from datetime import datetime
import os
import inspect
from typing import get_type_hints, List, Dict, Optional
from config import VAULT_PATH

class ToolExecutionError(Exception):
    pass

from typing import Dict, Callable

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
            "function": {
                "name": fn.__name__,
                "description": description or (fn.__doc__ or "").strip(),
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                },
            }
        }

        TOOLS.append(schema)

        return fn
    return decorator

def extract_header_section(markdown_content: str, header: str) -> str:
    lines = markdown_content.splitlines()
    output_lines = []
    capture = False
    header_prefix = header.strip()
    header_level = header_prefix.count("#")

    for line in lines:
        if line.strip().startswith("#"):
            if line.strip() == header_prefix:
                capture = True
                continue
            elif capture and line.strip().startswith("#") and line.strip().count("#") <= header_level:
                break

        if capture:
            output_lines.append(line)

    return "\n".join(output_lines)

@tool(description="Get the current date and time. Format: yyyy/mm/dd h:m:s")
def get_current_date_time():
    t_now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    return t_now
    
@tool(description="Load specific markdown note file")
def read_markdown_note_file(local_path: str, header_section: Optional[str] = None):
    print(local_path)
    if ".." in local_path:
        raise EnvironmentError("Navigating out of the local directory is not allowed.")
    
    path = os.path.join(VAULT_PATH, local_path)
    print(local_path)
    if not path.lower().endswith(".md"):
        raise EnvironmentError("Only markdown files may be read.")

    with open(path, 'r', encoding='utf-8') as file:
        output = file.read()
    
    if header_section:
        output = extract_header_section(output, header_section)

    return output

@tool(description="List the directories and files in the mardown vault, with nested structure.")
def list_note_paths(subdir: str = ""):
    path = VAULT_PATH

    if subdir:
        path = os.path.join(path, subdir)

    output = {
        "directories": {},
        "files": [],
    }

    try:
        for next_subdir in [
            f for f in os.listdir(path) if not os.path.isfile(
                os.path.join(path, f)
            ) and not f.startswith(".")
        ]:
            output["directories"][next_subdir] = list_note_paths(os.path.join(subdir, next_subdir))
        
        for file in [
            f for f in os.listdir(path) if os.path.isfile(
                os.path.join(path, f)
            ) and not f.startswith(".") and f.lower().endswith(".md")
        ]:
            output["files"].append(file)

        return output

    except OSError as e:
        return {
            "status": "fail",
            "message": f"{e}"
        }
    
@tool(description="Get the headers from a markdown file.")
def get_markdown_headers(file_path: str):
    path = VAULT_PATH
    headers = []
    with open(os.path.join(path, file_path), 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith("#"):
                headers.append(line.strip())
    return headers


tool_dict = {
    "get_current_date_time": get_current_date_time,
    "list_note_paths": list_note_paths,
    "get_markdown_headers": get_markdown_headers,
    "read_markdown_note_file": read_markdown_note_file
}
