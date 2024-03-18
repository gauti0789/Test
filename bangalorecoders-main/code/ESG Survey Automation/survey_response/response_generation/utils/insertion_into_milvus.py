import time

import numpy as np
from pymilvus import (
    Collection,
)
import threading
import concurrent
import logging
from .storing_embeddings import store_chunks

logger = logging.getLogger(__name__)

class MilvusMultiThreadingInsert:
    def __init__(self, collection_name,chunks,no_of_files):
        logger.info("In milvus store")
        self.thread_local = threading.local()
        self.collection_name = collection_name
        self.no_of_files = no_of_files
        chunks_length = len(chunks)
        logger.info(f"no of files :{no_of_files}")
        each_chunk_length = chunks_length//no_of_files
        logger.info(f"each chunk length that need to be processed by thread: {each_chunk_length}")
        self.chunks = []
        index = 0
        if no_of_files == 1:
            self.chunks = [chunks]
        else:
            while index+each_chunk_length <= chunks_length:
                logger.info(f"{index+each_chunk_length}")
                self.chunks.append(chunks[index:index+each_chunk_length])
                index += each_chunk_length

            if index < chunks_length:
                self.chunks[-1].extend(chunks[index:])

    def get_thread_local_collection(self):
        if not hasattr(self.thread_local, "collection"):
            self.thread_local.collection = Collection(self.collection_name)
        return self.thread_local.collection

    def insert_data(self,chunks):
        try:
            logger.info(f"lenght of chunks array that need to be processed: {len(chunks)}")
            store_chunks(chunks,self.collection_name)
        except Exception as error:
            error_message = f"An error has occured {error}"
            logger.error(error_message)
            raise Exception(error_message)
            

    def insert_all_batches(self):
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
                logger.info(f"lenght of chunks array that need to be processed: {len(self.chunks[0])}")
                executor.map(self.insert_data,self.chunks)
        except Exception as error:
            error_message = f"An error has occured {error}"
            logger.error(error_message)
            raise Exception(error_message)

    def run(self):
        try:
            start_time = time.time()
            self.insert_all_batches()
            duration = time.time() - start_time
            logger.info(f"duration :{duration}")
        except Exception as error:
            error_message = f"An error has occured {error}"
            logger.error(error_message)
            raise Exception(error_message)
        

    def insert_excel_data(self,chunks):
        store_excel_chunks(chunks,self.collection_name)
    
    def insert_all_excel_batches(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
            executor.map(self.insert_excel_data,self.chunks)

    def run_excel(self):
        start_time = time.time()
        self.insert_all_excel_batches()
        duration = time.time() - start_time
        logger.info(f"duration :{duration}")
        