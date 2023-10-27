import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from io import BytesIO
import requests
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain


# Downloading PDFs from specified URLs
def download_pdf_in_memory(url, failed_urls):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BytesIO(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Failed to download: {url} due to {e}")
        failed_urls.append(url)
        return None


# Function to extract text from PDFs
def get_pdf_text(pdf_reader):
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text


# Extracting text from documents dropped from user's computer
def get_pdf_text_from_docs(pdf_docs):
    doc_text = ""
    for pdf in pdf_docs:
        try:
            pdf_reader = PdfReader(pdf)
            doc_text += get_pdf_text(pdf_reader)
        except Exception as e:
            st.error(f"An error occurred while processing the PDF: {e}")
    return doc_text


# Extracting text from documents for which links are provided
def get_pdf_text_from_urls(pdf_urls, failed_urls):
    text = ""
    for url in pdf_urls:
        pdf_in_memory = download_pdf_in_memory(url, failed_urls)
        if pdf_in_memory:
            try:
                pdf_reader = PdfReader(pdf_in_memory)
                text += get_pdf_text(pdf_reader)
            except Exception as e:
                st.error(f"An error occurred while processing the PDF from {url}: \
                {e}")
    return text


# Breaking the final body of text into chunks
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=800,
        chunk_overlap=50
    )
    chunks = text_splitter.split_text(text)
    return chunks


# Initialising OpenAIEmbeddings and creating vector store
def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


# Initialising a conversation chain
def get_conversation_chain(vectorstore):
    llm=ChatOpenAI(temperature=0.9)
    memory=ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    conversation_chain=ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


# defining the display layout for user-chatbot messages
def display_message(message, sender="user"):
    if sender == "user":
        st.text(f"👤 PDFAssistant: ")  # using unicode emoji
        st.write(message)
    else:
        st.text(f"🤖 User: {message}")   # Using Unicode emoji


# Function to handle user queries and produce output
def handle_userinput(user_question):
    if st.session_state.conversation is None:
        st.error("Please process the PDFs first before asking questions.")
    else:
        # the LLM is only triggered when there's a non-null query
        response = st.session_state.conversation({'question': user_question})
        st.session_state.chat_history = response['chat_history']
        for i, message in enumerate(st.session_state.chat_history):
            sender = "bot" if i % 2 == 0 else "user"
            display_message(message.content, sender=sender)


def main():
    load_dotenv()

    st.set_page_config(
        page_title="PDFAssistant",
        page_icon=":books:"
    )

    # setting the conversation key when it hasn't been initialised
    if "conversation" not in st.session_state:
        st.session_state.conversation=None

    # title and subtitle display for streamlit interface
    st.header("Question your PDFs :page_facing_up: :scroll: :computer: :mega:")
    st.subheader("Welcome to PDFAssistant. Query any of your pdfs"
                 " by first adding links or documents to the sidebar, "
                 "clicking process and finally asking your questions")

    # handling user queries
    user_question = st.text_input("Query your documents with PDFAssistant:")
    if user_question: # llm called only for valid non-null queries
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("PDF URLs")

        # PDF link adding section
        pdf_urls_area = "Enter PDF URLs (separate each URL by a newline):"
        pdf_urls = st.text_area(pdf_urls_area).split("\n")
        failed_urls = [] # Creating a list to hold failed URLs

        # PDF document adding section
        upload_msg = "OR/AND Upload your PDFs here and click on 'Process'"
        pdf_docs = st.file_uploader(upload_msg, accept_multiple_files=True)

        if st.button("Process"):
            try:
                # display message when no pdfs or links are added by
                # user
                if (not pdf_docs) and (not any(url.strip() for url in pdf_urls)):
                    st.error("Please add some PDFs or URLs to process.")
                else:
                    with st.spinner("Processing"):
                        raw_text = ""

                        # extracting text from pdf links
                        if pdf_urls and any(url.strip() for url in pdf_urls):
                            raw_text += get_pdf_text_from_urls(pdf_urls, failed_urls)

                            # displaying messages for failed pdf urls
                            if failed_urls:
                                msg = "Failed to download the following URLs:"
                                st.sidebar.warning(msg)
                                for url in failed_urls:
                                    st.sidebar.text(url)

                        # obtaining final string of downloaded pdf text
                        raw_text += get_pdf_text_from_docs(pdf_docs)

                        # dividing text into chunks
                        text_chunks = get_text_chunks(raw_text)

                        # creating vectorstore
                        vectorstore = get_vectorstore(text_chunks)

                        # initialising conversation chain
                        conv_chain = get_conversation_chain(vectorstore)
                        st.session_state.conversation = conv_chain

            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()

