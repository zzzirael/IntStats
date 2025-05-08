import React from 'react';
import HomePage from './pages/HomePage';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Profile from './pages/Profile';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/profile/:puuid" element={<Profile />} /> {/* Alterado para "perfil" */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;