from rag.vector_store import vector_store
from services.llm_service import llm_service
from services.prompts import SUMMARY_PROMPT_TEMPLATE
from utils.config import settings


async def summarize_history(patient_id: str, query: str) -> tuple[str, list[str]]:
    context_chunks = vector_store.query(patient_id, query, top_k=settings.vector_top_k)
    context = "\n".join(context_chunks) if context_chunks else "No prior history found."
    summary = await llm_service.generate_text(
        SUMMARY_PROMPT_TEMPLATE.format(query=query, context=context)
    )
    return summary, context_chunks
