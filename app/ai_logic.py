from __future__ import annotations


def generate_reply(message: str) -> str:
    message = (message or "").lower()

    if "price" in message:
        return "Consultation starts at ₹499, and we can help you pick the right doctor quickly. Would you like to book an appointment for today or tomorrow?"
    if "appointment" in message or "book" in message:
        return "Absolutely—share your preferred date/time (and online vs in-clinic) and I’ll confirm the best available slot. What works for you?"
    if "treatment" in message:
        return "We offer acne, hair fall, and skin treatments with a clear plan after a quick consultation. Which concern are you looking to treat—and should I book a slot for you today or tomorrow?"
    return "Thanks for reaching out—happy to help. What are you looking for, and would you like to book a quick appointment slot?"

