from pydantic import BaseModel
from typing import Literal, List

# Plan Schema
class ToolCall(BaseModel):
    tool_name: str
    tool_args: dict

class ReasonAndPlan(BaseModel):
    reasoning: str
    steps: List[ToolCall]
    next_state: Literal[
        "reason_and_plan", 
        "summarize", 
        "brainstorm", 
        "clarify"
    ]

class Summarize(BaseModel):
    summary: str

class Brainstorm(BaseModel):
    initial_reasoning: str
    ideas: List[str]
    closing_thoughts: str

class Clarification(BaseModel):
    summary_of_info_needed: str
    question_to_user: str