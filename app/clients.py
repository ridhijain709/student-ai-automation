from __future__ import annotations


def _norm(message: str) -> str:
    return (message or "").strip().lower()


def clinic_flow(message: str, client_name: str = "TANUS Clinic") -> tuple[str, str]:
    m = _norm(message)
    if any(k in m for k in ["book", "appointment", "slot", "consult", "consultation"]):
        return (
            f"{client_name}: Perfect—happy to help you book a consultation. "
            "Do you prefer online or in-clinic, and what time works best (today/tomorrow)?",
            "clinic_booking",
        )
    if any(k in m for k in ["price", "fees", "cost", "charges"]):
        return (
            f"{client_name}: Pricing depends on severity and the plan after assessment. "
            "What’s your main concern (acne/hair fall/skin) and since when? "
            "Would you like to book a consultation slot today or tomorrow?",
            "clinic_pricing",
        )
    if any(k in m for k in ["acne", "pimple"]):
        return (
            f"{client_name}: Yes—acne can be treated effectively with a personalized plan. "
            "Since when are you facing it, and is it mild or painful/cystic? "
            "Would you like to book a consultation (online or in-clinic)?",
            "clinic_acne",
        )
    if any(k in m for k in ["hair", "hairfall", "hair fall", "dandruff"]):
        return (
            f"{client_name}: For hair fall, we first check common triggers (stress, nutrition, hormones, scalp). "
            "Since when is the hair fall happening? "
            "Shall I book a consultation slot for you?",
            "clinic_hair",
        )
    if any(k in m for k in ["skin", "pigmentation", "rash", "eczema"]):
        return (
            f"{client_name}: Got it—skin concerns are best handled after a quick assessment. "
            "Can you share what the issue is and since when? "
            "Would you like to book an appointment today or tomorrow?",
            "clinic_skin",
        )
    return (
        f"{client_name}: Hi! Tell me what you need help with—acne, hair fall, skin, or pricing. "
        "Do you prefer an online consultation or in-clinic visit?",
        "clinic_general",
    )


def education_flow(message: str, client_name: str = "NextStep Education") -> tuple[str, str]:
    m = _norm(message)
    if any(k in m for k in ["demo", "trial", "counselling", "counseling", "call", "book"]):
        return (
            f"{client_name}: Absolutely—let’s schedule a short counselling/demo session. "
            "Which course are you considering (MBA/AI/etc.), and what time works better (today/tomorrow)?",
            "education_booking",
        )
    if "mba" in m:
        return (
            f"{client_name}: Our MBA track focuses on practical industry skills + placement support. "
            "Are you a final-year student or working professional—and which intake are you targeting? "
            "Want to book a demo/counselling call?",
            "education_mba",
        )
    if any(k in m for k in ["fees", "fee", "price", "cost"]):
        return (
            f"{client_name}: Fees vary by program and eligibility. "
            "Which course are you looking for and do you prefer online or on-campus (which city)? "
            "Should I book a quick counselling call to share exact fees + options?",
            "education_fees",
        )
    if any(k in m for k in ["eligibility", "eligible", "criteria", "%", "cgpa"]):
        return (
            f"{client_name}: Sure—eligibility depends on the program. "
            "Which course and what’s your background (12th/UG/working) + approximate score/CGPA? "
            "Want a quick counselling slot today or tomorrow?",
            "education_eligibility",
        )
    if any(k in m for k in ["course", "program", "ai", "data", "digital marketing"]):
        return (
            f"{client_name}: We offer MBA, AI/Data, and Digital Marketing programs. "
            "Which one are you considering, and what’s your target intake? "
            "Would you like a demo/counselling call?",
            "education_course_enquiry",
        )
    return (
        f"{client_name}: Hi! Which course are you interested in (MBA/AI/etc.) and are you looking for online or on-campus? "
        "Would you like to book a free counselling call?",
        "education_general",
    )


def fmcg_flow(message: str, client_name: str = "Ajoyal Foods") -> tuple[str, str]:
    m = _norm(message)
    if any(k in m for k in ["distributor", "distribution", "dealership", "stockist", "super stockist"]):
        return (
            f"{client_name}: We’re expanding our distributor network. "
            "Which city/area are you based in, and is this for distribution or wholesale? "
            "Share your phone number + expected monthly volume and I’ll guide you to the next step—okay?",
            "fmcg_distributor_enquiry",
        )
    if any(k in m for k in ["price", "rate", "mrp", "quote", "quotation", "wholesale"]):
        return (
            f"{client_name}: I can share the best price—please tell me your city/area, required quantity, "
            "and whether it’s retail or wholesale. Want me to send a quote today?",
            "fmcg_pricing_quote",
        )
    if any(k in m for k in ["product", "sku", "catalog", "flavour", "variant"]):
        return (
            f"{client_name}: We have multiple products/SKUs. "
            "Which items are you interested in and is this for retail, wholesale, or distribution? "
            "Share your city + quantity and I’ll send options.",
            "fmcg_product_enquiry",
        )
    return (
        f"{client_name}: Hello! Are you looking for distributor onboarding or product/pricing details? "
        "Share your city and requirement, and I’ll guide you.",
        "fmcg_general",
    )

