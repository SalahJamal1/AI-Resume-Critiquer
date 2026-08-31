import asyncio
import hashlib
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from  langchain_text_splitters import RecursiveCharacterTextSplitter

BASE_DIR = Path(__file__).resolve().parent
CHROMA_DIR = BASE_DIR / "chroma_db"
print(CHROMA_DIR)
embedding=OllamaEmbeddings(model="nomic-embed-text")

vector_store=Chroma(persist_directory=str(CHROMA_DIR),embedding_function=embedding,collection_name="resume_analysis")

retriever=vector_store.as_retriever(search_kwargs={"k": 5})

splitter=RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=500,chunk_overlap=150)


def _document_id(document:Document)->str:
    source=document.metadata.get("source","")
    page=document.metadata.get("page","")
    digest=hashlib.sha256(f"{source}:{page}:{document.page_content}".encode("utf-8"))
    return digest.hexdigest()


async def index_async(documents:list[Document],batch_size:int=50):
    batches:list[list[Document]]=[documents[i:i+batch_size] for i in range(0,len(documents),batch_size)]
    async def add_batch(batch:list[Document],num_batch:int):
        try:
            ids=[_document_id(doc) for doc in batch]
            await vector_store.aadd_documents(batch,ids=ids)
            return True
        except Exception as e:
            print(f"Vector store error: batch {num_batch} - {e}")
            return False
    tasks=[add_batch(batch,i) for i,batch in enumerate(batches)]
    results=await asyncio.gather(*tasks,return_exceptions=True)
    successful = sum(1 for result in results if result)
    if successful == len(batches):
        print(
            f"Vector Store: Successfully Proced {successful}/{len(batches)} documents"
        )
    else:
        print(
            f"Vector Store: Failed to Proced {len(batches) - successful}/{len(batches)} documents"
        )



async def ingestion(file_path:str):
    documents=await PyPDFLoader(file_path).aload()
    print("---Start ingestion---")
    print(
        f"Loaded {len(documents)} pages"
    )

    # Split documents
    chunks = splitter.split_documents(documents)

    print(
        f"Processing {len(chunks)} chunks "
        f"out of {len(documents)} pages"
    )

    print("--- Start ingesting ---")

    await index_async(chunks)

    print("--- Ingestion completed ---")


if __name__ == "__main__":
    asyncio.run(ingestion("../Salah_AbuFarha_Developer.pdf"))