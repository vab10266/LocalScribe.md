# agent/state.py
from enum import Enum

class AgentState(Enum):
    REASON_AND_PLAN = "reason_and_plan"
    EXECUTE_PLAN = "execute_plan"
    VERIFY = "verify"
    ERROR_HANDLER = "error"
    SUMMARIZE = "summarize"
    BRAINSTORM = "brainstorm"
    CLARIFY = "clarify"
