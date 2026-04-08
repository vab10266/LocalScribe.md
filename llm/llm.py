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
        response = client.responses.parse(
            model=self.model,
            instructions = self.sys_prompt,
            input=input,
            tools=self.tool_descriptions,
        )

        reasoning, output, tool_call = None, None, None
        for part in response.output:
            if part.type == "reasoning":
                reasoning = ', '.join([c.text for c in part.content])
            elif part.type == "message":
                output = ', '.join([c.text for c in part.content])
                output = output.strip()
            elif part.type == "function_call":
                tool_call = part.name, part.arguments[1:-1]
                
        return reasoning, output, tool_call