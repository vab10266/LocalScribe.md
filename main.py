from config import client, WELCOME_MESSAGE
from datetime import datetime
import json
from llm.llm import LLM
from agent.controller import AgentController
from agent.schema import ReasonAndPlan, Brainstorm, Clarification
from md_editor.propose_edit import propose_markdown_edit
from agent.tools import TOOLS, tool_dict, list_note_paths, get_markdown_headers

def display_history(history: list, layer=1):
    spacer = '|' + '____'*layer
    for line in history:
        print(f"{spacer}{line}")

if __name__ == "__main__":
    model = LLM(model="qwen/qwen3-1.7b", sys_prompt="Be helpful.", tool_descriptions=TOOLS)
    my_agent = AgentController(model=model, tools=tool_dict)
    external_history = [
        {
            "role": "system",
            "content": f"Available Markdown Notes:\n\n{list_note_paths()}"
        },
        {
            "role": "assistant",
            "content": WELCOME_MESSAGE
        }
    ]
    print(TOOLS)
    print(WELCOME_MESSAGE)
    print("User: ", end="")
    user_input = input()
    while user_input:
        message, external_history, internal_history = my_agent.run(user_input=user_input, external_history=external_history)
        display_history(internal_history)
        print(message)
        print("User: ", end="")
        user_input = input()
