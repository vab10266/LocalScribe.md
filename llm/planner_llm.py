# import sys

# from config import client
# from llm_configs.planner_config import PLANNER_MODEL, PLANNER_PROMPT, PLANNER_TOOLS
# from agent.schema import ReasonAndPlan
# from llm.llm import LLM

# class PlannerLLM(LLM):
#     def __init__(self):
#         super().__init__(PLANNER_MODEL, PLANNER_PROMPT, PLANNER_TOOLS)

# # def planner_llm(user_input, history):
# #     messages = [
# #         *history,
# #         {"role": "system", "content": PLANNER_PROMPT},
# #         {"role": "user", "content": user_input},
# #     ]
    
# #     try:
# #         response = client.responses.parse(
# #             model=PLANNER_MODEL,
# #             input=messages,
# #             text_format=ReasonAndPlan,
# #         )

# #     except Exception as e:
# #         print(e)
# #         sys.exit(1)

# #     return response