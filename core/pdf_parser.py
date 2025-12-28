from typing import List, Dict
from langchain_core.documents import Document

SECTION_TITLES = [
    "abstract",
    "contents",
    "introduction",
    "methods",
    "methodology",
    "experiments",
    "results",
    "discussion",
    "conclusion",
    "references"
]


class PDFSectionParser:

    def normalize_heading(self, line: str) -> str:
        line = line.strip().lower()

        # remove leading numbers like "4.", "2.1", "3 "
        while line and (line[0].isdigit() or line[0] in {".", " "}):
            line = line[1:]

        return line.strip()

    def parse(self, documents: List[Document]) -> List[Document]:
        full_text = " ".join(d.page_content for d in documents)

        sections: Dict[str, List[str]] = {}
        current_section = "unknown"

        for line in full_text.splitlines():
            line = line.strip()
            if not line:
                continue
            
            normalized = self.normalize_heading(line)
            if normalized in SECTION_TITLES:
                current_section = normalized
                sections.setdefault(current_section, [])
                continue

            sections.setdefault(current_section, []).append(line)

        section_documents = []

        for section, content in sections.items():
            section_documents.append(
                Document(
                    page_content="\n".join(content),
                    metadata={"section": section}
                )
            )

        for key, val in sections.items():
            sections[key] = ''.join(val)

        return section_documents, sections