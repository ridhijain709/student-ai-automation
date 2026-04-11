import { useState } from 'react';

export default function TruthGridPage() {
  const [formData, setFormData] = useState({
    student_name: '', target_role: '', projects_count: 0, internships_count: 0,
    tools_score: 0, communication_score: 0, certifications_count: 0
  });
  const [report, setReport] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch('/truthgrid/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    });
    setReport(await res.json());
  };

  return (
    <div className="p-8 max-w-4xl mx-auto bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold mb-6">TruthGrid V1 Assessment</h1>
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow mb-8 grid grid-cols-2 gap-4">
        <input className="p-2 border rounded" placeholder="Student Name" onChange={e => setFormData({...formData, student_name: e.target.value})} />
        <input className="p-2 border rounded" placeholder="Target Role" onChange={e => setFormData({...formData, target_role: e.target.value})} />
        <input type="number" className="p-2 border rounded" placeholder="Projects Count" onChange={e => setFormData({...formData, projects_count: parseInt(e.target.value)})} />
        <input type="number" className="p-2 border rounded" placeholder="Internships Count" onChange={e => setFormData({...formData, internships_count: parseInt(e.target.value)})} />
        <input type="number" className="p-2 border rounded" placeholder="Tools Score (1-10)" onChange={e => setFormData({...formData, tools_score: parseInt(e.target.value)})} />
        <input type="number" className="p-2 border rounded" placeholder="Comm Score (1-10)" onChange={e => setFormData({...formData, communication_score: parseInt(e.target.value)})} />
        <input type="number" className="p-2 border rounded" placeholder="Certs Count" onChange={e => setFormData({...formData, certifications_count: parseInt(e.target.value)})} />
        <button className="col-span-2 bg-blue-600 text-white p-3 rounded font-bold">Generate Report</button>
      </form>

      {report && (
        <div className="bg-white p-8 rounded-lg shadow border-t-4 border-blue-600">
          <h2 className="text-4xl font-bold mb-4">Score: {report.score}</h2>
          <div className="grid grid-cols-2 gap-8">
            <div><h3 className="font-bold text-lg">Strengths</h3><p>{report.strengths}</p></div>
            <div><h3 className="font-bold text-lg">Weaknesses</h3><p>{report.weaknesses}</p></div>
            <div className="col-span-2"><h3 className="font-bold text-lg">Next 30-Day Plan</h3><p>{report.next_steps}</p></div>
          </div>
        </div>
      )}
    </div>
  );
}
