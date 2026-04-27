from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ContentSpec:
    platform: str
    max_length_hint: str
    tone: str
    format_hint: str


_SPECS: dict[str, ContentSpec] = {
    "instagram": ContentSpec(
        platform="instagram",
        max_length_hint="Short, punchy, scroll-stopping (1–6 lines).",
        tone="friendly, energetic, simple words",
        format_hint="Add a few relevant emojis only if it fits naturally. Keep it readable.",
    ),
    "linkedin": ContentSpec(
        platform="linkedin",
        max_length_hint="Medium length (8–14 lines). Clear spacing. Professional but human.",
        tone="credible, practical, confident (no hype)",
        format_hint="Use short paragraphs + 3–5 bullets. Avoid excessive emojis.",
    ),
    "whatsapp": ContentSpec(
        platform="whatsapp",
        max_length_hint="Very short (4–8 lines). Broadcast-friendly.",
        tone="warm, direct, conversational",
        format_hint="Keep it skimmable. One clear CTA question at the end.",
    ),
    "whatsapp_broadcast": ContentSpec(
        platform="whatsapp_broadcast",
        max_length_hint="Very short (4–8 lines). Broadcast-friendly.",
        tone="warm, direct, conversational",
        format_hint="Keep it skimmable. One clear CTA question at the end.",
    ),
}


def _normalize_platform(platform: str) -> str:
    p = (platform or "").strip().lower()
    if p in {"ig", "insta"}:
        return "instagram"
    if p in {"linkedin", "li"}:
        return "linkedin"
    if p in {"wa", "whatsapp", "broadcast", "whatsapp_broadcast"}:
        return "whatsapp_broadcast" if "broadcast" in p or p == "broadcast" else "whatsapp"
    return p


def generate_content(topic: str, platform: str) -> str:
    """
    Demo-ready content generation using simple AI-style templates:
    Hook -> Value -> CTA
    """
    topic_clean = " ".join((topic or "").split()).strip()
    if not topic_clean:
        topic_clean = "your business"

    p = _normalize_platform(platform)
    if p not in _SPECS:
        supported = ", ".join(sorted(set(_SPECS.keys())))
        raise ValueError(f"Unsupported platform '{platform}'. Supported: {supported}")

    spec = _SPECS[p]

    # Hook ideas per platform
    hook = {
        "instagram": f"Most {topic_clean} enquiries don’t fail… they get *missed*.",
        "linkedin": f"If you’re exploring {topic_clean}, here’s the practical part most teams miss:",
        "whatsapp": f"Quick update on {topic_clean}:",
        "whatsapp_broadcast": f"Quick update on {topic_clean}:",
    }[spec.platform]

    # Value section (kept generic but business-forward)
    value_lines = {
        "instagram": [
            "Reply faster.",
            "Capture every lead automatically.",
            "Turn chats into bookings—without extra staff.",
        ],
        "linkedin": [
            "What it changes in the real world:",
            "- Faster first response (seconds, not hours)",
            "- Consistent answers + clear next step",
            "- Lead capture with timestamp so follow-ups don’t slip",
            "",
            "This is especially useful when enquiries spike after office hours.",
        ],
        "whatsapp": [
            "It helps you reply instantly, capture leads, and move people to the next step.",
            "Perfect for busy hours + weekends.",
        ],
        "whatsapp_broadcast": [
            "It helps you reply instantly, capture leads, and move people to the next step.",
            "Perfect for busy hours + weekends.",
        ],
    }[spec.platform]

    # CTA: always a question (conversion)
    cta = {
        "instagram": "Want a quick demo for your business? Reply with “DEMO” and I’ll send it.",
        "linkedin": "If you want, I can show a 5‑minute demo tailored to your business—should I share it?",
        "whatsapp": "Want me to show a 5‑minute demo for your business? What’s a good time today or tomorrow?",
        "whatsapp_broadcast": "Want me to show a 5‑minute demo for your business? What’s a good time today or tomorrow?",
    }[spec.platform]

    # Compose with a simple consistent structure
    lines: list[str] = []
    lines.append(hook)
    lines.append("")
    lines.extend(value_lines)
    lines.append("")
    lines.append(cta)
    lines.append("")
    lines.append(f"(Format: Hook → Value → CTA | Tone: {spec.tone} | Length: {spec.max_length_hint})")

    return "\n".join(lines).strip()

