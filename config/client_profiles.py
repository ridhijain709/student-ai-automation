from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ClientProfile:
    """
    Lightweight multi-client personalization.
    `industry` maps to vertical rules: clinic | education | fmcg
    """

    key: str
    industry: str  # clinic | education | fmcg
    business_name: str
    tone: str  # premium | friendly | professional
    pricing_line: str
    cta_link: str  # calendly/google form/whatsapp click-to-chat etc.


CLIENTS: dict[str, ClientProfile] = {
    # Demo keys required by spec (?client=clinic|education|fmcg)
    "clinic": ClientProfile(
        key="clinic",
        industry="clinic",
        business_name="TANUS Clinic",
        tone="professional",
        pricing_line="Consultation starts at ₹499 (final depends on assessment).",
        cta_link="https://calendly.com/demo/clinic-consultation",
    ),
    "education": ClientProfile(
        key="education",
        industry="education",
        business_name="NextStep Education",
        tone="friendly",
        pricing_line="Counselling call is free. Fees vary by program and eligibility.",
        cta_link="https://calendly.com/demo/education-counselling",
    ),
    "fmcg": ClientProfile(
        key="fmcg",
        industry="fmcg",
        business_name="Ajoyal Foods",
        tone="premium",
        pricing_line="We share distributor/retail pricing based on city, channel, and quantity.",
        cta_link="https://forms.gle/demo/fmcg-distributor-onboarding",
    ),
}


def get_client_profile(
    key: str | None,
    *,
    business_name: str | None = None,
    tone: str | None = None,
    pricing_line: str | None = None,
    cta_link: str | None = None,
) -> ClientProfile:
    k = (key or "clinic").strip().lower()
    base = CLIENTS.get(k, CLIENTS["clinic"])

    # Allow runtime overrides (useful for demos without redeploying)
    return ClientProfile(
        key=base.key,
        industry=base.industry,
        business_name=(business_name or base.business_name).strip(),
        tone=(tone or base.tone).strip().lower(),
        pricing_line=(pricing_line or base.pricing_line).strip(),
        cta_link=(cta_link or base.cta_link).strip(),
    )

