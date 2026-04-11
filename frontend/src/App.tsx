import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import GmailPage from './pages/GmailPage';
import TelegramPage from './pages/TelegramPage';
import LinkedInPage from './pages/LinkedInPage';
import WhatsAppPage from './pages/WhatsAppPage';
import ResumePage from './pages/ResumePage';
import TruthGridPage from './pages/TruthGridPage';

export default function App() {
  return (
    <BrowserRouter>
      <div className="flex">
        <Sidebar />
        <div className="flex-1">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/gmail" element={<GmailPage />} />
            <Route path="/telegram" element={<TelegramPage />} />
            <Route path="/linkedin" element={<LinkedInPage />} />
            <Route path="/whatsapp" element={<WhatsAppPage />} />
            <Route path="/resume" element={<ResumePage />} />
            <Route path="/truthgrid" element={<TruthGridPage />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}
