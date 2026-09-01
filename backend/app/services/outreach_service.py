import os

def generate_outreach_message(lead_name: str, company_name: str, industry: str, message_type: str = "cold_email") -> dict:
    """
    Generates personalized cold emails, follow-up messages, or LinkedIn pitches.
    Uses OpenAI LLM API if key is present, otherwise returns personalized AI templates.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key and not api_key.startswith("your-") and not api_key.startswith("mock-"):
        try:
            import openai
            client = openai.OpenAI(api_key=api_key)
            prompt = f"Write a personalized {message_type} to {lead_name} at {company_name} in the {industry} industry. Focus on driving ROI and introducing SalesGenie AI automation."
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert enterprise sales representative and B2B email copywriter."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
            )
            body_text = response.choices[0].message.content
            subject_text = f"Accelerating Sales Intelligence at {company_name}"
            return {"subject": subject_text, "body": body_text}
        except Exception as e:
            print(f"OpenAI Outreach generation failed: {e}")

    # Template fallback
    if message_type == "follow_up":
        subject = f"Following up: AI Sales Insights for {company_name}"
        body = f"Hi {lead_name},\n\nI wanted to follow up on our previous conversation regarding SalesGenie AI. Companies in the {industry} space are using our platform to boost pipeline conversion by up to 35%.\n\nWould you have 15 minutes this Thursday for a quick demo?\n\nBest regards,\nSalesGenie Team"
    elif message_type == "linkedin_pitch":
        subject = f"Connecting with {lead_name}"
        body = f"Hi {lead_name}, noticed your leadership in {company_name}'s growth. We've built an AI assistant designed to automate prospect qualification and lead scoring for {industry} teams. Would love to connect and share a quick preview!"
    else:
        subject = f"Unlocking AI-Driven Sales Intelligence for {company_name}"
        body = f"Hi {lead_name},\n\nI noticed {company_name}'s recent momentum in the {industry} sector. SalesGenie AI helps B2B sales teams instantly qualify prospects, generate high-converting outreach, and automate CRM synchronization.\n\nAre you open to exploring how we can streamline your sales pipeline this quarter?\n\nBest regards,\nSalesGenie Team"

    return {"subject": subject, "body": body}
