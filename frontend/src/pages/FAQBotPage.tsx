export default function FAQBotPage() {
  return (
    <div className="p-8 max-w-5xl">
      <h1 className="text-3xl font-bold text-gray-900 mb-2">
        FAQ Auto-Reply Bot
      </h1>
      <p className="text-gray-600 mb-8">
        Automatically answer common customer questions using AI and messaging workflows.
      </p>

      <div className="bg-white rounded-xl border p-6 mb-6">
        <h2 className="text-xl font-semibold mb-3">Business Problem</h2>
        <p className="text-gray-700">
          Teams answer the same repetitive questions again and again, wasting time.
        </p>
      </div>

      <div className="bg-white rounded-xl border p-6 mb-6">
        <h2 className="text-xl font-semibold mb-3">Solution</h2>
        <p className="text-gray-700">
          AI detects the intent of incoming questions and drafts fast, accurate replies.
        </p>
      </div>

      <div className="bg-white rounded-xl border p-6 mb-6">
        <h2 className="text-xl font-semibold mb-3">Stack</h2>
        <ul className="list-disc pl-5 text-gray-700 space-y-1">
          <li>WhatsApp API / Telegram Bot</li>
          <li>OpenAI API</li>
          <li>Zapier / Make</li>
        </ul>
      </div>

      <div className="bg-white rounded-xl border p-6">
        <h2 className="text-xl font-semibold mb-3">Outcome</h2>
        <p className="text-gray-700">
          Fewer repetitive messages, faster replies, and lighter support workload.
        </p>
      </div>
    </div>
  );
}
