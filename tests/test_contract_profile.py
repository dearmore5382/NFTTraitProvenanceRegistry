import ast
from pathlib import Path


SOURCE_PATH = Path(__file__).parents[1] / "contracts" / "NFTTraitProvenanceRegistry.py"
SOURCE = SOURCE_PATH.read_text(encoding="utf-8")


def test_contract_parses_and_has_required_header():
    ast.parse(SOURCE)
    lines = SOURCE.splitlines()
    assert lines[0] == "# v0.2.16"
    assert lines[1] == '# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }'
    assert lines[2] == "from genlayer import *"


def test_nondeterminism_is_consensus_wrapped():
    assert "gl.eq_principle.strict_eq(inspect)" in SOURCE
    assert SOURCE.count("gl.nondet.web.get") == 2
    assert SOURCE.count("gl.nondet.exec_prompt") == 1


def test_direct_snapshot_index_avoids_historical_scan():
    assert "snapshot_lookup.get" in SOURCE
    register = SOURCE.split("def register_snapshot", 1)[1].split("@gl.public.write", 1)[0]
    assert "for " not in register
    assert "while " not in register


def test_security_and_immutability_guards_exist():
    for code in (
        "CREATOR_ONLY",
        "COLLECTION_NOT_FROZEN",
        "SNAPSHOT_ALREADY_EXISTS",
        "SNAPSHOT_NOT_FROZEN",
        "ALREADY_VERIFIED",
        "INVALID_COLLECTION_ADDRESS",
    ):
        assert code in SOURCE


def test_bounded_facts_drive_deterministic_verdict():
    for field in ("source", "authority", "identity", "traits", "image", "duplicate", "misleading"):
        assert f'facts["{field}"]' in SOURCE
    assert 'verdict = "VERIFIED"' in SOURCE
    assert 'verdict = "CHANGED"' in SOURCE
    assert 'verdict = "UNVERIFIABLE"' in SOURCE

