from graph.state import GraphState
from graph.chains.answer_chain import answer_chain,GradAnswer
from graph.chains.hallucination_chain import hallucination_chain,GradHallucination
from graph.consts import MAX_RETRIES

def grade_hallucination(state: GraphState):

    documents=state["documents"]
    generation=state["generation"]
    if state.get("retries",0)>=MAX_RETRIES:
        print(f"--- Max retries ({MAX_RETRIES}) reached, accepting generation ---")
        return "useful"
    score:GradHallucination=hallucination_chain.invoke({"documents":documents,"generation":generation})
    print(score.binary_score)
    if score.binary_score:
        print("--- Generation is grounded in documents ---")
        return "useful"
    print("--- Generation contains hallucination ---")
    return "not useful"
