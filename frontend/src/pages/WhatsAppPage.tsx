export default function WhatsAppPage() {
  const flow = [
    'Lead captured via form or sheet',
    'Instant acknowledgement sent on WhatsApp',
    '24-hour and 48-hour follow-up sequence queued',
    'Status logged for handoff/sales tracking',
  ];

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-2">WhatsApp Lead Follow-up System</h1>
      <p className="text-gray-600 mb-6">
        Entry-level automation offer for SMEs that lose enquiries due to delayed follow-up.
      </p>

      <div className="bg-white border rounded-lg p-6 shadow mb-6">
        <h2 className="text-xl font-semibold mb-3">Workflow</h2>
        <ol className="list-decimal ml-6 space-y-2 text-gray-700">
          {flow.map((step) => (
            <li key={step}>{step}</li>
          ))}
        </ol>
      </div>

      <div className="bg-white border rounded-lg p-6 shadow mb-6">
        <h2 className="text-xl font-semibold mb-3">Client demo checklist</h2>
        <ul className="list-disc ml-6 space-y-2 text-gray-700">
          <li>Submit one sample enquiry and verify row creation.</li>
          <li>Show immediate confirmation message template.</li>
          <li>Preview follow-up schedule and status update fields.</li>
        </ul>
      </div>

      <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 text-amber-900">
        <strong>Transparency note:</strong> API keys and live business numbers are not stored in this repo. Production integration is done with client-owned accounts during implementation.
      </div>
    </div>
  );
}
