from config import client

class LLM:
    def __init__(
            self, 
            model: str, 
            sys_prompt: str, 
            tool_descriptions: list
        ) -> None:
        self.model = model
        self.sys_prompt = sys_prompt
        self.tool_descriptions = tool_descriptions
    
    def chat(self, input: str | list):
        spacer = '|' + '____'*1
        for line in input:
            print(f"{spacer}{line}")
        response = client.chat.completions.create(
            model=self.model,
            messages=input,
            tools=self.tool_descriptions,
        )

        message = response.choices[0].message

        return message