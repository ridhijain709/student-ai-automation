import { Link } from "react-router-dom";

export default function Sidebar() {
  return (
    <div className="w-64 bg-gray-800 text-white h-screen p-4 flex flex-col space-y-2">
      <Link to="/" className="p-2 hover:bg-gray-700 rounded">Portfolio Dashboard</Link>
      <Link to="/whatsapp" className="p-2 hover:bg-gray-700 rounded">WhatsApp Lead Follow-up</Link>
      <Link to="/content-calendar-auto-scheduler" className="p-2 hover:bg-gray-700 rounded">Content Calendar + Scheduler</Link>
      <Link to="/ai-query-auto-responder" className="p-2 hover:bg-gray-700 rounded">AI Query Auto-Responder</Link>
      <Link to="/telegram" className="p-2 hover:bg-gray-700 rounded">Inbox Simulation Lab</Link>
      <Link to="/resume" className="p-2 hover:bg-gray-700 rounded">Proposal Copy Helper</Link>
      <Link to="/truthgrid" className="p-2 hover:bg-gray-700 rounded">Discovery Scorecard</Link>
    </div>
  );
}
