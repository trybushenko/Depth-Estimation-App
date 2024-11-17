// src/App.tsx

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import ImageUploadPage from './components/ImageUploadPage';
import CameraStreamPage from './components/CameraStreamPage';

const App: React.FC = () => {
  return (
    <Router>
      <Navbar />
      
      <Routes>
        <Route path="/" element={<ImageUploadPage />} />
        <Route path="/camera-stream" element={<CameraStreamPage />} />
        {/* Add more routes here if needed */}
      </Routes>
    </Router>
  );
};

export default App;
