from datetime import datetime
import json
from llm.llm import LLM
from agent.state import AgentState
from llm_configs.planner_config import PLANNER_PROMPT
# from llm.planner_llm import PlannerLLM
from config import MAX_TOOL_CALLS, TIMEOUT_SECONDS
from agent.tools import *


class AgentController:
    def __init__(self, model: LLM, tools):
        self.model = model
        self.tools = tools

    def run(self, user_input, external_history=[]):
        self.start_time = datetime.now()
        self.tools_called = 0
        external_history.append({
            "role": "user",
            "content": user_input
        })
        internal_history = []
        state = AgentState.AGENT
        reasoning, message, tool_call = None, None, None
        observations = []

        while True:
            print(state)
            if state == AgentState.AGENT:
                message = self._reason_and_plan(
                    # user_input,
                    external_history,
                    internal_history
                )
                internal_history.append(message)
                print(message)
                if message.tool_calls:
                    state = AgentState.EXECUTE_TOOL
                else:
                    
                    state = AgentState.OUTPUT

            elif state == AgentState.EXECUTE_TOOL:
                
                for tool_call in message.tool_calls:
                    name = tool_call.function.name
                    args = tool_call.function.arguments
                    tool_call_id = tool_call.id
                    print(f"Model wants to call: {name} with {args}")
                    
                    tool_response = self._execute_tool(name, args)
                    internal_history.append({
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "content": json.dumps(tool_response)
                    })
                state = AgentState.VERIFY

            elif state == AgentState.VERIFY:
                healthy, err_message = self._verify(internal_history)

                if not healthy:
                    external_history.append({
                        "role": "system",
                        "content": err_message
                    })
                    return err_message, external_history, internal_history
                else:
                    state = AgentState.AGENT

            elif state == AgentState.OUTPUT:
                external_history.append(message)
                return message.content, external_history, internal_history

            
    def _reason_and_plan(self, external, internal):
        message = self.model.chat(
            input=[*external, *internal]
        )

        return message
    
    def _execute_tool(self, tool_name, tool_args):
            try:
                print(f"exec({tool_name}({tool_args}))")
                print(eval(tool_args))
                tool_response = self.tools[tool_name](**eval(tool_args))
                return tool_response
            
            except Exception as e:
                return str(RuntimeError(f"Function call failed: {e}"))
     
    def _verify(self, internal_history):
        print(internal_history)
        if len(internal_history) > 10:
            return False, "Too long without user input"
        return True, "N/A"

