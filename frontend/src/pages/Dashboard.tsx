import { MessageSquare, CalendarDays, Bot, ArrowRight } from 'lucide-react';

export default function Dashboard() {
  const demos = [
    {
      title: 'WhatsApp Lead Follow-up System',
      description: 'Automate lead capture, instant replies, and scheduled follow-ups.',
      icon: MessageSquare,
      outcome: 'Fewer lost leads, faster conversions',
      path: '/whatsapp',
    },
    {
      title: 'Content Auto-Scheduler',
      description: 'Generate captions and schedule posts from a content sheet.',
      icon: CalendarDays,
      outcome: '30 days of content planned faster',
      path: '/content-scheduler',
    },
    {
      title: 'FAQ Auto-Reply Bot',
      description: 'Reply to common customer questions automatically with AI.',
      icon: Bot,
      outcome: 'Less support work, faster replies',
      path: '/faq-bot',
    },
  ];

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">AI Automation Portfolio</h1>
        <p className="text-gray-600 mt-2 max-w-2xl">
          Three client-ready automations designed to help businesses save time,
          respond faster, and convert more leads.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {demos.map((demo) => (
          <a
            key={demo.title}
            href={demo.path}
            className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
          >
            <div className="flex items-center justify-between mb-4">
              <demo.icon className="w-10 h-10 text-blue-600" />
              <ArrowRight className="w-5 h-5 text-gray-400" />
            </div>

            <h2 className="text-xl font-semibold text-gray-900">{demo.title}</h2>
            <p className="text-gray-600 mt-2">{demo.description}</p>

            <div className="mt-4 inline-flex items-center px-3 py-1 rounded-full bg-blue-50 text-blue-700 text-sm">
              {demo.outcome}
            </div>
          </a>
        ))}
      </div>

      <div className="mt-10 bg-white rounded-xl border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900">Target Clients</h3>
        <p className="text-gray-600 mt-2">
          CA firms, coaching centres, clinics, local businesses, and SMEs.
        </p>
      </div>
    </div>
  );
}
