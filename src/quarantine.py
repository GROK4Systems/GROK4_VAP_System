def quarantine_event(output_text):
    return {
        "status": "Quarantined",
        "reason": "Low fidelity score. Requires human review.",
        "content": output_text
    }
