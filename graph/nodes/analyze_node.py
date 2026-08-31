from langchain_community.document_loaders import PyPDFLoader

from graph.chains.analyze_chain import analyze_chain
from graph.state import GraphState


def analyze_node(state:GraphState)->GraphState:
    print("--- Analyze Node ---")
    documents=state.get("documents",[])
    document="\n\n".join(f"Content:{d.page_content}" for d in documents)
    job_role=state.get("job_role","general job applications")
    response=analyze_chain.invoke({"documents":document,"job_role":job_role})
    retries=state.get("retries",0)+1

    return  {**state,"job_role":job_role,"generation":response.content,"retries":retries}

if __name__=="__main__":
    documents = PyPDFLoader("./../../Salah_AbuFarha_Developer.pdf").load()

    job_role = "AI Engineer"
    res=analyze_node({"documents":documents,"job_role":job_role})
    print(res)
    print("finished")

