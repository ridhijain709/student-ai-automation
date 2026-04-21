export default function WhatsAppPage() {
  return (
    <div className="p-8 max-w-5xl">
      <h1 className="text-3xl font-bold text-gray-900 mb-2">
        WhatsApp Lead Follow-up System
      </h1>
      <p className="text-gray-600 mb-8">
        Automatically respond to new leads, confirm enquiries, and schedule follow-ups.
      </p>

      <div className="bg-white rounded-xl border p-6 mb-6">
        <h2 className="text-xl font-semibold mb-3">Business Problem</h2>
        <p className="text-gray-700">
          Businesses lose revenue when leads are not followed up quickly after enquiry.
        </p>
      </div>

      <div className="bg-white rounded-xl border p-6 mb-6">
        <h2 className="text-xl font-semibold mb-3">Solution</h2>
        <p className="text-gray-700">
          A simple automation that sends a WhatsApp message after form submission and
          follows up automatically after a delay.
        </p>
      </div>

      <div className="bg-white rounded-xl border p-6 mb-6">
        <h2 className="text-xl font-semibold mb-3">Stack</h2>
        <ul className="list-disc pl-5 text-gray-700 space-y-1">
          <li>Google Forms</li>
          <li>Google Sheets</li>
          <li>Zapier / Make</li>
          <li>WhatsApp API</li>
        </ul>
      </div>

      <div className="bg-white rounded-xl border p-6">
        <h2 className="text-xl font-semibold mb-3">Outcome</h2>
        <p className="text-gray-700">
          Faster response time, fewer missed leads, and a more professional customer experience.
        </p>
      </div>
    </div>
  );
}
