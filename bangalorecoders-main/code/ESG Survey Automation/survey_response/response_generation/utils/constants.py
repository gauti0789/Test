# System prompt for generating answers from PDF documents

pdf_system_prompt ="""You are an ESG Analyst AI tasked with generating responses to survey questions based on information provided or from publicly available ESG disclosures.
Your expertise lies in analyzing ESG disclosures and extracting key insights to address survey questions effectively in Wells Fargo. 
You will be provided with context from the report relevant to each question to ensure your responses are accurate and well-informed.
Your responses should be detailed and tailored to each question in the survey, leveraging the provided context to provide insightful answers. You are always truthful.
"""


pdf_question_prompt="""Below is a chunk of text containing the most relevant context and their sources extracted from the client's ESG reports and other business documents.
Use the chunks of text to respond to the question below.
Be as truthful as possible.
Your answer will be important for ESG Analysts at Wells Fargo to fill survey details, therefore it should be extremely detailed and professional.

question: {}
docs: {}"""


NOTLOAD = "NotLoad"
THREADS = 10
MAX_THREADS = 12
TOKEN_LIMIT = 20000
CSV_DATA_TOKEN_LIMIT = 20000
MAX_PAGES_OR_SLIDES = 75
DOCUMENT_LIMIT = 3
CHANGE_IMPACT_DOCUMENT_LIMIT = 1
FILE_UPLOAD_MAX_MEMORY_SIZE = 100 * 1024 * 1024
TEXT_EMBEDDING = "text-embeddings-ada"
GPT_4_32K = "gpt-4-32k"
NO_FILES_SELECTED_ERROR = "No files selected."
DOCUMENT_LIMIT_EXCEEDED_ERROR_MESSAGE = "Document limit exceeded. Maximum allowed: {}"
MEMORY_SIZE_ERROR_MESSAGE = "Memory size exceeded."
INVALID_FILE_TYPE_ERROR = "Invalid file type. Only PDF files are allowed."
SLIDE_LIMIT_EXCEEDED_ERROR_MESSAGE = "Slide limit exceeded for file '{}'. Maximum allowed: {}"
FILES_PROCESSED_SUCCESSFULLY = "Document Uploaded Successfully."
INVALID_API_KEY = "Invalid API key."
UNABLE_TO_CONNECT_TO_VECTOR_DB = "Unable to connect to vector database."
INVALID_INPUT = "Invalid input."
FILE_NOT_FOUND = "File not found."
REQUEST_TIMEOUT_ERROR = "Request timeout error."
API_CONNECTION_ERROR = "API connection error."
RATE_LIMIT_ERROR = "Rate limit exceeded."
UNABLE_TO_CONNECT_TO_VECTOR_DB = "Unable to connect to vector database."