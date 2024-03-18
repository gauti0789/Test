import asyncio
import concurrent.futures
import io
import logging 
import json
import openai
from pymilvus.exceptions import (
    ConnectionNotExistException,
    MilvusException,
    MilvusUnavailableException,
)
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from ..utils import (
    text_extract,
    storing_embeddings,
    get_answer_from_pdf,
    insertion_into_milvus,
)
from ..utils.constants import *
import uuid

logger = logging.getLogger(__name__)

REQUEST_INFO = []

class ESGUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        """
            API endpoint for uploading ESG reports.

            Input:
            - PDF files: 'documentName' field in request.FILES
            - Year of report: 'YearOfReport' field in request.POST
            - Document URLs: 'DocumentURL' field in request.POST

            Output:
            - Status: HTTP status code indicating success or failure
            - Message: Message indicating the result of the operation
            - Tracker ID: Unique identifier for the uploaded report
        """
        try:
            pdf_files = request.FILES.getlist('documentName')
            year_of_report = request.POST.get('YearOfReport')
            document_urls = request.POST.getlist('DocumentURL')
            logger.info(year_of_report)
            logger.info(pdf_files)
            logger.info(document_urls)

            if not year_of_report or not document_urls or not pdf_files:
                return Response({"error_message":NO_FILES_SELECTED_ERROR}, status=status.HTTP_400_BAD_REQUEST)

            if not year_of_report:
                return Response({"error_message":INVALID_INPUT}, status=status.HTTP_400_BAD_REQUEST)

            if len(pdf_files) > DOCUMENT_LIMIT:
                return Response({"error_message":DOCUMENT_LIMIT_EXCEEDED_ERROR_MESSAGE.format(DOCUMENT_LIMIT)},
                                status=status.HTTP_406_NOT_ACCEPTABLE)

            total_size = sum(file.size for file in pdf_files)
            if total_size > FILE_UPLOAD_MAX_MEMORY_SIZE:
                return Response({"error_message":MEMORY_SIZE_ERROR_MESSAGE}, status=status.HTTP_406_NOT_ACCEPTABLE)

            for file in pdf_files:
                # Check if the file is a PDF
                if not file.name.lower().endswith('.pdf'):
                    return Response({"error_message":INVALID_FILE_TYPE_ERROR}, status=status.HTTP_400_BAD_REQUEST)

             # Create a unique tracker ID
            tracker_id = str(uuid.uuid4())

            # Store request data with the tracker ID in a constant dict
            document_names = [file.name for file in pdf_files]
            document_urls_str = document_urls[0]
            document_urls_list = json.loads(document_urls_str)
            request_details={
                'trackerId':tracker_id,
                'YearOfReport': year_of_report,
                'DocumentURL':  document_urls_list,
                'DocumentName': document_names
            }
            REQUEST_INFO.append(request_details)
            logger.info(f"Request stored with tracker ID: {REQUEST_INFO}")

            # Process the uploaded PDF files
            collection = storing_embeddings.create_and_get_collection()
            logger.info("collection-create")
            with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
                futures = [executor.submit(text_extract.extract_and_generate_index_from_pdf_doc,
                                           thread_number, file_obj,year_of_report)
                           for thread_number, file_obj in enumerate(pdf_files, start=1)]

                concurrent.futures.wait(futures)

                results = []
                for future in concurrent.futures.as_completed(futures):
                    result_array = future.result()
                    results.extend(result_array)
                logger.info(f"result length: {len(results)}")


            logger.info("Inserting into db")
            # Insert data into Milvus
            multithreading_insert = insertion_into_milvus.MilvusMultiThreadingInsert(
                collection_name=collection,
                chunks=results,
                no_of_files=len(pdf_files),
            )
            multithreading_insert.run()
            response_data = {
                'status': status.HTTP_201_CREATED,
                'message': 'Files processed successfully.',
                'trackerId': tracker_id
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        except openai.error.AuthenticationError as error:
            logger.error(str(error))
            error_message = INVALID_API_KEY
            return Response({"error_message": error_message}, status=status.HTTP_401_UNAUTHORIZED)
        except (MilvusException, ConnectionNotExistException, MilvusUnavailableException) as error:
            logger.error(str(error))
            error_message = UNABLE_TO_CONNECT_TO_VECTOR_DB
            return Response({"error_message": error_message}, status=525)
        except Exception as error:
            error_message = str(error)
            logging.error(f"Exception in upload/general-doc endpoint: {error}")
            return Response({"error_message": error_message}, status=525, content_type="application/json")




class AnswerAPIView(APIView):

    def post(self, request):

        """
        API endpoint for getting answers to questions.

        Input:
        - Input question: 'inputQuestion' field in request.data
        - Report year: 'reportYear' field in request.data

        Output:
        - Question: Input question
        - Response: Answer to the input question
        - Citations: List of citations (if any)
        """

        try:
            
            input_question = request.data.get('inputQuestion')
            report_year = request.data.get('reportYear')

            # Check if input_question and report_year are provided
            if not input_question or not report_year:
                return Response({"error_message":INVALID_INPUT}, status=status.HTTP_400_BAD_REQUEST)

            logger.info(f"Question: {input_question}")

            # Get answer related to the input_question
            logger.info("Getting answer related to input question")
            response_after_calling_GPT, citations, accuracy, confidence_scores = asyncio.run(self.get_answer_async({'question': input_question}, True))
            answer, input_tokens, output_tokens = response_after_calling_GPT
            logger.info(f"input_tokens: {input_tokens}, output_tokens; {output_tokens}")

            # Create response dictionary
            response = {
                "status": status.HTTP_201_CREATED,
                "question": input_question,
                "response": answer,
                "citations": citations,
            }

            citations = response.get('citations', [])
            documents = list(set(citation['document'] for citation in citations))
            response_dict={
            "reportYear": report_year,
            "questionnireSummary": {
                "response": answer,
                "status": status.HTTP_201_CREATED,
                "citations": citations,
                "documentReference":  documents,
                "accuracy": accuracy,
                "confidenceScores": confidence_scores
            }
            }


            logger.info("Returning as response")
            return Response( response_dict)

        except FileNotFoundError as error:
            error_message = FILE_NOT_FOUND
            logging.error(f"Exception in /interact endpoint: {error}")
            return Response({"error_message": error_message}, status=status.HTTP_404_NOT_FOUND, content_type="application/json")
        except openai.error.Timeout as error:
            logger.error(str(error))
            error_message = REQUEST_TIMEOUT_ERROR
            return Response({"error_message": error_message}, status=525)
        except (openai.error.APIConnectionError, openai.error.APIError) as error:    
            logger.error(str(error))
            error_message = API_CONNECTION_ERROR
            return Response({"error_message": error_message}, status=525)
        except openai.error.RateLimitError as error:
            logger.error(str(error))
            error_message = RATE_LIMIT_ERROR
            return Response({"error_message": error_message}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        except (MilvusException, ConnectionNotExistException, MilvusUnavailableException) as error:
            logger.error(str(error))
            error_message = UNABLE_TO_CONNECT_TO_VECTOR_DB
            return Response({"error_message": error_message}, status=525)
        except Exception as error:
            error_message = str(error)
            logging.error(f"Exception in /interact endpoint: {error_message}")
            return Response({"error_message": error_message}, status=525, content_type="application/json")

    async def get_answer_async(self, question, is_citation):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, get_answer_from_pdf.answer,question['question'], is_citation)


class ListReportAPIView(APIView):

    def post(self, request):

        """
        API endpoint for listing uploaded reports for a specific year.

        Input:
        - Report year: 'reportYear' field in request.data

        Output:
        - List of documents uploaded for the specified year
        """

        try:
            
            report_year = request.data.get('reportYear')

            # Check if input_question and report_year are provided
            if  not report_year:
                return Response({"error_message":INVALID_INPUT}, status=status.HTTP_400_BAD_REQUEST)

            logger.info(REQUEST_INFO)
            response = {"documents": []}
            for info in REQUEST_INFO:
                if info['YearOfReport'] == report_year:
                    for i in range(len(info['DocumentName'])):
                        document = {
                            "documentName": info['DocumentName'][i],
                            "metadata": {
                                "documentType": "PDF",
                                "referenceLink": info['DocumentURL'][i],
                                "generated By": "User1",
                                "reportYear": info['YearOfReport']
                            }
                        }
                        response["documents"].append(document)

            logger.info("Returning as response")
            return Response( response)

        except Exception as error:
            error_message = str(error)
            logging.error(f"Exception in /interact endpoint: {error_message}")
            return Response({"error_message": error_message}, status=525, content_type="application/json")
