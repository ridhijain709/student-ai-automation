from __future__ import annotations


def generate_reply(message: str) -> str:
    message = (message or "").lower()

    if "price" in message:
        return "Our consultation starts at ₹499. Would you like to book an appointment?"
    if "appointment" in message or "book" in message:
        return "Please share your preferred date and time. We'll confirm your booking shortly."
    if "treatment" in message:
        return "We offer acne, hair fall, and skin treatments. Which one are you interested in?"
    return "Thanks for reaching out! How can we help you today?"

