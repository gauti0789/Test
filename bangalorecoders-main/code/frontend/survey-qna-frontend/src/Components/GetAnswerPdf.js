import React, { useState } from 'react';
import axios from 'axios';
import '../Styles/DashboardPage.css';
import API_CONFIG from '../config';

const GetAnswerPdf = () => {
  const [questionYear, setQuestionYear] = useState('');
  const [response, setResponse] = useState(null);

  const handleYearChange = (event) => {
    setQuestionYear(event.target.value);
  };
  
  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      
      const response = await axios.get(API_CONFIG.BASE_URL+'/firstdraftreport/download/result/'+questionYear, {
        // Add any necessary data for your API call
        // For example, if you need to send any parameters in the request body
      }, {
        responseType: 'blob', // Set the response type to 'blob' to receive a binary response
      });

      // Create a Blob object from the response data
      const pdfBlob = new Blob([response.data], { type: 'application/pdf' });

      // Create a link element to download the PDF
      const downloadLink = document.createElement('a');
      downloadLink.href = window.URL.createObjectURL(pdfBlob);
      downloadLink.download = 'SurveyAnswer'+questionYear+'.pdf'; // Set the filename for the downloaded file

      // Append the link to the body
      document.body.appendChild(downloadLink);

      // Trigger the download
      downloadLink.click();

      // Remove the link from the body
      document.body.removeChild(downloadLink);
      console.log(response);
      setResponse(`Answer document generated and downloaded`);

    } catch (error) { 
      console.error('Error occurred while generating Answer:', error);
      setResponse(`Error Generating Answer document`);
    }

    // clearing submit fields
    setQuestionYear('');

  };

  const handleClearResponse = () => {
    setResponse(null);
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          className='FileTextInputs'
          type="text"
          placeholder="Question Year"
          value={questionYear}
          onChange={handleYearChange}
        />
        <div><button type="submit" className='ChatButtons'>Retrieve Answer Pdf Document</button></div>
        
      </form>
      {response && (
        <div>
          <textarea
            rows="3"
            cols="50"
            value={response}
            readOnly
            placeholder="Response Message"
          />
          <br/>
          <button onClick={handleClearResponse} className='HideDetailsButton'>Clear Response</button>
        </div>
      )}
    </div>
  );
};

export default GetAnswerPdf;
