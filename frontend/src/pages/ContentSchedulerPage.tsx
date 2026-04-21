export default function ContentSchedulerPage() {
  return (
    <div className="p-8 max-w-5xl">
      <h1 className="text-3xl font-bold text-gray-900 mb-2">
        Content Auto-Scheduler
      </h1>
      <p className="text-gray-600 mb-8">
        Turn a simple content sheet into generated captions and scheduled posts.
      </p>

      <div className="bg-white rounded-xl border p-6 mb-6">
        <h2 className="text-xl font-semibold mb-3">Business Problem</h2>
        <p className="text-gray-700">
          Small businesses struggle to post consistently and waste time writing captions manually.
        </p>
      </div>

      <div className="bg-white rounded-xl border p-6 mb-6">
        <h2 className="text-xl font-semibold mb-3">Solution</h2>
        <p className="text-gray-700">
          AI generates captions from content ideas and prepares them for scheduling on social platforms.
        </p>
      </div>

      <div className="bg-white rounded-xl border p-6 mb-6">
        <h2 className="text-xl font-semibold mb-3">Stack</h2>
        <ul className="list-disc pl-5 text-gray-700 space-y-1">
          <li>Google Sheets</li>
          <li>OpenAI / ChatGPT</li>
          <li>Buffer / Meta scheduler</li>
          <li>Zapier / Make</li>
        </ul>
      </div>

      <div className="bg-white rounded-xl border p-6">
        <h2 className="text-xl font-semibold mb-3">Outcome</h2>
        <p className="text-gray-700">
          More consistent posting, less manual work, and faster content production.
        </p>
      </div>
    </div>
  );
}
