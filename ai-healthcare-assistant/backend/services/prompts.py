SYSTEM_GUARDRAILS = """
You are a clinical documentation assistant.
- Do not provide real medical advice.
- Never claim a diagnosis.
- Prescription output must be marked 'Simulation Only'.
- Remove biased assumptions based on gender, ethnicity, language, or socioeconomic status.
- If information is missing, explicitly state it.
""".strip()

SOAP_PROMPT_TEMPLATE = """
Generate a SOAP note from this doctor-patient transcript.
Return concise markdown with sections: Subjective, Objective, Assessment, Plan.
Transcript:
{transcript}
""".strip()

PRESCRIPTION_SIM_PROMPT_TEMPLATE = """
Generate a simulated prescription draft based on the transcript below.
Strictly include this header: 'Simulation Only - Not Medical Advice'.
Transcript:
{transcript}
""".strip()

SUMMARY_PROMPT_TEMPLATE = """
Using the patient history context and user query, generate a short clinical summary.
Query: {query}
Context:
{context}
""".strip()

ANOMALY_PROMPT_TEMPLATE = """
Find inconsistencies, missing critical details, or symptom anomalies in the transcript.
Return JSON with fields: anomalies (list of strings), risk_level (low|medium|high).
Transcript:
{transcript}
""".strip()
