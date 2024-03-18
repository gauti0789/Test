import logging
import openai
import os
import tiktoken

from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader


logger = logging.getLogger(__name__)

load_dotenv()

# Set the OpenAI API key from the environment variable
openai.api_key = os.environ['openai_api_key']
CHUNK_SIZE_GENERAL_DOC=os.environ['CHUNK_SIZE_GENERAL_DOC']
CHUNK_OVERLAP=os.environ['CHUNK_OVERLAP']


def get_token_cl100k(input_text):
    # Make sure OPENAI_ENGINE environment variable is set
    if 'OPENAI_ENGINE' not in os.environ:
        raise ValueError("OPENAI_ENGINE environment variable is not set.")
    
    # Get the base encoding configuration
    cl100k_base = tiktoken.get_encoding("cl100k_base")
    
    # Modify the encoding configuration with additional special tokens
    enc = tiktoken.Encoding(
        name=os.environ['OPENAI_ENGINE'],
        pat_str=cl100k_base._pat_str,
        mergeable_ranks=cl100k_base._mergeable_ranks,
        special_tokens={
            **cl100k_base._special_tokens, 
            "special_token1": 100264, 
            "special_token2": 100265, 
            "special_token3": 100266,
        }
    )
    
    # Encode the input text using the modified encoding configuration
    tokens = enc.encode(input_text, allowed_special={"special_token1", "special_token2", "special_token3"})
    return tokens


def splitTextIntoChunks(text):
    """
     - this function splits the text into chunks of size 1000
     args:
      - text that need to be chunked
    returns:
        chunks obtained from the text
    """

    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=int(CHUNK_SIZE_GENERAL_DOC),
            chunk_overlap=int(CHUNK_OVERLAP),
            length_function=len
        )
    pdf_chunks = text_splitter.split_text(text=text)
    return pdf_chunks



def extract_and_generate_index_from_pdf_doc(thread_no,file,year_of_report):
    """
    Extracts text from general documents (PDFs) and generates an index using language chaining.

    Args:
        general_docs (list): List of paths to general documents (PDFs).

    Returns:
        None
    """
    chunks = []
    logger.info(f"converting document to chunks by thread {thread_no}")
    filename, extension = os.path.splitext(file.name)
    logger.info(f"file name {file.name}")
    name = filename.split("/")[-1]
    if extension.lower() == '.pdf':
        pdf_reader = PdfReader(file)
        for page_number,page in enumerate(pdf_reader.pages):
            text = page.extract_text()
            text = splitTextIntoChunks(text)
            for chunk in text:
                token_length = len(get_token_cl100k(chunk))
                chunks.append([chunk,name,page_number+1,token_length,year_of_report])
    logger.info(f"chunks obtained by thread {thread_no}")
    return chunks

