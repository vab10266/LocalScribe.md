from config import client
from datetime import datetime
import json
from llm.llm import LLM
from agent.controller import AgentController
from agent.schema import ReasonAndPlan, Brainstorm, Clarification
from md_editor.propose_edit import propose_markdown_edit
from agent.tools import TOOLS, tool_dict, list_note_paths

# from pydantic_core._pydantic_core import ValidationError

# if __name__ == "__main__":
#     # print(TOOLS)
#     for prompt in [ 
#         [
#             {
#                 "role": "user",
#                 "content": "My name is Vaud"
#             },
#             {
#                 "role": "assistant",
#                 "content": "Okay, I'll call you Vaud."
#             },
#             {
#                 "role": "user",
#                 "content": "What is my name?"
#             }
#         ]
#         # "What files do we have?", 
#         # "What is the current time?"
#     ]:
#         print("_-"* 20)
#         start_time = datetime.now()
#         # try:
#         response = client.responses.parse(
#             model="qwen/qwen3-1.7b",
#             instructions = "Use tools when possible to ensure accuracy. If you are asked a question you don't know the anser to, check to see if you have notes on the subject.",
#             input=prompt,
#             tools=TOOLS,
#             # tools=[
#             #     {
#             #         'type': 'function', 'name': 'make_plan', 
#             #         'description': 'create plan for execution', 
#             #         'parameters': {
#             #             'type': 'object', 
#             #             'properties': {
#             #                 'steps': {
#             #                     'type': 'array', 
#             #                     'description': ''
#             #                 }, 'next_state': {
#             #                     'type': 'string', 
#             #                     'description': ''
#             #                 }
#             #             }, 'required': ['steps', 'next_state']
#             #         }
#             #     }
#             # ],
#             # text_format=ReasonAndPlan,

#         )
#         print(datetime.now() - start_time)
#         print(response.output)
        
#         for part in response.output:
#             if part.type == "reasoning" or part.type == "message":
#                 print(f"{part.type}: {', '.join([c.text for c in part.content])}")
#             elif part.type == "function_call":
#                 print(f"{part.type}: {part.name}({part.arguments[1:-1]})")
#                 print(f"'{part.arguments}'")
#                 # print(dict(part.arguments))
#                 try:
#                     # print(exec(f"{part.name}({part.arguments[1:-1]})"))
#                     print(tool_dict[part.name](**eval(part.arguments)))
#                 except Exception as e:
#                     raise RuntimeError(f"Function call failed: {e}")
#                 # print(f"Result: {globals()[part.name](**dict(part.arguments))}")


if __name__ == "__main__":
#     model = LLM(model="qwen/qwen3-1.7b", sys_prompt="Be helpful.", tool_descriptions=[])
#     my_agent = AgentController(model=model, tools=[])
#     print("Hello World")
#     user_input = input()
#     while user_input:
#         message, external_history, internal_history = my_agent.run(user_input=user_input)
#         print(message)
#         user_input = input()
    print(list_note_paths())


# import lmstudio as lms
# SERVER_API_HOST = "http://127.0.0.1:1234"


# ip_address = '10.0.0.212'
# port = 1234
# lms.get_default_client(SERVER_API_HOST)
# model = lms.llm()
# model.complete("Once upon a time,")

# # Configure the default client with an API token
# lms.configure_default_client(SERVER_API_HOST, )

# model = lms.llm()
# result = model.respond("What is the meaning of life?")
# print(result)
