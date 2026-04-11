import { useState, useEffect } from 'react';

export default function TelegramPage() {
  const [msg, setMsg] = useState({ sender: '', raw_text: '' });
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    fetch('/telegram/messages').then(res => res.json()).then(setMessages);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    await fetch('/telegram/incoming', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(msg)
    });
    window.location.reload();
  };

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">Telegram Assistant</h1>
      <form onSubmit={handleSubmit} className="mb-8 p-4 bg-white rounded shadow">
        <input className="block w-full mb-2 p-2 border" placeholder="Sender" onChange={e => setMsg({...msg, sender: e.target.value})} />
        <textarea className="block w-full mb-2 p-2 border" placeholder="Message" onChange={e => setMsg({...msg, raw_text: e.target.value})} />
        <button className="bg-blue-600 text-white px-4 py-2 rounded">Process Message</button>
      </form>
      <div className="space-y-4">
        {messages.map(m => (
          <div key={m.id} className="p-4 bg-white rounded shadow border">
            <p className="text-sm">{m.raw_text}</p>
            <p className="text-xs text-gray-500 mt-2">{m.summary}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
