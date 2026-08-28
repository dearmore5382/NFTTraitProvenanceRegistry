ALLOWED = {
    "source": {"AVAILABLE", "UNAVAILABLE"},
    "authority": {"MATCH", "MISMATCH", "UNKNOWN"},
    "identity": {"SAME", "DIFFERENT", "UNKNOWN"},
    "traits": {"SAME", "NON_MATERIAL", "MATERIAL", "UNKNOWN"},
    "image": {"SAME", "REPLACED", "UNKNOWN"},
    "duplicate": {"NONE", "SUSPECTED", "UNKNOWN"},
    "misleading": {"NO", "YES", "UNKNOWN"},
    "reference_source_authenticated": {"TRUE", "FALSE"},
}


def derive(facts):
    if set(facts) != set(ALLOWED):
        return "INVALID_CONSENSUS_OUTPUT"
    if any(facts[key] not in values for key, values in ALLOWED.items()):
        return "INVALID_CONSENSUS_OUTPUT"
    if facts["source"] == "UNAVAILABLE" or facts["reference_source_authenticated"] != "TRUE" or "UNKNOWN" in facts.values():
        return "UNVERIFIABLE"
    if (
        facts["authority"] == "MISMATCH"
        or facts["identity"] == "DIFFERENT"
        or facts["traits"] == "MATERIAL"
        or facts["image"] == "REPLACED"
        or facts["duplicate"] == "SUSPECTED"
        or facts["misleading"] == "YES"
    ):
        return "CHANGED"
    return "VERIFIED"
