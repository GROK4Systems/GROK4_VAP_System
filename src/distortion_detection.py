# distortion_detection.py

import numpy as np

def model_confidence(output_text):
    # Placeholder: returns a simulated confidence score
    return np.random.uniform(0.6, 0.99)

def out_of_distribution_check(input_text, model_id):
    # Placeholder: simulate low OOD values (good)
    return np.random.uniform(0.0, 0.3)

def compare_to_truth_signature(output_text):
    # Placeholder: simulated semantic deviation score
    return np.random.uniform(0.0, 0.5)

def run_safety_filters(output_text):
    # Basic check for unsafe content or flagged terms
    unsafe_terms = ["hate", "violence", "fraud", "mislead"]
    if any(term in output_text.lower() for term in unsafe_terms):
        return "FLAGGED"
    return "OK"

def energetic_signature_match(output_text):
    # Simulated alignment score (placeholder)
    return np.random.uniform(0.5, 1.0)

def weighted_sum(*args):
    return np.mean(args)

def detect_distortion(input_text, output_text, model_id):
    conf = model_confidence(output_text)
    ood = out_of_distribution_check(input_text, model_id)
    semantic_delta = compare_to_truth_signature(output_text)
    safety_flag = run_safety_filters(output_text)
    energetic_match = energetic_signature_match(output_text)

    fidelity = weighted_sum(
        conf,
        1 - ood,
        1 - semantic_delta,
        energetic_match,
        safety_flag == "OK"
    )

    return {
        "fidelity_score": round(float(fidelity), 4),
        "semantic_delta": round(float(semantic_delta), 4),
        "safety_flag": safety_flag,
        "energetic_match": round(float(energetic_match), 4)
    }
