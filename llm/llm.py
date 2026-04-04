from config import client

class LLM:
    def __init__(self, model: str, sys_prompt: str, tool_dict: list) -> None:
        self.model = model
        self.sys_prompt = sys_prompt
        self.tool_dict - tool_dict
    
    def chat(self, input: str):
        response = client.responses.create(
            model=self.model,
            instructions = self.sys_prompt,
            input=input,
            tools=self.tool_dict,

        )

        
        for part in response.output:
            if part.type == "reasoning" or part.type == "message":
                print(f"{part.type}: {', '.join([c.text for c in part.content])}")
            elif part.type == "function_call":
                print(f"{part.type}: {part.name}({part.arguments})")
                
        reasoning = "<|message|>".join(response.output_text.split("<|message|>")[:-1])
        output = response.output_text.split("<|message|>")[-1]

        return reasoning, output