from __future__ import annotations


def detect_intent(*, vertical: str, message: str) -> str:
    """
    Lightweight intent detector (rule-based) for demo reliability.
    Returns a stable, human-readable intent string.
    """
    v = (vertical or "").strip().lower()
    m = (message or "").lower()

    def has_any(*terms: str) -> bool:
        return any(t in m for t in terms)

    if v == "clinic":
        if has_any("book", "appointment", "slot", "consult", "consultation"):
            return "clinic_booking"
        if has_any("price", "fees", "cost", "charges"):
            return "clinic_pricing"
        if has_any("acne", "pimple"):
            return "clinic_acne"
        if has_any("hair", "hairfall", "hair fall", "dandruff"):
            return "clinic_hair"
        if has_any("skin", "pigmentation", "rash", "eczema"):
            return "clinic_skin"
        return "clinic_general_enquiry"

    if v == "education":
        if has_any("demo", "trial", "counselling", "counseling", "call", "book"):
            return "education_booking"
        if has_any("fees", "fee", "price", "cost"):
            return "education_fees"
        if has_any("eligibility", "eligible", "criteria", "percent", "%", "cgpa"):
            return "education_eligibility"
        if has_any("mba", "bba", "btech", "mtech", "ai", "data", "course", "program"):
            return "education_course_enquiry"
        return "education_general_enquiry"

    if v == "fmcg":
        if has_any("distributor", "distribution", "dealership", "stockist", "super stockist"):
            return "fmcg_distributor_enquiry"
        if has_any("price", "rate", "mrp", "wholesale", "quote", "quotation"):
            return "fmcg_pricing_quote"
        if has_any("available", "availability", "supply", "delivery", "logistics"):
            return "fmcg_availability_logistics"
        if has_any("product", "sku", "catalog", "flavour", "variant"):
            return "fmcg_product_enquiry"
        return "fmcg_general_enquiry"

    return "general_enquiry"


def qualification_questions(*, vertical: str, intent: str) -> list[str]:
    v = (vertical or "").strip().lower()
    i = (intent or "").strip().lower()

    if v == "clinic":
        if i in {"clinic_acne", "clinic_skin", "clinic_hair"}:
            return [
                "What’s the main concern and since when (days/weeks)?",
                "Have you tried any treatments/medicines already?",
                "Do you prefer online or in-clinic consultation?",
            ]
        return [
            "Do you prefer online or in-clinic consultation?",
            "What day/time works best for you (today/tomorrow)?",
        ]

    if v == "education":
        return [
            "Which course/program are you interested in (e.g., MBA/AI)?",
            "Which intake are you targeting and what’s your background (12th/UG/working)?",
            "Do you prefer online or on-campus? Which city?",
        ]

    if v == "fmcg":
        if i == "fmcg_distributor_enquiry":
            return [
                "Which city/area are you looking to distribute in?",
                "Is this for distribution/wholesale/retail?",
                "What’s your expected monthly volume (approx.)?",
            ]
        return [
            "Which city/area and what quantity do you need?",
            "Is this for retail or wholesale?",
            "Which products/SKUs are you interested in?",
        ]

    return []

