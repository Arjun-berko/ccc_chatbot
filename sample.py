# import streamlit as st
# from dotenv import load_dotenv
# from PyPDF2 import PdfReader
# from langchain.text_splitter import CharacterTextSplitter
#
# def get_pdf_text(pdf_docs):
#     text=""
#     for pdf in pdf_docs:
#         pdf_reader=PdfReader(pdf)
#         for page in pdf_reader.pages:
#             text +=page.extract_text()
#     return text
#
# def get_text_chunks(text):
#     text_splitter=CharacterTextSplitter(
#         separator="\n",
#         chunk_size=1000,
#         chunk_overlap=200
#     )
#     chunks=text_splitter.split_text(text)
#     return chunks
#
#
# def main():
#     load_dotenv()
#     st.set_page_config(page_title="Chat with multiple PDFs", page_icon=": books:")
#
#     st.header("Chat with multiple PDFs :books:")
#     st.text_input("Ask a question about your documents:")
#
#     with st.sidebar:
#         st.subheader("Your documents")
#         pdf_docs=st.file_uploader("Upload your PDFs here and click on 'Process'",accept_multiple_files=True)
#
#         if st.button("Process"):
#             with st.spinner("Processing"):
#                 # get pdf text
#                 raw_text=get_pdf_text(pdf_docs)
#
#                 # get text chunks
#                 text_chunks=get_text_chunks(raw_text)
#                 st.write(text_chunks)
#
#
# if __name__ == "__main__":
#     main()


import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from io import BytesIO
import requests
from langchain.text_splitter import CharacterTextSplitter

def download_pdf_in_memory(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        print(f"Failed to download: {url}")
        return None

def get_pdf_text_from_urls(pdf_urls):
    text = ""
    for url in pdf_urls:
        pdf_in_memory = download_pdf_in_memory(url)
        if pdf_in_memory:
            pdf_reader = PdfReader(pdf_in_memory)
            for page in pdf_reader.pages:
                text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_text(text)
    return chunks

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")

    st.header("Chat with multiple PDFs :books:")
    st.text_input("Ask a question about your documents:")

    with st.sidebar:
        st.subheader("PDF URLs")
        pdf_urls = st.text_area("Enter PDF URLs (separate each URL by a newline):").split("\n")

        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                raw_text = get_pdf_text_from_urls(pdf_urls)

                # get text chunks
                text_chunks = get_text_chunks(raw_text)
                st.write(text_chunks)

if __name__ == "__main__":
    main()


