from config import client
from datetime import datetime
import json

from agent.schema import ReasonAndPlan, Brainstorm, Clarification
from md_editor.propose_edit import propose_markdown_edit
from agent.tools import TOOLS
from pydantic_core._pydantic_core import ValidationError

if __name__ == "__main__":
    print(TOOLS)
    for prompt in ["Hi", "What files do we have?", "What is the current time?"]:
        print("_-"* 20)
        start_time = datetime.now()
        # try:
        response = client.responses.parse(
            model="openai/gpt-oss-20b",
            instructions = "Use tools when possible to ensure accuracy.",
            input=prompt,
            tools=[{'type': 'function', 'name': 'make_plan', 'description': 'create plan for execution', 'parameters': {'type': 'object', 'properties': {'steps': {'type': 'array', 'description': ''}, 'next_state': {'type': 'string', 'description': ''}}, 'required': ['steps', 'next_state']}}],
            # text_format=ReasonAndPlan,

        )
        print(datetime.now() - start_time)
        # print(response)
        # print(response.output)
        # print(response.output_text)
        # reasoning = "<|message|>".join(response.output_text.split("<|message|>")[:-1])
        # output = response.output_text.split("<|message|>")[-1]
        # print(reasoning)
        # print(output)
        # print(response.output[-1])
        # except Exception as e:
        #     print(e)
        for part in response.output:
            if part.type == "reasoning" or part.type == "message":
                print(f"{part.type}: {', '.join([c.text for c in part.content])}")
            elif part.type == "function_call":
                print(f"{part.type}: {part.name}({part.arguments})")


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
