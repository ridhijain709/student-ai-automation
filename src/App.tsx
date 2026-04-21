/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { MessageSquare, CalendarDays, Bot } from 'lucide-react';

export default function App() {
  const automations = [
    { name: 'WhatsApp Lead Follow-up System', icon: MessageSquare, outcome: 'Faster lead response' },
    { name: 'Content Auto-Scheduler', icon: CalendarDays, outcome: 'Consistent monthly posting' },
    { name: 'FAQ Auto-Reply Bot', icon: Bot, outcome: 'Reduced repetitive support' },
  ];

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">AI Automation Portfolio</h1>
        <p className="text-gray-600">Client-ready demos for CA firms, coaching centres, clinics, local businesses, and SMEs.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {automations.map((auto) => (
          <div key={auto.name} className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
            <div className="flex items-center justify-between mb-4">
              <auto.icon className="w-8 h-8 text-blue-600" />
              <span className="px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                Demo
              </span>
            </div>
            <h2 className="text-lg font-semibold text-gray-900">{auto.name}</h2>
            <p className="mt-2 text-sm text-gray-600">{auto.outcome}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
