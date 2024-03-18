import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginPage from './Components/LoginPage';
import DashboardPage from './Components/DashboardPage';
import DashboardPage2 from './Components/DashboardPage2';

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<LoginPage/>} />
        <Route path="/dashboard/:username/:password" element={<DashboardPage2/>} />
        <Route path="/dashboard" element={<DashboardPage2/>} />
      </Routes>
    </Router>
  );
}

export default App;
