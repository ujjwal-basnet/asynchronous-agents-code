from schemas import TextModelResponse 
from sqlalchemy.orm import Session
from utils import calculate_usage_report, Message 
from entities import ModelUsage, ModelTrace ##### sql tables
from loguru import logger 


def save_usage_and_trace(
    db: Session,
    response: TextModelResponse,
    prompt: str,
    source_url: str | None = None
):
    """
    Calculate usage observability and save both ModelUsage and ModelTrace
    """

    # --- calculate usage report ---
    msg = Message(prompt=prompt, response=response.content, model=response.model)
    report = calculate_usage_report(msg)

    # --- save usage ---
    usage = ModelUsage(
        request_id=response.request_id,
        ip=str(response.ip) if response.ip else None,
        model=response.model,
        req_tokens=report.req_tokens,
        res_tokens=report.res_tokens,
        total_tokens=report.req_tokens + report.res_tokens,
        cost=report.total_cost,
        created_at=response.created_at
    )
    db.add(usage)
    db.commit()
    db.refresh(usage)
    logger.info(f"Saved usage for request_id={response.request_id}")

    # --- save trace ---
    trace = ModelTrace(
        request_id=response.request_id,
        source_url=source_url,
        prompt=prompt,
        content=response.content,
        created_at=datetime.utcnow()
    )
    db.add(trace)
    db.commit()
    db.refresh(trace)
    logger.info(f"Saved trace for request_id={response.request_id}")

    return usage, trace, report
