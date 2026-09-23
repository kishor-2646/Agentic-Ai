#RAG Agent code

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import RetrievalQA

from demo import create_llm

def process_pdf(file_path:str="./resume.pdf"):
    # Step 1 : Document loaders and parsing 
    loader = PyPDFLoader(file_path)# loads the document 
    document = loader.load() #parse the info from the pdf 
    # Step 2 : Text splitter
    splitter = RecursiveCharacterTextSplitter(chunk_size=700,chunk_overlap = 150)
    chunks = splitter.split_documents(document)
    return chunks

# Step 3 : Create the vector embeddings
embeddings = OllamaEmbeddings(model='all-minilm')
# other embedding options : gemini,huggingface,openai

def ingest_data():
    chunks = process_pdf()
    # Step 4: Store the vector embeddings in a vectorstore
    vector_store = FAISS.from_documents(chunks,embeddings)
    print("Data ingested successfully!")
    return vector_store

def rag_chain(query,vector_store):
    # step 5 : Create a retriever to extract top 3 relevant chunks
    llm = create_llm() # initialize the llm 
    retriever = vector_store.as_retriever(search_kwargs={"k":3})
    #step 6 : create a RAG chain 
    chain = RetrievalQA.from_chain_type(
    llm =llm, retriever = retriever)
    #step 7 : Returns the results from the rag system
    return chain.invoke({"query":query})

# function calls to execute the RAG pipeline script
if __name__ == "__main__":
    vector_store = ingest_data()
    query = input("Enter your query :")
    response = rag_chain(query,vector_store)
    print(response)


