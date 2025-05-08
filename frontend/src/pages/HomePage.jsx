import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import React from 'react';
import Header from './Header';
import SearchBox from './SearchBox';

const HomePage = () => {
  return (
    <div className="home-page">
      <Header />
      <h1>IntStats!</h1>
      <SearchBox />
    </div>
  );
};
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<SearchBox />} />
        <Route path="/perfil/:puuid" element={<Perfil />} />
      </Routes>
    </Router>
  );
}

export default HomePage;