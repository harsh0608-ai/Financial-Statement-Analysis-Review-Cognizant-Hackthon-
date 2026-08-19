import { useState, useEffect } from 'react';

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AboutUs from './AboutUs';
import UploadPage1 from './Upload1';
import DashboardPage from './DashboardPage';
import TableReportPage from './Table';

function App() {
  
  return (
    <Router>
      <Routes>
        <Route path="/" element={<AboutUs />} />
        <Route path="/upload" element={<UploadPage1 />} />
        <Route path="/dash" element={<DashboardPage />} />
        <Route path="/table" element={<TableReportPage />} />
      </Routes>
    </Router>
  );
}
export default App;