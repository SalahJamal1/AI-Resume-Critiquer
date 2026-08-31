from graph.state import GraphState
from graph.ingestion import  ingestion

async def ingestion_node(state:GraphState)->GraphState:
    print("---Start ingestion---")
    file_path=state["file_path"]
    await ingestion(file_path)
    return state