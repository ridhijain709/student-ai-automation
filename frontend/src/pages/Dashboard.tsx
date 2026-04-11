import { useState, useEffect } from 'react';
import { LayoutDashboard, Mail, Send, Linkedin, MessageSquare, FileText, Bot } from 'lucide-react';

interface Task {
  id: number;
  title: string;
}

interface SummaryData {
  tasks_by_priority: {
    [key: string]: Task[];
  };
  urgent_messages: number;
  pending_followups: number;
  emails_action: number;
  truthgrid_recent: any[];
}

export default function Dashboard() {
  const [summary, setSummary] = useState<SummaryData | null>(null);

  useEffect(() => {
    fetch('/dashboard/summary')
      .then(res => res.json())
      .then(setSummary);
  }, []);

  const modules = [
    { name: 'Gmail', icon: Mail, path: '/gmail' },
    { name: 'Telegram', icon: Send, path: '/telegram' },
    { name: 'LinkedIn', icon: Linkedin, path: '/linkedin' },
    { name: 'WhatsApp', icon: MessageSquare, path: '/whatsapp' },
    { name: 'Resume', icon: FileText, path: '/resume' },
    { name: 'TruthGrid', icon: Bot, path: '/truthgrid' },
  ];

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-8">
        {modules.map((m) => (
          <a key={m.name} href={m.path} className="p-6 bg-white rounded-lg shadow border hover:shadow-md transition-shadow">
            <m.icon className="w-8 h-8 mb-2 text-blue-600" />
            <h2 className="font-semibold">{m.name}</h2>
          </a>
        ))}
      </div>

      {summary && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {Object.entries(summary.tasks_by_priority).map(([priority, tasks]: [string, Task[]]) => (
            <div key={priority} className="bg-white p-6 rounded-lg shadow">
              <h2 className="text-xl font-semibold mb-4">{priority} Tasks</h2>
              {tasks.map(t => (
                <div key={t.id} className="border-b py-2">{t.title}</div>
              ))}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
