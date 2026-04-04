# # agent/trace.py
# from dataclasses import dataclass, field
# from typing import Any, Literal, List
# from datetime import datetime

# StepType = Literal["plan", "tool", "summary", "error"]

# @dataclass
# class AgentStep:
#     step_id: int
#     type: StepType
#     name: str | None
#     content: str
#     data: Any | None = None
#     timestamp: str = field(
#         default_factory=lambda: datetime.now().isoformat()
#     )


# @dataclass
# class AgentTrace:
#     query: str
#     steps: List[AgentStep] = field(default_factory=list)

#     def log(self, type: StepType, content: str, name=None, data=None):
#         step = AgentStep(
#             step_id=len(self.steps),
#             type=type,
#             name=name,
#             content=content,
#             data=data,
#         )
#         self.steps.append(step)
