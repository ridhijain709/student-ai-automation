import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import WhatsAppPage from './pages/WhatsAppPage';
import ContentSchedulerPage from './pages/ContentSchedulerPage';
import FAQBotPage from './pages/FAQBotPage';
import ResumePage from './pages/ResumePage';
import TruthGridPage from './pages/TruthGridPage';

export default function App() {
  return (
    <BrowserRouter>
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/whatsapp" element={<WhatsAppPage />} />
            <Route path="/content-scheduler" element={<ContentSchedulerPage />} />
            <Route path="/faq-bot" element={<FAQBotPage />} />
            <Route path="/resume" element={<ResumePage />} />
            <Route path="/truthgrid" element={<TruthGridPage />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}
