/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { LayoutDashboard, Linkedin, MessageSquare, FileText, Send, Bot } from 'lucide-react';

export default function App() {
  const automations = [
    { name: 'LinkedIn Automation', icon: Linkedin, status: 'Active' },
    { name: 'WhatsApp Automation', icon: MessageSquare, status: 'Idle' },
    { name: 'Resume Processing', icon: FileText, status: 'Active' },
    { name: 'Telegram Bot', icon: Send, status: 'Idle' },
    { name: 'Truth Grid AI', icon: Bot, status: 'Active' },
  ];

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">AutoFlow AI Dashboard</h1>
        <p className="text-gray-600">Manage and monitor your automated workflows.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {automations.map((auto) => (
          <div key={auto.name} className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
            <div className="flex items-center justify-between mb-4">
              <auto.icon className="w-8 h-8 text-blue-600" />
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${auto.status === 'Active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                {auto.status}
              </span>
            </div>
            <h2 className="text-lg font-semibold text-gray-900">{auto.name}</h2>
          </div>
        ))}
      </div>
    </div>
  );
}
