# PDFAssistant

PDFAssistant is an interactive tool that allows users to ask questions based on the content of PDF documents. It makes use of various libraries such as Streamlit, PyPDF2, and langchain to facilitate the querying process of the PDFs.

## Dependencies

- `streamlit`: For creating the web application
- `dotenv`: For loading environment variables
- `PyPDF2`: For PDF text extraction
- `requests`: For downloading PDFs from URLs
- `langchain`: A chain of NLP tools for text processing and embedding

## Code Structure

### `download_pdf_in_memory(url, failed_urls)`

- Downloads a PDF from a given URL and stores it in memory.
- Appends failed URLs to the `failed_urls` list.

### `get_pdf_text(pdf_reader)`

- Extracts text content from the PDF pages using a `PdfReader` object.

### `get_pdf_text_from_docs(pdf_docs)`

- Processes uploaded PDF documents and extracts text.

### `get_pdf_text_from_urls(pdf_urls, failed_urls)`

- Processes PDFs from given URLs and extracts text.

### `get_text_chunks(text)`

- Breaks down the PDF text into manageable chunks. Useful for processing.

### `get_vectorstore(text_chunks)`

- Initializes OpenAIEmbeddings and creates a vector store for text chunks.

### `get_conversation_chain(vectorstore)`

- Sets up a conversation chain, utilizing a language model and a vector store.

### `display_message(message, sender="user")`

- Displays messages in the Streamlit app, differentiating between user and bot.

### `handle_userinput(user_question)`

- Handles user queries and displays the conversation in the Streamlit app.

### `main()`

- Main function that initializes the Streamlit app and orchestrates the execution of functionalities.

## Usage

1. **Running the Application:**
    - Open a web browser and go to `http://localhost:8501/`.
    - You should see the PDFAssistant interface ready for interaction.

2. **Adding Core PDFs:**
    - Open the file `core_pdfs.txt` from the project directory.
    - Copy the links listed in the file.
    - Paste these links into the "PDF URLs" box in the PDFAssistant interface.

3. **Adding Additional PDFs:**
    - Users can add more PDFs by pasting additional links into the "PDF URLs" box.
    - Users can also upload PDF files directly through the user interface.
   
4. **Processing PDFs:**
    - After adding the PDFs, click the "Process" button. PDFAssistant will extract and process text from the added PDFs.
   
5. **Querying PDFs:**
    - Enter your questions in the query box to receive responses based on the content of the processed PDFs.


## Error Handling

- The application includes error handling mechanisms to manage failed downloads and PDF processing issues.

## Installation and Setup

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/yourusername/PDFAssistant.git
    cd PDFAssistant
    ```
   
2. **Create a Virtual Environment:**
    ```bash
    python3 -m venv env
    source env/bin/activate  # For Windows, use `env\Scripts\activate`
    ```
   
3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    Ensure the `requirements.txt` file includes the following:
    ```
    streamlit
    python-dotenv
    PyPDF2
    requests
    langchain
    ```
   
4. **Set Up Environment Variables:**
   - Create a `.env` file in the project directory.
   - Add necessary environment variables, such as API keys, if needed.
   
5. **Run the Application:**
    ```bash
    streamlit run your_app_script.py
    ```
    The application should now be running at `http://localhost:8501/`.


