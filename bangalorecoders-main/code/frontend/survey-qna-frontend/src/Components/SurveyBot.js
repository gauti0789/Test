import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../Styles/DashboardPage.css';
import API_CONFIG from '../config';


const SurveyBot = () => {
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState([]);
  const [reportYear, setReportYear] = useState([]);
  const [responseMetaData, setResponseMetaData] = useState([]);
  const [showInfo, setShowInfo] = useState(false);

  const toggleInfo = () => {
    setShowInfo(!showInfo);
  };


  const handleYearChange = (event) => {
    setReportYear(event.target.value);
  };

  const handleQuestionSubmit = async (event) => {
    event.preventDefault();
    const newQuestion = event.target.question.value;
    if (newQuestion) {
      setQuestions([...questions, newQuestion]);

      const formData = new FormData();
      formData.append('reportYear', reportYear);
      formData.append('inputQuestion', newQuestion);

      console.log(formData);

      try {
        const response = await axios.post(API_CONFIG.BASE_URL+'/questionnaire/generatefirstdraft/generateAnswer', formData);
        const responseData = response.data;
        //setResponse(responseData);
        setAnswers([...answers, responseData.questionnireSummary.response]);
        let citationsString = "";
        responseData.questionnireSummary.citations.forEach((citation, index) => {
            citationsString += `Citation ${index + 1}: Document - ${citation.document}, Page No - ${citation.page_no}\n`;
        });


        const responseMessage = `Citations: \n${citationsString} \nDocument Reference: ${responseData.questionnireSummary.documentReference} \nAccuracy: ${responseData.questionnireSummary.accuracy} \nConfidence Score: ${responseData.questionnireSummary.confidenceScores} \nStatus: ${responseData.questionnireSummary.status}\n`

        setResponseMetaData([...responseMetaData, responseMessage]);

      } catch (error) {
        console.error('Error occurred while generating answer', error);
        setAnswers([...answers, 'Error occurred while generating answer']);
        const responseMessage = `Citation: null \nDocument Reference: null \nAccuracy: null \nConfidence Score: null \nStatus: null\n`
        setResponseMetaData([...responseMetaData, responseMessage]);

      }

      event.target.reset();
    }
  };

  const handleClearChat = (event) => {
    event.preventDefault();
    setQuestions([]);
    setAnswers([]);
  };

  return (
    <div className='QNAContainer'> {/* Remaining 60% of screen space */}

      <h3 className='UploadHeader'>Chat with Survey Bot</h3>
      
      <form onSubmit={handleQuestionSubmit} style={{ marginTop: '10px' }}>
        <input
          className='FileTextInputs'
          type="text"
          placeholder="Enter Report Year"
          value={reportYear}
          onChange={handleYearChange}
        />
        <input type="text" name="question" placeholder="Ask something..." className='AskSomethingBox'/>
        <button type="submit" className='ChatButtons'>Send</button>
        <button className='ChatButtons' onClick={handleClearChat}>Clear</button>
      </form>

      <div className='ChatScreen'> {/* Chatbot-like appearance */}
        {questions.map((question, index) => (
          <div>
          <div key={index} style={{ marginBottom: '10px' }}>
            <div className='QuestionText'>
              {question}
            </div>
          </div>

          <div key={index} style={{ marginBottom: '10px' }}>
          <div className='AnswerText'>
            {answers[index]}
          </div>
          <button onClick={toggleInfo} className='Infobutton'>ℹ️</button>
            {showInfo && (
              <div>
                <textarea
                  value={responseMetaData[index]}
                  readOnly
                  placeholder="Response Message"
                />
                <div>
                  <button onClick={toggleInfo} className='HideDetailsButton'>Hide details</button>
                </div>
              </div>
            )}
          </div>
          </div>
          
        ))}
        
      </div>
      
    </div>
  );
};

export default SurveyBot;
