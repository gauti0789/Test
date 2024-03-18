import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../Styles/DashboardPage.css';
import API_CONFIG from '../config';

const UploadQuestionnaire = () => {
  const [questionYear, setQuestionYear] = useState('');
  const [questionDocumentName, setQuestionDocumentName] = useState('');
  const [questionsPdf, setQuestionsPdf] = useState([null]);
  const [response, setResponse] = useState(null);
  const [formMetaData, setFormMetaData] = useState('');

  const handleYearChange = (event) => {
    setQuestionYear(event.target.value);
  };
  
  const handleDocumentNameChange = (event) => {
    setQuestionDocumentName(event.target.value);
  };

  const handlePdfChange = (index, event) => {
    const newPdf = [...questionsPdf];
    newPdf[index] = event.target.files[0];
    setQuestionsPdf(newPdf);
  };

  const handleAddPdf = () => {
    setQuestionsPdf([...questionsPdf, null]);
  };

  const handleRemovePdf = (index) => {
    const newPdf = [...questionsPdf];
    newPdf.splice(index, 1);
    setQuestionsPdf(newPdf);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const md = '{"generateReportforYear":"' + questionYear +'","userId":"test"}'
    const formData = new FormData();
    
    formData.append('metadata', md);
    
    questionsPdf.forEach((pdf, index) => {
      formData.append('SurveyQuestionnaireDocumentName', pdf);
    });

    //formData.append('SurveyQuestionnaireDocumentName', questionsPdf);
    formData.append('documentName', questionDocumentName);
    formData.append('documentType', 'pdf');
    
    console.log(formData);

    for (let pair of formData.entries()) {
      console.log(pair[0] + ', ' + pair[1]);
    }

    try {
      const response = await axios.post(API_CONFIG.BASE_URL+'/questionnaire/generatefirstdraft/pdf', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      console.log(response)
      const responseData = response.data;
      setResponse(responseData);
      setResponse(`Task Id: ${responseData.taskid} \nStatus: ${responseData.status} \nCreated At: ${responseData.createAt}`);
      
    } catch (error) { 
      console.log(response)
      console.error('Error occurred while generating first draft:', error);
      setResponse(`Task Id: null \nStatus: null \nCreated At: null`);
    }

    // clearing submit fields
    setQuestionYear('');
    setFormMetaData('');
    setQuestionDocumentName('');
    setQuestionsPdf([null]);
    // Clear file input value
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach((input) => {
      input.value = null;
    });

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
        <div className='FileInputs'>
          {questionsPdf.map((pdf, index) => (
            <div key={index}>
              <input
                type="file"
                onChange={(event) => handlePdfChange(index, event)}
              />
              {index === questionsPdf.length - 1 && (
                <button type="button" onClick={handleAddPdf} className='Plusbutton'>+</button>
              )}
              {index > 0 && (
                <button type="button" onClick={() => handleRemovePdf(index)} className='Minusbutton'>-</button>
              )}
            </div>
          ))}
        </div>

        <input
          className='FileTextInputs'
          type="text"
          placeholder="Document Name"
          value={questionDocumentName}
          onChange={handleDocumentNameChange}
        />
        <div><button type="submit" className='ChatButtons'>Submit</button></div>
        
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

export default UploadQuestionnaire;
