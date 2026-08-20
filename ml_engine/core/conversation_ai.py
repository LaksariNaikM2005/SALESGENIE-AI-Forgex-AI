import google.generativeai as genai

def analyze_transcript(transcript: str) -> dict:
    """Extracts sentiment and a brief summary from meeting notes."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Analyze this sales transcript. Provide a 1-sentence summary and state the sentiment (Positive/Neutral/Negative). Transcript: {transcript}"
    response = model.generate_content(prompt)
    return {"analysis": response.text}