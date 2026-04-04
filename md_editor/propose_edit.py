# editor/apply_edit.py
import difflib
from pathlib import Path
from md_editor.markdown_as_tree import parse_markdown_sections
from agent.tools import tool, TOOLS

@tool(description="Propose an edit to the section of the markdown file. If the user accepts, the edit will be made.")
def propose_markdown_edit(
    file: str,
    section_title: str,
    new_content: str,
):
    path = Path(file)
    text = path.read_text()
    sections = parse_markdown_sections(text)

    section = next(
        s for s in sections if s.title == section_title
    )

    lines = text.splitlines()
    old = lines[section.start:section.end]
    new = new_content.splitlines()

    diff = "\n".join(
        difflib.unified_diff(
            old, new,
            fromfile=file,
            tofile=file,
            lineterm=""
        )
    )
    print(f"Proposed edit (y/n):\n\n{diff}")
    proceed = input() == "y"
    if proceed:
        # Apply edit
        lines[section.start:section.end] = new
        path.write_text("\n".join(lines))

        return {
            "status": "success",
            "diff": diff
        }
    
    return {
        "status": "rejected",
        "message": "User rejected change."
    }

if __name__ =="__main__":
    # propose_markdown_edit(
    #     file = "vault\\temp.md",
    #     section_title = "Main",
    #     new_content = "# Main\nHello",
    # )
    print(TOOLS)