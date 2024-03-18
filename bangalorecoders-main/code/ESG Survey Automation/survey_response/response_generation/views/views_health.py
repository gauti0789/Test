from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class HealthView(APIView):
    def get(self, request):
        """
        API endpoint for checking the health status of the application.

        Input:
        - None

        Output:
        - Status: HTTP status indicating the health status (200 OK)
        - Message: Information message indicating that the API is healthy
        """
        try:
            # Define response dictionary
            response_dict = {
                'status': status.HTTP_200_OK,
                'message': "API is healthy"
            }

            # Return response
            return Response(response_dict, status=status.HTTP_200_OK)

        except Exception as e:
            # Log any errors
            logger.error(f"Error in HealthView: {str(e)}")
            # Return error response
            return Response({"error_message": "Error in checking health status"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
