import { useState, useEffect } from 'react';

export default function ResumePage() {
  const [formData, setFormData] = useState({ target_role: '', company_name: '', jd_text: '', master_profile_text: '' });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const res = await fetch('/resume/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    });
    setResult(await res.json());
    setLoading(false);
  };

  const copyToClipboard = (text) => navigator.clipboard.writeText(text);

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Resume Automation</h1>
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow mb-8 space-y-4">
        <input className="w-full p-2 border rounded" placeholder="Target Role" onChange={e => setFormData({...formData, target_role: e.target.value})} />
        <input className="w-full p-2 border rounded" placeholder="Company Name" onChange={e => setFormData({...formData, company_name: e.target.value})} />
        <textarea className="w-full p-2 border rounded h-32" placeholder="Job Description" onChange={e => setFormData({...formData, jd_text: e.target.value})} />
        <textarea className="w-full p-2 border rounded h-32" placeholder="Master Profile Text" onChange={e => setFormData({...formData, master_profile_text: e.target.value})} />
        <button className="bg-blue-600 text-white px-6 py-2 rounded font-semibold" disabled={loading}>
          {loading ? 'Generating...' : 'Generate Resume'}
        </button>
      </form>

      {result && (
        <div className="bg-white p-6 rounded-lg shadow space-y-4">
          <h2 className="text-2xl font-bold">Generated Content</h2>
          {['generated_summary', 'generated_skills', 'generated_bullets', 'generated_cover_letter'].map(key => (
            <div key={key} className="border-t pt-4">
              <div className="flex justify-between items-center mb-2">
                <h3 className="font-semibold capitalize">{key.replace('_', ' ')}</h3>
                <button onClick={() => copyToClipboard(result[key])} className="text-sm text-blue-600 hover:underline">Copy</button>
              </div>
              <p className="text-gray-700 whitespace-pre-wrap">{result[key]}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
