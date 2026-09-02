import os

def generate_outreach_message(
    lead_name: str,
    company_name: str,
    industry: str,
    message_type: str = "cold_email",
    tone: str = "Consultative",
    value_prop: str = "PLC & SCADA Integration",
    tech_stack: str = "Siemens PLC, ROS2",
) -> dict:
    """
    Generates personalized manufacturing cold emails, follow-up messages, phone scripts, or LinkedIn pitches.
    Supports ordered parameters: Lead Target, Channel, Tone/Perspective, Value Proposition Focus.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key and not api_key.startswith("your-") and not api_key.startswith("mock-"):
        try:
            import openai
            client = openai.OpenAI(api_key=api_key)
            prompt = (
                f"Write a personalized {message_type} with a {tone} tone to {lead_name} at {company_name} in {industry}. "
                f"Highlight {value_prop} and mention their tech stack ({tech_stack}). Drive ROI for manufacturing automation."
            )
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are an expert industrial sales director crafting copy in a {tone} tone."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
            )
            body_text = response.choices[0].message.content
            subject_text = f"[{tone}] {value_prop} for {company_name}"
            return {"subject": subject_text, "body": body_text, "tone": tone, "message_type": message_type}
        except Exception as e:
            print(f"OpenAI Outreach generation failed: {e}")

    # High-converting manufacturing outreach templates with ordered parameter filters
    m_type = message_type.lower().replace(" ", "_")

    if "phone" in m_type or "script" in m_type:
        subject = f"Phone Call Script — {company_name} ({lead_name})"
        body = (
            f"📞 CALL SCRIPT FOR {lead_name.upper()} AT {company_name.upper()}:\n\n"
            f"1. OPENING: 'Hi {lead_name}, this is SalesGenie AI calling regarding {company_name}'s plant operations in {industry}. Have I caught you at a good time?'\n"
            f"2. VALUE HOOK ({value_prop}): 'We've been helping manufacturing plants optimize {value_prop} using advanced ML lead scoring and {tech_stack} integration.'\n"
            f"3. PERSPECTIVE ({tone}): 'Given your Q4 expansion goals, our platform automates qualification so your engineering team focuses only on high-margin deals.'\n"
            f"4. CALL TO ACTION: 'Would you be open to a 10-minute technical demonstration this Thursday at 2 PM?'"
        )
    elif "linkedin" in m_type:
        subject = f"LinkedIn Connection Pitch — {lead_name}"
        body = (
            f"Hi {lead_name},\n\n"
            f"Noticed your manufacturing leadership at {company_name}. We've been working with {industry} operations executives to streamline {value_prop}.\n\n"
            f"With your stack ({tech_stack}), our ML intelligence platform delivers predictive lead scoring and automated CRM integration.\n\n"
            f"Would love to connect and share our Q3 manufacturing ROI benchmark paper!\n\n"
            f"Best regards,\nSalesGenie AI Engineering Team"
        )
    elif "proposal" in m_type or "cover" in m_type:
        subject = f"Executive Cover Letter: {value_prop} Strategy for {company_name}"
        body = (
            f"Dear {lead_name},\n\n"
            f"Re: Executive SLA Proposal & Commercial Strategy for {company_name}\n\n"
            f"We are pleased to submit our formal proposal focused on {value_prop} for {company_name}'s {industry} manufacturing facilities.\n\n"
            f"Key Objectives Addressed:\n"
            f"• Integration with existing architecture: {tech_stack}\n"
            f"• Primary Focus Area: {value_prop}\n"
            f"• Commercial Incentive: Volume tier pricing with guaranteed implementation SLA\n\n"
            f"We look forward to scheduling our executive review with your operations leadership team.\n\n"
            f"Sincerely,\nSalesGenie AI Platform Team"
        )
    else: # Executive Email (default)
        subject = f"[{tone}] {value_prop} Optimization for {company_name}"
        body = (
            f"Dear {lead_name},\n\n"
            f"I am reaching out regarding {company_name}'s manufacturing operations in the {industry} sector.\n\n"
            f"Our AI Sales Intelligence platform was specifically designed for B2B industrial enterprises. Based on our real-world dataset analysis, {industry} companies deploying {value_prop} achieve a 35% higher pipeline conversion rate.\n\n"
            f"How we align with your environment ({tech_stack}):\n"
            f"1. Real ML Lead Scoring tailored to manufacturing metrics\n"
            f"2. Direct SCADA / CRM synchronization\n"
            f"3. Automated next-best-action recommendations\n\n"
            f"Are you open to a brief 15-minute technical briefing this week to review the implementation roadmap?\n\n"
            f"Best regards,\nSalesGenie AI Team"
        )

    return {"subject": subject, "body": body, "tone": tone, "message_type": message_type, "value_prop": value_prop}
