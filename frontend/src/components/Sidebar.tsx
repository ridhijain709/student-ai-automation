import { Link } from "react-router-dom";

export default function Sidebar() {
  return (
    <div className="w-72 bg-gray-900 text-white min-h-screen p-5 flex flex-col">
      <div className="mb-8">
        <h1 className="text-xl font-bold">AI Automation Portfolio</h1>
        <p className="text-sm text-gray-300 mt-1">
          Client-ready business automation demos
        </p>
      </div>

      <div className="space-y-2">
        <Link to="/" className="block p-3 rounded hover:bg-gray-800">
          Dashboard
        </Link>

        <Link to="/whatsapp" className="block p-3 rounded hover:bg-gray-800">
          WhatsApp Lead Follow-up
        </Link>

        <Link to="/content-scheduler" className="block p-3 rounded hover:bg-gray-800">
          Content Auto-Scheduler
        </Link>

        <Link to="/faq-bot" className="block p-3 rounded hover:bg-gray-800">
          FAQ Auto-Reply Bot
        </Link>
      </div>

      <div className="mt-8 pt-4 border-t border-gray-700 text-sm text-gray-400">
        Built for CA firms, coaching centres, clinics, and SMEs
      </div>
    </div>
  );
}
