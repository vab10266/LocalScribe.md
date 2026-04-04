

PLANNER_MODEL = "openai/gpt-oss-20b"
PLANNER_PROMPT = """Your job is to call the make_plan function to direct a state machine. 
Your options for steps are 
[
    "get_current_date_time", 
    "get_file_structure", 
    "propose_markdown_edit"
], and your options for next_state are 
[
    "reason_and_plan", 
    "summarize", 
    "brainstorm", 
    "clarify"
]
"""
PLANNER_TOOLS = [
    {
        'type': 'function', 
        'name': 'make_plan', 
        'description': 'create plan for execution', 
        'parameters': {
            'type': 'object', 
            'properties': {
                'steps': {
                    'type': 'array', 
                    'description': ''
                }, 
                'next_state': {'type': 'string', 'description': ''}
            }, 
            'required': ['steps', 'next_state']
        }
    }
]
