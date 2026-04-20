from services.bias_filter_service import sanitize_bias
from services.llm_service import llm_service
from services.prompts import PRESCRIPTION_SIM_PROMPT_TEMPLATE, SOAP_PROMPT_TEMPLATE


async def generate_soap_and_prescription(transcript: str) -> tuple[str, str]:
    cleaned = sanitize_bias(transcript)
    soap_note = await llm_service.generate_text(SOAP_PROMPT_TEMPLATE.format(transcript=cleaned))
    prescription = await llm_service.generate_text(
        PRESCRIPTION_SIM_PROMPT_TEMPLATE.format(transcript=cleaned)
    )

    if "Simulation Only" not in prescription:
        prescription = f"Simulation Only - Not Medical Advice\n\n{prescription}"

    return soap_note, prescription
