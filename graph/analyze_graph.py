from langgraph.graph import StateGraph,END
from graph.consts import INGESTION,ANALYZE
from graph.nodes.analyze_node import analyze_node
from graph.state import GraphState
from graph.nodes.ingestion_node import ingestion_node
from graph.nodes.grade_answer import grade_hallucination

workflow=StateGraph(GraphState)
workflow.set_entry_point(INGESTION)

workflow.add_node(INGESTION,ingestion_node)

workflow.add_node(ANALYZE,analyze_node)
workflow.add_edge(INGESTION,ANALYZE)

workflow.add_conditional_edges(ANALYZE,grade_hallucination,{
    "useful":END,
    "not useful":ANALYZE,
})

app=workflow.compile()

if __name__=="__main__":
    try:
        app.get_graph().draw_mermaid_png(output_file_path="analyzing.png")
    except Exception as e:
        print(f"Could not render graph diagram: {e}")