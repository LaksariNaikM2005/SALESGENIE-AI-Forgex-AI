import google.generativeai as genai
import os

# Ensure Member 1 adds GEMINI_API_KEY to the .env file
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_email(industry: str, company: str) -> str:
    """Drafts a personalized cold email using the Gemini LLM."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Write a professional, 3-sentence B2B cold email to {company} in the {industry} industry."
    response = model.generate_content(prompt)
    return response.text