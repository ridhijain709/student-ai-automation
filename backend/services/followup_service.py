from __future__ import annotations

from config.client_profiles import ClientProfile


def should_trigger_followups(*, intent: str, message: str) -> bool:
    """
    Conservative trigger: only when user shows buying intent.
    """
    i = (intent or "").lower()
    m = (message or "").lower()

    interest_terms = ["book", "appointment", "slot", "call", "demo", "price", "fees", "cost", "quote", "quotation"]
    if any(t in m for t in interest_terms):
        return True

    # Some intents are inherently commercial
    return any(k in i for k in ["pricing", "booking", "quote", "distributor"])


def build_followups(*, profile: ClientProfile, intent: str) -> tuple[str, str]:
    """
    Two-step follow-up sequence. Step 1 is immediate; Step 2 is a gentle nudge.
    """
    business = profile.business_name
    link = profile.cta_link

    if profile.industry == "clinic":
        f1 = (
            f"Happy to help from {business}. Would you like me to book your consultation slot? "
            f"You can also pick a time here: {link}"
        )
        f2 = (
            f"Just checking in—do you want to go ahead with the consultation booking? "
            f"If yes, share a preferred time (today/tomorrow) or use: {link}"
        )
        return f1, f2

    if profile.industry == "education":
        f1 = (
            f"Quick one from {business}: would you like to schedule a short counselling/demo class slot? "
            f"Here’s the booking link: {link}"
        )
        f2 = (
            f"Just checking—should I book your counselling/demo slot, or do you have any questions before we schedule? "
            f"Link: {link}"
        )
        return f1, f2

    if profile.industry == "fmcg":
        f1 = (
            f"From {business}—want me to share the best quote/onboarding steps? "
            f"Submit details here and we’ll respond fast: {link}"
        )
        f2 = (
            f"Just checking—are you still interested in pricing/distribution? "
            f"If yes, share your city + quantity or use: {link}"
        )
        return f1, f2

    f1 = f"Would you like to proceed? Here’s a quick link: {link}"
    f2 = f"Just checking in—still interested? Link: {link}"
    return f1, f2

