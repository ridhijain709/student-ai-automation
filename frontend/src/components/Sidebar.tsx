import { Link } from "react-router-dom";

export default function Sidebar() {
  return (
    <div className="w-64 bg-gray-800 text-white h-screen p-4 flex flex-col space-y-2">
      <Link to="/" className="p-2 hover:bg-gray-700 rounded">Dashboard</Link>
      <Link to="/resume" className="p-2 hover:bg-gray-700 rounded">Resume</Link>
      <Link to="/truthgrid" className="p-2 hover:bg-gray-700 rounded">TruthGrid</Link>
      <Link to="/gmail" className="p-2 hover:bg-gray-700 rounded">Gmail</Link>
      <Link to="/linkedin" className="p-2 hover:bg-gray-700 rounded">LinkedIn</Link>
      <Link to="/telegram" className="p-2 hover:bg-gray-700 rounded">Telegram</Link>
      <Link to="/whatsapp" className="p-2 hover:bg-gray-700 rounded">WhatsApp</Link>
    </div>
  );
}
