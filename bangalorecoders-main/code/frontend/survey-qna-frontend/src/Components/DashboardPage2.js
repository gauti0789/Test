import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import UploadQuestionnaire from './UploadQuestionnaire';
import UploadSurveyDocuments from './UploadSurveyDocuments';
import GetAnswerPdf from './GetAnswerPdf';
import SurveyBot from './SurveyBot';
import '../Styles/DashboardPage.css';

const DashboardPage2 = () => {
  
  const { username, password } = useParams();
  const [user, setUser] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    setUser(username+password);
  }, [username,password]);

  if (user!=='test123') {
    navigate('/');
  }
  

  return (
    <div className='DashboardContainer'>
      <div className='DashboardHeader'>
        <h2>ESG Survey Response Automation</h2> 
      </div>
      <div className="Dashboard"> 
        
        <div style={{ display: 'flex' }}>
          <div className='PDFContainer'> {/* Set width to occupy 40% of screen space */}
            
          <h3 className='UploadHeader'>Upload PDF documents containing Survey Information</h3>

            { /* Upload documents list */}
            <UploadSurveyDocuments></UploadSurveyDocuments>


            <div className='SingleFileContainer'>
              <h3 className='UploadHeader'>Upload Questionnaire PDF file</h3>
              
               {/* new questionnaire code */}
               <UploadQuestionnaire></UploadQuestionnaire>
              <div>

              </div>
            </div>

            <div className='SingleFileContainer'>
              <h3 className='UploadHeader'>Download Survey Answer PDF</h3>
              
               {/* Download Survey Answer PDF code */}
               <GetAnswerPdf></GetAnswerPdf>
              <div>

              </div>
            </div>

          </div>

          { /* Survey Question Answer bot */ }
          
          <SurveyBot></SurveyBot>

        </div>
      </div>
    </div>
  );
};

export default DashboardPage2;
