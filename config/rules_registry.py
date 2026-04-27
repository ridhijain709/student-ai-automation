from __future__ import annotations

from dataclasses import dataclass

from config import clinic_rules, education_rules, fmcg_rules


@dataclass(frozen=True)
class VerticalRules:
    key: str
    name: str
    whatsapp_triage_prompt: str
    cta_hints: list[str]


VERTICALS: dict[str, VerticalRules] = {
    clinic_rules.VERTICAL_KEY: VerticalRules(
        key=clinic_rules.VERTICAL_KEY,
        name=clinic_rules.VERTICAL_NAME,
        whatsapp_triage_prompt=clinic_rules.WHATSAPP_TRIAGE_PROMPT,
        cta_hints=clinic_rules.CTA_HINTS,
    ),
    education_rules.VERTICAL_KEY: VerticalRules(
        key=education_rules.VERTICAL_KEY,
        name=education_rules.VERTICAL_NAME,
        whatsapp_triage_prompt=education_rules.WHATSAPP_TRIAGE_PROMPT,
        cta_hints=education_rules.CTA_HINTS,
    ),
    fmcg_rules.VERTICAL_KEY: VerticalRules(
        key=fmcg_rules.VERTICAL_KEY,
        name=fmcg_rules.VERTICAL_NAME,
        whatsapp_triage_prompt=fmcg_rules.WHATSAPP_TRIAGE_PROMPT,
        cta_hints=fmcg_rules.CTA_HINTS,
    ),
}


def get_vertical(key: str | None) -> VerticalRules:
    if not key:
        return VERTICALS["clinic"]
    return VERTICALS.get(key.strip().lower(), VERTICALS["clinic"])

