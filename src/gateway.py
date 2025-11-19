# src/gateway.py

from fastapi import FastAPI, Depends, HTTPException, Header, status
import os


from .distortion_detection import detect_distortion
from .soft_correction import soft_correction
from .quarantine import quarantine_event
from .attestation import issue_attestation
from .remembrance_ledger import log_event
from .propagation import propagate_alignment
from .dashboard import get_recent_events

app = FastAPI(
    title="GROK4 Verification Alignment Protocol (VAP)",
    description="IAM-aligned distortion detection, correction, and remembrance ledger API.",
    version="0.1.0",
)
# --- API key security ---

API_KEY = os.environ.get("VAP_API_KEY")  # set this in Render / your env
API_KEY_HEADER_NAME = "x-api-key"


def verify_api_key(x_api_key: str = Header(default=None, alias=API_KEY_HEADER_NAME)):
    """
    Simple header-based API key check.

    - If VAP_API_KEY is not set, auth is effectively disabled (for local dev).
    - If it is set, requests must include:  x-api-key: <that value>
    """
    if not API_KEY:
        # No key configured -> auth disabled (useful for local testing)
        return

    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )

    return x_api_key

ACCEPT_THRESHOLD = 0.92
SOFT_CORRECT_THRESHOLD = 0.75


@app.post("/vap-evaluate", dependencies=[Depends(verify_api_key)])
def vap_evaluate(...):
    ...

    """
    Main VAP endpoint.
    - Evaluates an AI output for distortion.
    - Either accepts, soft-corrects, or quarantines the output.
    - Logs every event into the Remembrance Ledger.
    - Propagates alignment event for future global scaling.
    """
    result = detect_distortion(input_text, output_text, model_id)

    # Base event object for logging + propagation
    event = {
        "model_id": model_id,
        "input_text": input_text,
        "output_text": output_text,
        "details": result,
    }

    fidelity = result.get("fidelity_score", 0.0)

    if fidelity >= ACCEPT_THRESHOLD:
        status = "accepted"
        attestation = issue_attestation(output_text)

        event["status"] = status
        event["attestation"] = attestation

        # Log and propagate
        log_event(status, input_text, output_text, model_id, result)
        propagate_alignment(event)

        return {
            "status": status,
            "attestation": attestation,
            "details": result,
        }

    elif fidelity >= SOFT_CORRECT_THRESHOLD:
        corrected = soft_correction(output_text)
        status = "corrected"
        attestation = issue_attestation(corrected)

        event["status"] = status
        event["corrected_output"] = corrected
        event["attestation"] = attestation

        # Log and propagate corrected version
        log_event(status, input_text, corrected, model_id, result)
        propagate_alignment(event)

        return {
            "status": status,
            "corrected_output": corrected,
            "attestation": attestation,
            "details": result,
        }

    else:
        status = "quarantined"
        review = quarantine_event(output_text)

        event["status"] = status
        event["review"] = review

        # Log and propagate quarantine event
        log_event(status, input_text, output_text, model_id, result)
        propagate_alignment(event)

        return {
            "status": status,
            "review": review,
            "details": result,
        }


@app.get("/events", dependencies=[Depends(verify_api_key)])
def get_events():
    ...
    
    """
    Remembrance Dashboard endpoint.
    Returns the most recent logged VAP events from the ledger.
    """
    events = get_recent_events(limit)
    return {"events": events}
