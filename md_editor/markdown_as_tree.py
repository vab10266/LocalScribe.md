# editor/markdown_ast.py
import re
from dataclasses import dataclass
from typing import List

HEADER_RE = re.compile(r"^(#{1,6})\s+(.*)$")

@dataclass
class MdSection:
    title: str
    level: int
    start: int
    end: int
    content: str


def parse_markdown_sections(text: str) -> List[MdSection]:
    lines = text.splitlines()
    headers = []

    for i, line in enumerate(lines):
        m = HEADER_RE.match(line)
        if m:
            headers.append((i, len(m.group(1)), m.group(2)))

    sections = []
    for idx, (line_no, level, title) in enumerate(headers):
        start = line_no
        end = headers[idx + 1][0] if idx + 1 < len(headers) else len(lines)
        content = "\n".join(lines[start:end])
        sections.append(
            MdSection(title, level, start, end, content)
        )

    return sections
