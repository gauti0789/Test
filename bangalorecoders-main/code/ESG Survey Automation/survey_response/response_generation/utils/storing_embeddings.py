import logging
import numpy as np
import openai
import os

from .constants import *
from dotenv import load_dotenv
from pymilvus import (
    Collection,
    CollectionSchema,
    DataType,
    FieldSchema,
    utility,
    connections
)


logger = logging.getLogger(__name__)

load_dotenv()

openai.api_key = os.environ['openai_api_key']
openai.api_type = os.environ['openai_api_type']
openai.api_base = os.environ['openai_api_base']
openai.api_version = os.environ['openai_api_version']
COLLECTION_NAME = os.environ['COLLECTION_NAME']
DIMENSION = os.environ['DIMENSION']
MILVUS_HOST = os.environ['MILVUS_HOST']
MILVUS_PORT = os.environ['MILVUS_PORT']
OPENAI_ENGINE = os.environ['OPENAI_ENGINE']
CONNECTION_NAME=os.environ['CONNECTION_NAME']
NUMBER_LIST=os.environ['NUMBER_LIST']
CONNECTION_NAME=os.environ['CONNECTION_NAME']


def create_embedding(text):
    """
    Generates embedding from text
    Args:
        text: the text that need to be converted into embedding
    Returns:
        str: The generated embedding.
    """
    return openai.Embedding.create(
        input=text, 
        deployment_id=OPENAI_ENGINE)["data"][0]["embedding"]


collection = None

def create_and_get_collection():
    global collection
    try:
        # Check if the collection has already been created
        if collection is None:
            collection_name = COLLECTION_NAME
            if utility.has_collection(collection_name):
                utility.drop_collection(collection_name)

            fields = [
                FieldSchema(name='id', dtype=DataType.INT64, descrition='Ids', is_primary=True, auto_id=True),
                FieldSchema(name='content', dtype=DataType.VARCHAR, description='content', max_length=3000),
                FieldSchema(name='file_name', dtype=DataType.VARCHAR, description='file name content belongs to', max_length=100),
                FieldSchema(name='page_no', dtype=DataType.INT64, descrition='page no'),
                FieldSchema(name='token_length', dtype=DataType.INT64, descrition='token length'),
                FieldSchema(name='year_of_report', dtype=DataType.VARCHAR, descrition='year_of_report',max_length=10),
                FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, description='Embedding generated from content',dim=int(DIMENSION))
            ]
            schema = CollectionSchema(fields=fields, description='PDF COLLECTION')
            collection = Collection(name=collection_name, schema=schema)

            index_params = {
                'index_type': 'IVF_FLAT',
                'metric_type': 'L2',
                'params': {'nlist': int(NUMBER_LIST)}
            }

            collection.create_index(field_name="embedding", index_params=index_params)

        return collection
    except Exception as error:
        raise error

def store_chunks(chunks,collection):
    input_tokens = 0
    try:
        for text, file_name, page_number, token_length,year_of_report in chunks:
            embedding = np.array(create_embedding(text))
            input_tokens += token_length

            logger.info(f"Embedding shape: {embedding.shape}")
            logger.info("Page Number: %s, Token Length: %s, File Name: %s, Year of Report: %s, Text Length: %s", page_number, token_length, year_of_report, file_name, len(text))

            field = [[text], [file_name], [page_number], [token_length],[year_of_report], [embedding]]
            collection.insert(field)    
    except Exception as error:
        error_message = f"An error has occured {error}"
        logger.error(error_message)
        raise Exception(error_message)