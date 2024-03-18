import asyncio
import io
import re
import logging 
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..utils.questionnaire_utils import generate_pdf_with_answers
from ..utils.constants import *
import uuid
import json
import os
from datetime import datetime
from django.http import HttpResponse


report_info = {}
logger = logging.getLogger(__name__)

class SurveyQuestionnaireUpload(APIView):

    def post(self, request):

        """
            API endpoint for uploading a survey questionnaire and generating a PDF report.

            Input:
            - Uploaded questionnaire file: 'SurveyQuestionnaireDocumentName' field in request.FILES
            - Document type: 'documentType' field in request.POST
            - Document name: 'documentName' field in request.POST
            - Metadata: 'metadata' field in request.POST, containing:
                - generateReportforYear: Year for which the report needs to be generated
                - userId: User ID associated with the upload

            Output:
            - Task ID: Unique identifier for the generated report
            - Status: Indicates whether the operation was successful or not
            - Creation time: Timestamp indicating when the report was generated
        """

        try:
            # Get the uploaded file and metadata from the request
            questionnaire_file = request.FILES.get('SurveyQuestionnaireDocumentName')
            document_type = request.POST.get('documentType')
            document_name=request.POST.get('documentName')
            metadata_str = request.POST.get('metadata')  
            if metadata_str:
                metadata = json.loads(metadata_str)  # Parse metadata string into dictionary
                generate_report_for_year = metadata.get('generateReportforYear')
                user_id = metadata.get('userId')
            else:
                generate_report_for_year = None
                user_id = None

            taskid = str(uuid.uuid4())  

            if not (questionnaire_file and document_type and document_name and generate_report_for_year and user_id):
                return Response({"error_message":INVALID_INPUT}, status=status.HTTP_400_BAD_REQUEST)
    
            output_directory = "./reports"
            os.makedirs(output_directory, exist_ok=True)  
            output_file_path = os.path.join(output_directory, f"{taskid}_{generate_report_for_year}.pdf")
            # Define a function to run the async code synchronously
            def run_async_code_synchronously():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(
                    generate_pdf_with_answers(questionnaire_file, output_file_path)
                )

            # Run the async code synchronously
            run_async_code_synchronously()

            createAt = datetime.now().isoformat()

            response_data = {
                'taskid': taskid,
                'status': 'success',
                'createAt': createAt
            }
            report_info[generate_report_for_year] = response_data
            # Return the response
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as error:
            error_message = str(error)
            logging.error(f"Exception in upload/general-doc endpoint: {error}")
            return Response({"error_message": error_message}, status=525, content_type="application/json")


class ReportStatus(APIView):

    """
        API endpoint for fetching the status of a generated report.

        Input:
        - Report year: Year for which the report was generated (from path variable)
        - Task ID: Unique identifier of the report (from path variable)

        Output:
        - Status of the report: Indicates whether the report is in progress or completed
        - Task ID: Unique identifier of the report
        - Creation time: Timestamp indicating when the report was generated

    """
    def get(self, request, reportYear, TaskId):
        try:
            # Check if reportYear and TaskId are present in the path variables
            if not reportYear or not TaskId:
                return Response({"error_message": "reportYear and TaskId are required in the path"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if the report for the given reportYear and TaskId exists in report_info
            if reportYear in report_info and report_info[reportYear]['taskid'] == TaskId:
               return Response(report_info[reportYear], status=status.HTTP_200_OK)
            else:
                return Response({'status': 'in progress', 'taskid': TaskId, 'createAt': datetime.now().isoformat()}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in fetching report status: {str(e)}")
            return Response({"error_message": "Error in fetching report status"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReportPDF(APIView):

    """
        API endpoint for downloading a generated PDF report.

        Input:
        - Report year: Year for which the report was generated (from path variable)

        Output:
        - PDF file: Response containing the generated PDF report file
    """
    def get(self, request, reportYear):
        try:
            # Check if reportYear is present in the path variable
            if not reportYear:
                return Response({"error_message": "reportYear is required in the path"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Fetch the taskId from report_info based on reportYear
            if reportYear in report_info:
                taskId = report_info[reportYear].get('taskid')
                if taskId:
                    pdf_file_path = f"./reports/{taskId}_{reportYear}.pdf"
                    logger.info(pdf_file_path)
                    # Check if the PDF file exists
                    if os.path.exists(pdf_file_path):
                        logger.info("inside if") 
                        with open(pdf_file_path, 'rb') as file:
                            response = HttpResponse(file.read(), content_type='application/pdf')
                            response['Content-Disposition'] = f'attachment; filename="{reportYear}.pdf"'
                            return response
                       
                    else:
                        return Response({"error_message": "PDF file not found"}, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({"error_message": "TaskId not found for the given reportYear"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"error_message": "Report not found for the given reportYear"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in fetching report status: {str(e)}")
            return Response({"error_message": "Error in fetching report status"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


