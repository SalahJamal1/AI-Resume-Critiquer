from typing import TypedDict, NotRequired

from langchain_core.documents import Document


class GraphState(TypedDict):
    generation:NotRequired[str]
    job_role:NotRequired[str]
    documents:NotRequired[list[Document]]
    file_path:NotRequired[str]
    retries:NotRequired[int]
