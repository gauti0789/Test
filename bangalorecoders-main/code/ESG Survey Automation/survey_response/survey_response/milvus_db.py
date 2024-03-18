from dotenv import load_dotenv

import os
load_dotenv()

from pymilvus import connections
from pymilvus.exceptions import MilvusException

import logging 
logger = logging.getLogger(__name__)


MILVUS_HOST = os.environ['MILVUS_HOST']
MILVUS_PORT = os.environ['MILVUS_PORT']
CONNECTION_NAME = os.environ['CONNECTION_NAME']

class VectorDB:

    @staticmethod
    def connect():
        try:
            logger.info("connecting to db")
            connections.connect(CONNECTION_NAME,host='localhost', port=MILVUS_PORT)
            logger.info("connected to vector db")
        except MilvusException as error:
            logger.error(f"error occured while connectiong to milvus DB: {error}")
            raise(error)