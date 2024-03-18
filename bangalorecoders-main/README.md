# ESG Survey Automation

## Overview


ESG Survey Automation is a web application developed to streamline the process of managing and analyzing ESG (Environmental, Social, and Governance) reports. The application allows users to upload multiple reports, upload questionnaire PDFs, generate response answers as PDFs, provide answers to specific questions with citations, list uploaded documents, and check the status of report generation.

## Technologies Used

- **Frontend**: React
- **Backend**: Django
- **Database**: Milvus
- **Containerization**: Docker Desktop

## Architecture

The application follows a microservices architecture, with separate components for the frontend, backend, and database. Communication between these components is managed through RESTful APIs.

- **Frontend**: Developed using React, the frontend component provides the user interface for interacting with the application. It communicates with the backend API to fetch and display data.

- **Backend**: Built using Django, the backend component serves as the server-side logic for the application. It handles client requests, processes data, and interacts with the Milvus database to store and retrieve vector data.

- **Database**: The application uses Milvus as the vector store database for efficient storage and retrieval of high-dimensional vector data. Milvus is deployed as a Docker container using Docker Desktop.


## How to Access Publicly Deployed Application

-- **Web Application**: Web Application deployed and running on Azure VM, can be accessed at this url: **http://172.174.211.63:3000/**. On accessing this it will ask for credentials. Enter username: test, password: 123

-- **API(s)**: Backend APIs are also deployed and running at **http://172.174.211.63:8000/**. The different API routes are:
1. Health Check Api: **http://172.174.211.63:8000/api/esgreports/keepalive/ping**
   <img width="628" alt="image" src="https://github.com/Hackathon2024-March/bangalorecoders/assets/54638989/c22211f9-d5ec-4250-9c8d-02c12ff6cf01">

3. Upload the ESG Reports: http://172.174.211.63:8000/api/esgreports/upload
   <img width="538" alt="image" src="https://github.com/Hackathon2024-March/bangalorecoders/assets/54638989/c2814403-ebf4-4424-99af-34082df33d7a">

5. Retrieve response for the specific question: http://172.174.211.63:8000/api/questionnaire/generatefirstdraft/generateAnswer
   <img width="536" alt="image" src="https://github.com/Hackathon2024-March/bangalorecoders/assets/54638989/9fbb8678-c652-4f27-a730-3807985e53a5">

7. Download the First Draft Report: http://172.174.211.63:8000/api/firstdraftreport/download/result/:reportYear
   <img width="535" alt="image" src="https://github.com/Hackathon2024-March/bangalorecoders/assets/54638989/fcc31c00-18bf-4f0b-b177-415542980b31">

9. Upload the Survey Questionnire: http://172.174.211.63:8000/questionnaire/generatefirstdraft/pdf
   <img width="541" alt="image" src="https://github.com/Hackathon2024-March/bangalorecoders/assets/54638989/02fccbf7-4e98-4ebc-87bc-0b9a54229710">

6. Retrieve list all the uploaded ESG reports: http://172.174.211.63:8000/api/esgreports/retrieve
   <img width="544" alt="image" src="https://github.com/Hackathon2024-March/bangalorecoders/assets/54638989/3b4ae690-3e6f-4b1c-af8c-a7095b1ac374">

7. Find status of the Survey Questionnire: http://172.174.211.63:8000/questionnaire/generatefirstdraft/pdf/:reportYear/:TaskId/status
   <img width="519" alt="image" src="https://github.com/Hackathon2024-March/bangalorecoders/assets/54638989/b042b29b-970d-4d34-844c-d639f2a1dd87">

_**Note:**_
_Sometimes on hitting the ping URL or the Frontend Application, it is not able to respond. This is due to automatic shutting down of deployed docker containers in the VM, This cause the deplyed applications to stop running and requires VM restart.
In this case you need to run the backend and frontend applications locally, the steps for which are provided in detail below._

## Running the Application

### Prerequisites

- Docker Desktop installed on your machine
- Python 3.11 installed on your machine
- Node.js and npm installed for running the frontend (if not already installed)

### Frontend

1. Navigate to the `code/frontend/survey-qna-frontend` directory.
2. Install dependencies by running `npm install`.
3. Start the development server with `npm start`.
4. Access the frontend application at `http://localhost:3000`.
5. Enter credentials. Username: test, Password: 123. On successful login it will navigate to the dashboard page of the application.

### Backend

1. Navigate to the `/code/ESG Survey Automation/survey_response/` directory.
2. Open Docker Desktop to run Docker Images.
3. Start Docker Conatiners with `docker-compose up -d`
4. Verify all 3 docker containers are running.
5. Create a virtual environment by running `python -m venv myenv`.
6. Activate the virtual environment:
   - On Windows: `myenv\Scripts\activate`
   - On macOS and Linux: `source myenv/bin/activate`
7. Install dependencies with `pip install -r requirements.txt`.
8. Make sure all dependencies should install without errors.
9. Run the Django server with `python manage.py runserver`.
10. The backend API will be accessible at `http://localhost:8000`.

_**Note:**
If you are trying to run backend and frontend from your local system, you need to modify the baseurl location in frontend code.
In **`code\frontend\survey-qna-frontend\src\config.js`** file, change the config property to **BASE_URL: 'http://localhost:8000/api'**. and then start React app_
