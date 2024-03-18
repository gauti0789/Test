import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../Styles/DashboardPage.css';
import API_CONFIG from '../config';

const UploadSurveyDocuments = () => {

  const [documentNames, setDocumentNames] = useState([null]);
  const [documentUrls, setDocumentUrls] = useState(['']);
  const [year, setYear] = useState('');
  const [responseMessage, setResponseMessage] = useState('');
  const [showResponse, setShowResponse] = useState(false);

  const handleYearChange = (event) => {
    setYear(event.target.value);
  };

  const handleNameChange = (index, event) => {
    const newNames = [...documentNames];
    newNames[index] = event.target.files[0];
    setDocumentNames(newNames);
  };

  const handleUrlChange = (index, event) => {
    const newUrls = [...documentUrls];
    newUrls[index] = event.target.value;
    setDocumentUrls(newUrls);
  };

  const handleAddDocument = () => {
    setDocumentNames([...documentNames, null]);
    setDocumentUrls([...documentUrls, '']);
  };

  const handleRemoveDocument = (index) => {
    const newNames = [...documentNames];
    const newUrls = [...documentUrls];
    newNames.splice(index, 1);
    newUrls.splice(index, 1);
    setDocumentNames(newNames);
    setDocumentUrls(newUrls);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append('YearOfReport', year);
    
    documentNames.forEach((name, index) => {
      formData.append('documentName', name);
      formData.append('DocumentURL', documentUrls[index]);
    });
    
    //formData.append('documentName', documentNames);
    //formData.append('DocumentURL', documentUrls);
    
    console.log(formData);
    for (let pair of formData.entries()) {
      console.log(pair[0] + ', ' + pair[1]);
    }
    
    try {
      //const response = await axios.post('{{baseUrl}}/esgreports/upload', formData);
      const response = await axios.post(API_CONFIG.BASE_URL+'/esgreports/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      console.log(response)
      const responseData = response.data;
      setResponseMessage(`Status: ${responseData.status} \nMessage: ${responseData.message} \nTracker ID: ${responseData.trackerId} \n`);
    } catch (error) {
      console.error('Error occurred while uploading:', error);
      setResponseMessage(`Status: Error occurred while uploading \nMessage: Error occurred while uploading \nTracker ID: null \n`);
    }

    setShowResponse(true);
    setYear('');
    setDocumentNames([null]);
    setDocumentUrls(['']);

    // Clear file input value
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach((input) => {
      input.value = null;
    });
  };

  const handleClearResponse = () => {
    setShowResponse(false);
    setResponseMessage('');
  };


  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          className='FileTextInputs'
          type="text"
          placeholder="Year of Report"
          value={year}
          onChange={handleYearChange}
        />
        <div className='FileInputs'>
          {documentNames.map((name, index) => (
            <div key={index}>
              <input
                type="file"
                onChange={(event) => handleNameChange(index, event)}
              />
              <input
                type="text"
                placeholder="Document URL"
                value={documentUrls[index]}
                onChange={(event) => handleUrlChange(index, event)}
              />
              {index === documentNames.length - 1 && (
                <button type="button" onClick={handleAddDocument} className='Plusbutton'>+</button>
              )}
              {index > 0 && (
                <button type="button" onClick={() => handleRemoveDocument(index)} className='Minusbutton'>-</button>
              )}
            </div>
          ))}
        </div>
        <button type="submit" className='ChatButtons'>Submit</button>
      </form>
      {showResponse && (
        <div>
          <textarea
            rows="3"
            cols="50"
            value={responseMessage}
            readOnly
            placeholder="Response Message"
          />
          <br/>
          <div><button onClick={handleClearResponse} className='HideDetailsButton'>Clear Response</button></div>
        </div>
      )}
    </div>
      );
};

export default UploadSurveyDocuments;
