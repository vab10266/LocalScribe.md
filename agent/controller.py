from datetime import datetime

from agent.state import AgentState
from llm_configs.planner_config import PLANNER_PROMPT
from llm.planner_llm import PlannerLLM
from config import MAX_TOOL_CALLS, TIMEOUT_SECONDS
from agent.tools import TOOLS, ToolExecutionError


class AgentController:
    def __init__(self, planner_llm, tools):
        self.planner_llm = planner_llm
        self.tools = tools

    def run(self, user_input, external_history):
        self.start_time = datetime.now()
        self.tools_called = 0
        internal_history = []
        state = AgentState.REASON_AND_PLAN
        plan = None
        observations = []

        while True:
            if state == AgentState.REASON_AND_PLAN:
                plan = self._reason_and_plan(
                    user_input,
                    external_history,
                    internal_history
                )
                internal_history.append({
                    "role": "assistant",
                    "content": plan.reasoning
                })
                state = AgentState.EXECUTE_PLAN

            elif state == AgentState.EXECUTE_PLAN:
                observations = self._execute_plan(plan.steps)
                internal_history.extend(observations)
                state = AgentState.VERIFY

            elif state == AgentState.VERIFY:
                if self._verify(plan, observations):
                    state = plan.next_state
                else:
                    state = AgentState.ERROR_HANDLER

            elif state == AgentState.ERROR_HANDLER:
                plan = self._handle_error(
                    plan,
                    observations
                )
                internal_history.append({
                    "role": "assistant",
                    "content": plan.reasoning
                })
                state = AgentState.EXECUTE_PLAN

            elif state == AgentState.SUMMARIZE:
                return self._summarize_for_user(
                    user_input,
                    plan.reasoning,
                    observations
                )
            
            elif state == AgentState.BRAINSTORM:
                return self._brainstorm_ideas(
                    user_input,
                    observations
                )
            
            elif state == AgentState.CLARIFY:
                return self._ask_user(
                    user_input,
                    observations
                )
            
    def _reason_and_plan(self, user_input, external, internal):
        response = planner_llm(
            user_input=user_input,
            history=[*external, *internal]
        )

        return response
    
    def _execute_plan(self, steps):
            
        observations = []

        for idx, step in enumerate(steps):
            tool_name = step.tool_name
            args = step.tool_args

            if tool_name not in TOOLS:
                raise ToolExecutionError(f"Unknown tool: {tool_name}")

            tool_fn = TOOLS[tool_name]

            # Log the action
            observations.append({
                "role": "assistant",
                "content": f"ACTION: {tool_name}({args})"
            })

            try:
                result = tool_fn(**args)
            except Exception as e:
                # Tool failure is *recoverable*, not fatal
                observations.append({
                    "role": "tool",
                    "content": f"ERROR in {tool_name}: {str(e)}"
                })
                raise ToolExecutionError(str(e)) from e

            # Log the observation
            observations.append({
                "role": "tool",
                "content": result
            })

        return observations
     
    def _verify(self, plan, observations):
        return True

    def _handle_error(self, plan, observations):
        response = error_handler_llm(
            plan=plan,
            observations=observations
        )

        return response
    
    def _summarize_for_user(self, user_input, external, internal):
        response = summarizer_llm(
            user_input=user_input,
            history=[*external, *internal]
        )

        return response
    
    def _brainstorm_ideas(self, user_input, external, internal):
        response = brainstormer_llm(
            user_input=user_input,
            history=[*external, *internal]
        )

        return response
    
    def _ask_user(self, user_input, external, internal):
        response = clarifier_llm(
            user_input=user_input,
            history=[*external, *internal]
        )

        return response
