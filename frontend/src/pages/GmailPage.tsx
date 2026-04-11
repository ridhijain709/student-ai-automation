import { useState, useEffect } from 'react';

export default function GmailPage() {
  const [text, setText] = useState('');
  const [sender, setSender] = useState('');
  const [subject, setSubject] = useState('');
  const [messages, setMessages] = useState([]);
  const [result, setResult] = useState(null);

  useEffect(() => {
    fetch('/gmail/messages').then(res => res.json()).then(setMessages);
  }, []);

  const handleAnalyze = async () => {
    const res = await fetch('/gmail/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sender, subject, raw_text: text })
    });
    setResult(await res.json());
    fetch('/gmail/messages').then(res => res.json()).then(setMessages);
  };

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Gmail Assistant</h1>
      <div className="bg-white p-6 rounded-lg shadow mb-8 space-y-4">
        <input className="w-full p-2 border rounded" placeholder="Sender" onChange={e => setSender(e.target.value)} />
        <input className="w-full p-2 border rounded" placeholder="Subject" onChange={e => setSubject(e.target.value)} />
        <textarea className="w-full p-2 border rounded h-32" placeholder="Paste email content here..." onChange={e => setText(e.target.value)} />
        <button onClick={handleAnalyze} className="bg-blue-600 text-white px-6 py-2 rounded font-semibold">Analyze</button>
      </div>

      {result && (
        <div className="grid grid-cols-2 gap-4 mb-8">
          <div className="bg-white p-4 rounded shadow"><strong>Category:</strong> {result.category}</div>
          <div className="bg-white p-4 rounded shadow"><strong>Urgency:</strong> {result.urgency}</div>
          <div className="col-span-2 bg-white p-4 rounded shadow"><strong>Summary:</strong> {result.summary}</div>
          <div className="col-span-2 bg-white p-4 rounded shadow"><strong>Action:</strong> {result.recommended_action}</div>
          <div className="col-span-2 bg-white p-4 rounded shadow"><strong>Draft:</strong> {result.draft_reply}</div>
        </div>
      )}

      <h2 className="text-2xl font-bold mb-4">Recent Messages</h2>
      <div className="space-y-4">
        {messages.map(m => (
          <div key={m.id} className="bg-white p-4 rounded shadow border-l-4 border-blue-500">
            <h3 className="font-bold">{m.subject}</h3>
            <p className="text-sm text-gray-600 mb-4">{m.sender}</p>
            <div className="flex space-x-2">
              <button className="text-xs bg-gray-100 px-2 py-1 rounded">Mark as Read</button>
              <button className="text-xs bg-gray-100 px-2 py-1 rounded">Archive</button>
              <button className="text-xs bg-blue-100 px-2 py-1 rounded text-blue-700">Reply</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
