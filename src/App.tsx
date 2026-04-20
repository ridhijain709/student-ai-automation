import { Calendar, MessageSquare, Bot, CheckCircle2 } from 'lucide-react';

const offers = [
  {
    name: 'WhatsApp Lead Follow-up System',
    icon: MessageSquare,
    outcome: 'Instant acknowledgement + timed follow-ups so no enquiry gets ignored.',
    status: 'Demo-ready',
  },
  {
    name: 'Content Calendar + Auto-Scheduler',
    icon: Calendar,
    outcome: 'Weekly content planning and queueing for consistent posting with less manual effort.',
    status: 'Simulation-first',
  },
  {
    name: 'AI Query Auto-Responder',
    icon: Bot,
    outcome: 'Incoming queries are triaged and answered with structured AI-assisted drafts.',
    status: 'Demo-ready',
  },
];

const industries = ['Coaching institutes', 'Clinics', 'CA firms', 'Retail/FMCG distributors', 'Local service businesses'];

export default function App() {
  return (
    <main className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-6xl px-6 py-12">
        <header className="mb-10">
          <p className="mb-3 inline-block rounded-full bg-blue-100 px-3 py-1 text-sm font-medium text-blue-800">
            SME AI Automation Portfolio
          </p>
          <h1 className="text-3xl font-bold text-slate-900 md:text-4xl">
            Productized AI automations for SMEs that need faster follow-up and cleaner operations.
          </h1>
          <p className="mt-4 max-w-3xl text-slate-600">
            This repository showcases three practical automation offers with transparent demo scope. Built to support client demos on GitHub, LinkedIn, and discovery calls.
          </p>
        </header>

        <section className="mb-10 grid grid-cols-1 gap-5 md:grid-cols-3">
          {offers.map((offer) => (
            <article key={offer.name} className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="mb-3 flex items-center justify-between">
                <offer.icon className="h-8 w-8 text-blue-700" />
                <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-medium text-slate-700">{offer.status}</span>
              </div>
              <h2 className="text-lg font-semibold text-slate-900">{offer.name}</h2>
              <p className="mt-2 text-sm text-slate-600">{offer.outcome}</p>
            </article>
          ))}
        </section>

        <section className="mb-10 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-slate-900">How this portfolio is used in client conversations</h2>
          <ul className="mt-4 space-y-2 text-slate-700">
            <li className="flex gap-2"><CheckCircle2 className="mt-0.5 h-4 w-4 text-green-600" />Pick one workflow based on business pain-point.</li>
            <li className="flex gap-2"><CheckCircle2 className="mt-0.5 h-4 w-4 text-green-600" />Demo with sample data before requesting live credentials.</li>
            <li className="flex gap-2"><CheckCircle2 className="mt-0.5 h-4 w-4 text-green-600" />Deploy a lightweight version first, then scale after proof.</li>
          </ul>
        </section>

        <section className="mb-10 rounded-xl border border-amber-200 bg-amber-50 p-6">
          <h2 className="text-xl font-semibold text-amber-900">Live vs demo transparency</h2>
          <p className="mt-3 text-amber-900">
            No production credentials are stored in this repository. External channels (WhatsApp/social schedulers) are demonstrated through safe simulation flow unless client-owned integrations are connected.
          </p>
        </section>

        <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-slate-900">Target sectors</h2>
          <div className="mt-4 flex flex-wrap gap-2">
            {industries.map((industry) => (
              <span key={industry} className="rounded-full bg-slate-100 px-3 py-1 text-sm text-slate-700">{industry}</span>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}
