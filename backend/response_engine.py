from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


try:
    import google.generativeai as genai
except Exception:  # pragma: no cover
    genai = None


DEMO_ROOT = Path(__file__).resolve().parents[1] / "demos"


@dataclass
class EngineResult:
    reply: str
    escalate: bool
    source: str  # faq | gemini | fallback
    matched_faq: bool
    response_time_ms: float


class ResponseEngine:
    def __init__(self, vertical: str):
        self.vertical = vertical
        self.system_prompt = self._load_system_prompt()
        self.faq_bank = self._load_faq_bank()

    def _vertical_dir(self) -> Path:
        # vertical comes from route param; map to demo folder names
        mapping = {
            "fmcg": "01-fmcg-distributor-automation",
            "clinic": "02-clinic-patient-automation",
            "edtech": "03-edtech-admission-automation",
            "agency": "04-agency-whitelabel-system",
            "bschool": "05-bschool-admission-automation",
            # Allow full folder names too:
            "01-fmcg-distributor-automation": "01-fmcg-distributor-automation",
            "02-clinic-patient-automation": "02-clinic-patient-automation",
            "03-edtech-admission-automation": "03-edtech-admission-automation",
            "04-agency-whitelabel-system": "04-agency-whitelabel-system",
            "05-bschool-admission-automation": "05-bschool-admission-automation",
        }
        folder = mapping.get(self.vertical, self.vertical)
        return DEMO_ROOT / folder

    def _load_system_prompt(self) -> str:
        p = self._vertical_dir() / "prompts" / "system_prompt.txt"
        if not p.exists():
            return "You are a helpful business assistant. Answer briefly and end with a CTA."
        return p.read_text(encoding="utf-8")

    def _load_faq_bank(self) -> list[dict[str, Any]]:
        p = self._vertical_dir() / "prompts" / "faq_bank.json"
        if not p.exists():
            return []
        data = json.loads(p.read_text(encoding="utf-8"))
        return data.get("faqs", [])

    def check_faq(self, message: str) -> dict | None:
        msg = (message or "").strip().lower()
        if not msg or not self.faq_bank:
            return None

        best = None
        best_score = 0.0
        for f in self.faq_bank:
            q = (f.get("q") or "").strip().lower()
            if not q:
                continue
            score = SequenceMatcher(None, msg, q).ratio()
            if score > best_score:
                best_score = score
                best = f

        if best and best_score >= 0.75:
            return {"faq": best, "score": best_score}
        return None

    def generate_response(self, message: str, sender_name: str) -> EngineResult:
        start = time.time()

        faq_match = self.check_faq(message)
        if faq_match:
            answer = faq_match["faq"]["a"]
            reply = self._append_cta(answer, sender_name=sender_name)
            ms = (time.time() - start) * 1000
            return EngineResult(reply=reply, escalate=False, source="faq", matched_faq=True, response_time_ms=ms)

        # Gemini fallback (if configured)
        reply = None
        if genai and os.getenv("GEMINI_API_KEY"):
            try:
                genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
                model = genai.GenerativeModel("gemini-1.5-flash")
                prompt = self._build_gemini_prompt(message=message, sender_name=sender_name)
                out = model.generate_content(prompt)
                reply = getattr(out, "text", None) or str(out)
            except Exception:
                reply = None

        if not reply:
            reply = self._append_cta(
                "Thanks—got it. Main aapko details share kar deta/deti hoon. Aap apna preferred time/number share kar sakte/sakti hain?",
                sender_name=sender_name,
            )
            ms = (time.time() - start) * 1000
            return EngineResult(
                reply=reply,
                escalate=self._should_escalate(message=message, response=reply),
                source="fallback",
                matched_faq=False,
                response_time_ms=ms,
            )

        reply = self._append_cta(reply, sender_name=sender_name)
        ms = (time.time() - start) * 1000
        return EngineResult(
            reply=reply,
            escalate=self._should_escalate(message=message, response=reply),
            source="gemini",
            matched_faq=False,
            response_time_ms=ms,
        )

    def _build_gemini_prompt(self, message: str, sender_name: str) -> str:
        return (
            f"{self.system_prompt.strip()}\n\n"
            f"Sender name: {sender_name}\n"
            f"User message: {message}\n\n"
            "Reply as the business assistant. Keep it concise and end with one clear next step (CTA)."
        )

    def _append_cta(self, text: str, *, sender_name: str) -> str:
        t = (text or "").strip()
        if not t:
            t = "Thanks for reaching out."
        if not t.endswith("?"):
            t = t.rstrip(".") + "."
        # Gentle universal CTA (vertical prompts already specify links/CTAs)
        if "link" in t.lower():
            return t
        return f"{t}\n\nWould you like me to share the booking/onboarding link?"

    def _should_escalate(self, message: str, response: str) -> bool:
        m = (message or "").lower()
        r = (response or "").lower()
        red_flags = [
            "complaint",
            "refund",
            "legal",
            "fraud",
            "allergic",
            "reaction",
            "severe pain",
            "bleeding",
            "emergency",
            "5 lakh",
            "₹5 lakh",
        ]
        return any(x in m for x in red_flags) or "not sure" in r or "can't" in r

