import json
import logging
import openai
import os
from dotenv import load_dotenv
from pymilvus import Collection, utility
from .text_extract import get_token_cl100k

from .constants import *
from .storing_embeddings import create_embedding
from .accuracy import *

logger = logging.getLogger(__name__)

load_dotenv()

openai.api_key = os.environ['openai_api_key']
openai.api_type = os.environ['openai_api_type']
openai.api_base = os.environ['openai_api_base']
openai.api_version = os.environ['openai_api_version']
COLLECTION_NAME = os.environ['COLLECTION_NAME']
TOKEN_LENGTH = os.environ['TOKEN_LENGTH']
MODEL_NAME = os.environ['MODEL_NAME']
MILVUS_HOST = os.environ['MILVUS_HOST']
MILVUS_PORT = os.environ['MILVUS_PORT']
OPENAI_ENGINE = os.environ['OPENAI_ENGINE']
TEMPERATURE = os.environ['TEMPERATURE']
CONNECTION_NAME = os.environ['CONNECTION_NAME']
LIMIT = os.environ['LIMIT']


def get_result_from_pdf_doc(question, docs):
    """
    Generates answers from PDF documents based on a given question.

    Args:
        question (str): The question asked by the user.
        docs (str): The chunks of text from the PDF document.

    Returns:
        str: The generated answer.
    """
    messages = [
            {"role": "system", "content": pdf_system_prompt},
            {"role": "user", "content": pdf_question_prompt.format(question, docs)}
        ]
    input_tokens = len(get_token_cl100k(json.dumps(messages)))
    response = openai.ChatCompletion.create(
        deployment_id=MODEL_NAME,
        messages = messages,
        max_tokens=int(TOKEN_LENGTH),
        temperature=int(TEMPERATURE)
    )
    answer = response.choices[0].message.content
    output_tokens = len(get_token_cl100k(answer))
    return [answer, input_tokens, output_tokens]



def answer(question, is_citation):
    """
    does the similarity search on question and generates the answer

    Args:
        question : question for which answer is needed
        is_citation : whether the citation is required or not for the answer

    Returns:
        str: answer

    """
    collection_name = COLLECTION_NAME
    try:
        if utility.has_collection(collection_name, timeout=2):

            collection = Collection(name=collection_name)
            load = utility.load_state(collection_name)
            if str(load) == NOTLOAD:
                collection.load()

            # Search parameters for the index
            search_params={
                "metric_type": "L2",
                "params": {"nprobe": 128}
            }

            # these parameters are for searching. same as similarity search
            results=collection.search(
                data=[create_embedding(question)],  # Embeded search value
                anns_field="embedding",  # Search across embeddings
                param=search_params,
                limit=int(LIMIT),  # Limit to five results per search
                # Include title field in result
                consistency_level="Strong",
                output_fields=['content', 'file_name', 'page_no']
            )
            docs = []
            citations = []
            for doc in results[0]:
                row = []
                row.extend([doc.entity.get('content')])
                docs.append(row)
            response=get_result_from_pdf_doc(question,docs)
            if is_citation:
                for doc in results[0]:
                    citations.append({'document': doc.entity.get('file_name'), 'page_no': doc.entity.get('page_no')})
                    logger.info(f"Citations: {citations}")

            accuracy=calculate_accuracy(response[0], docs)
            confidence_scores=calculate_confidence_scores(response[0],docs)
            return response, citations, accuracy, confidence_scores[0]
    except Exception as e:
        raise e

