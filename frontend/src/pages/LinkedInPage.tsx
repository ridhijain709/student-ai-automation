export default function LinkedInPage() {
  const weeklyPlan = [
    { day: 'Monday', task: 'Generate 3 educational post ideas from business offers' },
    { day: 'Wednesday', task: 'Approve final captions + hooks' },
    { day: 'Friday', task: 'Queue next week posts in scheduler tool' },
  ];

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-2">Content Calendar + Auto-Scheduler</h1>
      <p className="text-gray-600 mb-6">
        Productized workflow for planning, drafting, and scheduling content in weekly batches.
      </p>

      <div className="bg-white border rounded-lg p-6 shadow mb-6">
        <h2 className="text-xl font-semibold mb-3">What this offer includes</h2>
        <ul className="list-disc ml-6 space-y-2 text-gray-700">
          <li>Monthly theme mapping based on client service priorities.</li>
          <li>AI-assisted caption draft generation with human approval.</li>
          <li>Batch scheduling process using a chosen scheduler tool.</li>
        </ul>
      </div>

      <div className="bg-white border rounded-lg p-6 shadow mb-6">
        <h2 className="text-xl font-semibold mb-3">Example weekly execution</h2>
        <div className="space-y-3">
          {weeklyPlan.map((item) => (
            <div key={item.day} className="border-l-4 border-blue-500 pl-4 py-1">
              <p className="font-semibold">{item.day}</p>
              <p className="text-gray-700">{item.task}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 text-amber-900">
        <strong>Demo scope:</strong> This page demonstrates the operating model. Direct posting integrations are configured with client-owned scheduler accounts during onboarding.
      </div>
    </div>
  );
}
