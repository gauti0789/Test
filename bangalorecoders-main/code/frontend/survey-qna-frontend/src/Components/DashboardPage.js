import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import '../Styles/DashboardPage.css';

const DashboardPage = () => {
  const [multipleFiles, setMultipleFiles] = useState([]);
  const [singleFile, setSingleFile] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState([]);
  
  const { username, password } = useParams();
  const [user, setUser] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    setUser(username+password);
  }, [username]);

  if (user!=='test123') {
    navigate('/');
  }

  const handleMultipleFileChange = (event) => {
    const fileList = event.target.files;
    const newFiles = Array.from(fileList).filter(file => file.type === 'application/pdf');
    setMultipleFiles([...multipleFiles, ...newFiles]);
  };

  const handleSingleFileChange = (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      setSingleFile(file);
    } else {
      setSingleFile(null);
      alert('Please select a valid PDF file.');
    }
  };

  const handleQuestionSubmit = (event) => {
    event.preventDefault();
    const newQuestion = event.target.question.value;
    if (newQuestion) {
      setQuestions([...questions, newQuestion]);
      // Dummy answer for demonstration
      setAnswers([...answers, "This is just a dummy answer for "+newQuestion]);
      event.target.reset();
    }
  };

  const handleClearChat = (event) => {
    event.preventDefault();
    setQuestions([]);
    setAnswers([]);
  };

  return (
    <div className='DashboardContainer'>
      <div className='DashboardHeader'>
        <h2>ESG Survey Response Automation</h2> 
      </div>
      <div className="Dashboard"> 
        
        <div style={{ display: 'flex' }}>
          <div className='PDFContainer'> {/* Set width to occupy 40% of screen space */}
            <div className='MultipleFilesContainer'>
              <h3 className='UploadHeader'>Upload PDF documents containing Survey Information</h3>
              <div>
                <input className='FileInputText'
                  type="file"
                  id="multiplefile"
                  accept="application/pdf"
                  multiple
                  onChange={handleMultipleFileChange}
                />
                <label for="multiplefile" className='FileInputLabel'>Select files</label>
              </div>
              
              {multipleFiles.length!=0 && 
              <div className='UploadedFilesList'>
                <h4>Uploaded Files:</h4>
                <ul class="FileList">
                  {multipleFiles.map((file, index) => (
                    <li key={index}>{file.name}</li>
                  ))}
                </ul>
              </div>
              }
            </div>
            <div className='SingleFileContainer'>
              <h3 className='UploadHeader'>Upload Questionnaire PDF file</h3>
              <input className='FileInputText'
                type="file"
                id="singlefile"
                accept="application/pdf"
                onChange={handleSingleFileChange}
              />
              <label for="singlefile" className='FileInputLabel'>Select file</label>
              {singleFile && 
                <div><h4>Uploaded File:</h4> 
                <div className='UploadedSingleFile'>{singleFile.name}</div>
                </div>
              }
            </div>
          </div>
          <div className='QNAContainer'> {/* Remaining 60% of screen space */}

            <h3 className='UploadHeader'>Chat with Survey Bot</h3>
            
            <form onSubmit={handleQuestionSubmit} style={{ marginTop: '10px' }}>
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
                </div>
                </div>
                
              ))}
              
            </div>
            
          </div> 
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
