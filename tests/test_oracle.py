from oracle import derive


BASE = {
    "source": "AVAILABLE",
    "authority": "MATCH",
    "identity": "SAME",
    "traits": "SAME",
    "image": "SAME",
    "duplicate": "NONE",
    "misleading": "NO",
}


def changed(**updates):
    facts = dict(BASE)
    facts.update(updates)
    return facts


def test_verified_exact():
    assert derive(BASE) == "VERIFIED"


def test_non_material_trait_normalization_is_verified():
    assert derive(changed(traits="NON_MATERIAL")) == "VERIFIED"


def test_each_consequential_field_changes_verdict():
    assert derive(changed(authority="MISMATCH")) == "CHANGED"
    assert derive(changed(identity="DIFFERENT")) == "CHANGED"
    assert derive(changed(traits="MATERIAL")) == "CHANGED"
    assert derive(changed(image="REPLACED")) == "CHANGED"
    assert derive(changed(duplicate="SUSPECTED")) == "CHANGED"
    assert derive(changed(misleading="YES")) == "CHANGED"


def test_unavailable_and_unknown_are_unverifiable():
    assert derive(changed(source="UNAVAILABLE")) == "UNVERIFIABLE"
    for key in ("authority", "identity", "traits", "image", "duplicate", "misleading"):
        assert derive(changed(**{key: "UNKNOWN"})) == "UNVERIFIABLE"


def test_invalid_output_is_rejected():
    assert derive(changed(image="SIMILAR")) == "INVALID_CONSENSUS_OUTPUT"
    incomplete = dict(BASE)
    incomplete.pop("traits")
    assert derive(incomplete) == "INVALID_CONSENSUS_OUTPUT"

