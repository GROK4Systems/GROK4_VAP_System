import uuid
from datetime import datetime

def issue_attestation(output_text):
    return {
        "attestation_id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "verified_output": output_text
    }
