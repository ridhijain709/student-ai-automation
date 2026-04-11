import os
import google.generativeai as genai
from typing import Any, Dict

# Configure Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def call_gemini_json(system_prompt: str, user_prompt: str, response_schema: Any) -> str:
    """
    Calls Gemini with a system prompt and forces structured JSON output.
    """
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_prompt
    )
    
    response = model.generate_content(
        user_prompt,
        generation_config=genai.types.GenerationConfig(
            response_mime_type="application/json",
            response_schema=response_schema,
        ),
    )
    
    return response.text
