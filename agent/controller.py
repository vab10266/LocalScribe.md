from datetime import datetime

from llm.llm import LLM
from agent.state import AgentState
from llm_configs.planner_config import PLANNER_PROMPT
# from llm.planner_llm import PlannerLLM
from config import MAX_TOOL_CALLS, TIMEOUT_SECONDS
from agent.tools import TOOLS, ToolExecutionError


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
                reasoning, message, tool_call = self._reason_and_plan(
                    # user_input,
                    external_history,
                    internal_history
                )
                internal_history.append({
                    "role": "assistant",
                    "content": reasoning
                })
                if tool_call:
                    state = AgentState.EXECUTE_TOOL
                else:
                    state = AgentState.OUTPUT

            elif state == AgentState.EXECUTE_TOOL:
                internal_history.append({
                    "role": "tool_call",
                    "content": tool_call
                })
                tool_response = self._execute_tool(tool_call)
                internal_history.append({
                    "role": "tool",
                    "content": tool_response
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
                external_history.append({
                    "role": "assistant",
                    "content": message
                })
                return message, external_history, internal_history

            
    def _reason_and_plan(self, external, internal):
        reasoning, message, tool_call = self.model.chat(
            input=[*external, *internal]
        )

        return reasoning, message, tool_call
    
    def _execute_tool(self, tool_call):
            tool_name, tool_args = tool_call
            try:
                # print(exec(f"{part.name}({part.arguments[1:-1]})"))
                tool_response = self.tools[tool_name](**eval(tool_args))
                return tool_response
            
            except Exception as e:
                raise RuntimeError(f"Function call failed: {e}")
     
    def _verify(self, internal_history):
        print(internal_history)
        return True, "N/A"

