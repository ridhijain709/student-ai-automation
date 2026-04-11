# Ridhi Command Center

The **Ridhi Command Center** is an AI-powered personal assistant designed to streamline the workflow of student entrepreneurs. It centralizes communication, automates resume tailoring, and provides actionable employability insights, all powered by Google Gemini.

---

## 🚀 Purpose
To reduce cognitive load for student entrepreneurs by triaging communications, automating job application materials, and tracking progress through a unified dashboard.

---

## 📦 Modules
- **Dashboard**: Central overview of urgent tasks, pending follow-ups, and recent activity.
- **Gmail & Telegram**: AI-powered triage, summarization, and draft replies for incoming messages.
- **LinkedIn Assist**: Manual conversation analysis for connection requests, follow-ups, and referral asks.
- **WhatsApp (Stub)**: Simulation-first architecture for incoming message handling.
- **Resume Automation**: ATS-friendly resume generation based on job descriptions and master profiles.
- **TruthGrid**: Rule-based scoring and AI-generated employability reports.

---

## 🛠 Tech Stack
- **Backend**: Python, FastAPI, SQLAlchemy, SQLite
- **Frontend**: React, Tailwind CSS
- **AI/LLM**: Google Gemini API (`gemini-1.5-flash`)
- **Deployment**: Cloud Run (Infrastructure-ready)

---

## 🏗 Architecture
The application follows a standard client-server architecture:
- **FastAPI Backend**: Handles API requests, database interactions, and AI orchestration.
- **React Frontend**: Provides a responsive, professional UI for interaction.
- **SQLite**: Lightweight database for persistence.

---

## ⚙️ Setup

### Prerequisites
- Python 3.10+
- Node.js 18+

### Backend
1. `cd backend`
2. `pip install -r requirements.txt`
3. Create a `.env` file and add `GEMINI_API_KEY=your_key_here`.
4. Run: `python main.py`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

---

## 💡 Simulated vs. Live Features
| Feature | Status | Note |
| :--- | :--- | :--- |
| **Gemini Integration** | Live | Fully functional via API |
| **Database Persistence** | Live | SQLite |
| **Gmail/Telegram** | Live | Currently via pasted text |
| **WhatsApp** | Simulated | Stubbed for future integration |

---

## 🗺 Roadmap
- [ ] Integrate real Gmail/Telegram APIs.
- [ ] Implement user authentication.
- [ ] Add real-time notifications via WebSockets.
- [ ] Enhance TruthGrid scoring with more data points.

---

## 👤 Author
**Ridhi Jain**
*Student Entrepreneur & Developer*
[ridhijain608@gmail.com](mailto:ridhijain608@gmail.com)
