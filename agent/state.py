# agent/state.py
from enum import Enum

class AgentState(Enum):
    AGENT = "agent"
    EXECUTE_TOOL = "execute_plan"
    VERIFY = "verify"
    OUTPUT = "output"
