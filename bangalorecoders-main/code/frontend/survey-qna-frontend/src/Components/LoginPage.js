import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../Styles/LoginPage.css';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    // Add your authentication logic here (e.g., check username and password)
    // For simplicity, we'll just navigate to the dashboard if username and password are not empty
    if (username === 'test' && password === '123') {
        navigate('/dashboard/'+username+'/'+password);
    } else {
      alert('Invalid username or password');
    }
  };

  return (
    <div className='LoginContainer'>
      <div className='LoginHeader'>
        <h2>ESG Survey Response Automation</h2> 
      </div>

      <div className='LoginInfoBox'>
        <h2>Login</h2>
        <form onSubmit={handleSubmit} className='InputGroup'>
            <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            />
            <br />
            <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            />
            <br />
            <button type="submit">Login</button>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;