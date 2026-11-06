import streamlit as st
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openrouter import ChatOpenRouter
from langchain_chroma import Chroma
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from dotenv import load_dotenv
load_dotenv()



st.title("PageBrain: Turn any URL into an interactive Q&A bot")
url_input = st.text_input("Enter a URL to chat with:", placeholder="https://example.com")

# loader = UnstructuredURLLoader(urls=urls)
# data = loader.load()


@st.cache_resource(show_spinner=False)
def get_vectorstore(url_input):

    # urls=["https://openai.com/"]
    # urls=[url_input]
    loader = WebBaseLoader(web_paths=[url_input])
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.split_documents(data)
    
    vectorstore = Chroma.from_documents(
        documents=docs, 
        embedding=HuggingFaceEmbeddings(),
        collection_name="hf_embedding_test"
    )
    return vectorstore
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=150)
# docs = text_splitter.split_documents(data)
# all_splits = docs
# vectorstore = Chroma.from_documents(documents=docs, embedding=HuggingFaceEmbeddings(),collection_name="hf_embedding_test")

# vectorstore=get_vectorstore()
# retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})

# question="which libray provide recursive text splitter in langchain"
# result=retriever.invoke(question)
# # for i, doc in enumerate(result, 1):
# #     print(f"\nResult {i}:")
# #     print(doc.page_content)
    
    
# llm = ChatOpenRouter(model="nvidia/nemotron-3-ultra-550b-a55b:free")



# query = st.chat_input("Ask me anything: ") 

# prompt = query

# system_prompt = (
#     "You are an assistant for question-answering tasks. "
#     "Use the following pieces of retrieved context to answer "
#     "the question. If you don't know the answer, say that you "
#     "don't know.  keep the "
#     "answer concise."
#     "\n\n"
#     "{context}"
# )


# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", system_prompt),
#         ("human", "{input}"),
#     ]
# )


# if query:
#     question_answer_chain = create_stuff_documents_chain(llm, prompt)
#     rag_chain = create_retrieval_chain(retriever, question_answer_chain)

#     response = rag_chain.invoke({"input": query})
#     print(response["answer"])

#     st.write(response["answer"])
if url_input:
    # Loading indicator for scraping and chunking the URL
    with st.spinner(f"Loading and processing {url_input}..."):
        vectorstore = get_vectorstore(url_input)
        retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})
    
    st.success("URL processed successfully!")

    llm = ChatOpenRouter(model="nvidia/nemotron-3-ultra-550b-a55b:free")
    
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. keep the "
        "answer concise."
        "\n\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    query = st.chat_input("Ask me anything: ") 

    if query:
        # Show the user's query
        st.write(f"**You:** {query}")
        
        # 4. Loading indicator for the LLM response
        with st.spinner("Generating response..."):
            question_answer_chain = create_stuff_documents_chain(llm, prompt)
            rag_chain = create_retrieval_chain(retriever, question_answer_chain)

            response = rag_chain.invoke({"input": query})
            
        st.write(f"**AI:** {response['answer']}")