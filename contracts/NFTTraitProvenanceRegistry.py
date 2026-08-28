# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
import typing
import json


class NFTTraitProvenanceRegistry(gl.Contract):
    collection_count: u256
    snapshot_count: u256
    verification_count: u256

    collection_names: TreeMap[u256, str]
    collection_creators: TreeMap[u256, str]
    collection_chains: TreeMap[u256, str]
    collection_contracts: TreeMap[u256, str]
    collection_authorities: TreeMap[u256, str]
    collection_manifest_urls: TreeMap[u256, str]
    collection_manifest_hashes: TreeMap[u256, str]
    collection_statuses: TreeMap[u256, str]
    collection_snapshot_counts: TreeMap[u256, u256]

    snapshot_collection_ids: TreeMap[u256, u256]
    snapshot_token_ids: TreeMap[u256, u256]
    snapshot_metadata_urls: TreeMap[u256, str]
    snapshot_metadata_hashes: TreeMap[u256, str]
    snapshot_image_refs: TreeMap[u256, str]
    snapshot_trait_manifests: TreeMap[u256, str]
    snapshot_statuses: TreeMap[u256, str]
    snapshot_verification_counts: TreeMap[u256, u256]
    snapshot_lookup: TreeMap[u256, u256]

    verification_snapshot_ids: TreeMap[u256, u256]
    verification_requesters: TreeMap[u256, str]
    verification_current_urls: TreeMap[u256, str]
    verification_statuses: TreeMap[u256, str]
    verification_verdicts: TreeMap[u256, str]
    verification_facts: TreeMap[u256, str]

    def __init__(self):
        self.collection_count = u256(0)
        self.snapshot_count = u256(0)
        self.verification_count = u256(0)

    def _address_text(self, value: str) -> str:
        text = str(value)
        if text.startswith("addr#"):
            return "0x" + text[5:]
        return text

    def _sender(self) -> str:
        return self._address_text(gl.message.sender_address)

    def _valid_address(self, value: str) -> str:
        text = self._address_text(value)
        if len(text) != 42 or not text.startswith("0x"):
            return "INVALID_ADDRESS"
        allowed = "0123456789abcdefABCDEF"
        for char in text[2:]:
            if char not in allowed:
                return "INVALID_ADDRESS"
        return "OK"

    def _valid_text(self, value: str, maximum: u256) -> str:
        text = str(value).strip()
        if len(text) == 0 or u256(len(text)) > maximum:
            return "INVALID_TEXT"
        return "OK"

    def _valid_url(self, value: str) -> str:
        text = str(value).strip()
        if len(text) < 10 or len(text) > 500:
            return "INVALID_URL"
        if not text.startswith("https://") and not text.startswith("ipfs://") and not text.startswith("ar://"):
            return "INVALID_URL"
        return "OK"

    def _authenticated_metadata_url(self, value: str) -> str:
        text = str(value).strip()
        if text.startswith("ipfs://") or text.startswith("ar://"):
            return "OK"
        return "AUTHENTICATED_SOURCE_REQUIRED"

    def _valid_hash(self, value: str) -> str:
        text = str(value).strip()
        if len(text) < 32 or len(text) > 160 or " " in text:
            return "INVALID_HASH"
        return "OK"

    def _token_key(self, collection_id: u256, token_id: u256) -> u256:
        return collection_id * u256(1000000000000) + token_id

    @gl.public.write
    def register_collection(self, name: str, chain: str, contract_address: str, authority: str, manifest_url: str, manifest_hash: str) -> typing.Any:
        if self._valid_text(name, u256(120)) != "OK":
            return "INVALID_NAME"
        if self._valid_text(chain, u256(40)) != "OK":
            return "INVALID_CHAIN"
        if self._valid_address(contract_address) != "OK":
            return "INVALID_COLLECTION_ADDRESS"
        if self._valid_url(authority) != "OK":
            return "INVALID_AUTHORITY"
        if self._valid_url(manifest_url) != "OK":
            return "INVALID_MANIFEST_URL"
        if self._valid_hash(manifest_hash) != "OK":
            return "INVALID_MANIFEST_HASH"

        collection_id = self.collection_count
        self.collection_names[collection_id] = name.strip()
        self.collection_creators[collection_id] = self._sender()
        self.collection_chains[collection_id] = chain.strip()
        self.collection_contracts[collection_id] = self._address_text(contract_address)
        self.collection_authorities[collection_id] = authority.strip()
        self.collection_manifest_urls[collection_id] = manifest_url.strip()
        self.collection_manifest_hashes[collection_id] = manifest_hash.strip()
        self.collection_statuses[collection_id] = "DRAFT"
        self.collection_snapshot_counts[collection_id] = u256(0)
        self.collection_count = collection_id + u256(1)
        return collection_id

    @gl.public.write
    def freeze_collection(self, collection_id: u256) -> typing.Any:
        if collection_id >= self.collection_count:
            return "COLLECTION_NOT_FOUND"
        if self.collection_creators[collection_id] != self._sender():
            return "CREATOR_ONLY"
        if self.collection_statuses[collection_id] != "DRAFT":
            return "COLLECTION_ALREADY_FROZEN"
        self.collection_statuses[collection_id] = "FROZEN"
        return "FROZEN"

    @gl.public.write
    def register_snapshot(self, collection_id: u256, token_id: u256, metadata_url: str, metadata_hash: str, image_ref: str, trait_manifest: str) -> typing.Any:
        if collection_id >= self.collection_count:
            return "COLLECTION_NOT_FOUND"
        if self.collection_creators[collection_id] != self._sender():
            return "CREATOR_ONLY"
        if self.collection_statuses[collection_id] != "FROZEN":
            return "COLLECTION_NOT_FROZEN"
        if token_id >= u256(1000000000000):
            return "TOKEN_ID_TOO_LARGE"
        if self._valid_url(metadata_url) != "OK":
            return "INVALID_METADATA_URL"
        if self._authenticated_metadata_url(metadata_url) != "OK":
            return "AUTHENTICATED_SOURCE_REQUIRED"
        if self._valid_hash(metadata_hash) != "OK":
            return "INVALID_METADATA_HASH"
        if self._valid_text(image_ref, u256(500)) != "OK":
            return "INVALID_IMAGE_REF"
        if self._valid_text(trait_manifest, u256(4000)) != "OK":
            return "INVALID_TRAIT_MANIFEST"

        lookup_key = self._token_key(collection_id, token_id)
        if self.snapshot_lookup.get(lookup_key, u256(0)) != u256(0):
            return "SNAPSHOT_ALREADY_EXISTS"

        snapshot_id = self.snapshot_count
        self.snapshot_collection_ids[snapshot_id] = collection_id
        self.snapshot_token_ids[snapshot_id] = token_id
        self.snapshot_metadata_urls[snapshot_id] = metadata_url.strip()
        self.snapshot_metadata_hashes[snapshot_id] = metadata_hash.strip()
        self.snapshot_image_refs[snapshot_id] = image_ref.strip()
        self.snapshot_trait_manifests[snapshot_id] = trait_manifest.strip()
        self.snapshot_statuses[snapshot_id] = "REGISTERED"
        self.snapshot_verification_counts[snapshot_id] = u256(0)
        self.snapshot_lookup[lookup_key] = snapshot_id + u256(1)
        self.collection_snapshot_counts[collection_id] = self.collection_snapshot_counts[collection_id] + u256(1)
        self.snapshot_count = snapshot_id + u256(1)
        return snapshot_id

    @gl.public.write
    def freeze_snapshot(self, snapshot_id: u256) -> typing.Any:
        if snapshot_id >= self.snapshot_count:
            return "SNAPSHOT_NOT_FOUND"
        collection_id = self.snapshot_collection_ids[snapshot_id]
        if self.collection_creators[collection_id] != self._sender():
            return "CREATOR_ONLY"
        if self.snapshot_statuses[snapshot_id] != "REGISTERED":
            return "SNAPSHOT_ALREADY_FROZEN"
        self.snapshot_statuses[snapshot_id] = "FROZEN"
        return "FROZEN"

    @gl.public.write
    def submit_verification(self, snapshot_id: u256, current_url: str) -> typing.Any:
        if snapshot_id >= self.snapshot_count:
            return "SNAPSHOT_NOT_FOUND"
        if self.snapshot_statuses[snapshot_id] != "FROZEN":
            return "SNAPSHOT_NOT_FROZEN"
        if self._valid_url(current_url) != "OK":
            return "INVALID_CURRENT_URL"

        verification_id = self.verification_count
        self.verification_snapshot_ids[verification_id] = snapshot_id
        self.verification_requesters[verification_id] = self._sender()
        self.verification_current_urls[verification_id] = current_url.strip()
        self.verification_statuses[verification_id] = "SUBMITTED"
        self.verification_verdicts[verification_id] = "UNVERIFIED"
        self.verification_facts[verification_id] = ""
        self.snapshot_verification_counts[snapshot_id] = self.snapshot_verification_counts[snapshot_id] + u256(1)
        self.verification_count = verification_id + u256(1)
        return verification_id

    @gl.public.write
    def verify_metadata(self, verification_id: u256) -> typing.Any:
        if verification_id >= self.verification_count:
            return "VERIFICATION_NOT_FOUND"
        if self.verification_statuses[verification_id] != "SUBMITTED":
            return "ALREADY_VERIFIED"

        snapshot_id = self.verification_snapshot_ids[verification_id]
        collection_id = self.snapshot_collection_ids[snapshot_id]
        reference_url = self.snapshot_metadata_urls[snapshot_id]
        current_url = self.verification_current_urls[verification_id]
        collection_name = self.collection_names[collection_id]
        collection_address = self.collection_contracts[collection_id]
        authority = self.collection_authorities[collection_id]
        token_id = self.snapshot_token_ids[snapshot_id]
        locked_hash = self.snapshot_metadata_hashes[snapshot_id]
        image_ref = self.snapshot_image_refs[snapshot_id]
        trait_manifest = self.snapshot_trait_manifests[snapshot_id]

        def inspect() -> str:
            reference_content = "[UNAVAILABLE]"
            current_content = "[UNAVAILABLE]"
            try:
                reference_content = gl.nondet.web.get(reference_url).body.decode("utf-8")[:5000]
            except Exception:
                reference_content = "[UNAVAILABLE]"
            try:
                current_content = gl.nondet.web.get(current_url).body.decode("utf-8")[:5000]
            except Exception:
                current_content = "[UNAVAILABLE]"

            prompt = (
                "Act as an NFT metadata provenance inspector. Compare the immutable reference and current metadata. "
                "Return ONLY JSON with exactly these string fields: source, reference_hash_matches, authority, identity, traits, image, duplicate, misleading. "
                "Allowed values: source=AVAILABLE|UNAVAILABLE; reference_hash_matches=TRUE|FALSE|UNKNOWN; authority=MATCH|MISMATCH|UNKNOWN; "
                "identity=SAME|DIFFERENT|UNKNOWN; traits=SAME|NON_MATERIAL|MATERIAL|UNKNOWN; "
                "image=SAME|REPLACED|UNKNOWN; duplicate=NONE|SUSPECTED|UNKNOWN; misleading=NO|YES|UNKNOWN. "
                "Formatting, JSON key order, trait order, gateway URL, and case-only changes are NON_MATERIAL. "
                "A removed or altered value-bearing trait is MATERIAL. An image is REPLACED only when its content identity differs, "
                "not merely because the gateway URL differs. Independently canonicalize the fetched reference JSON and verify its digest against the locked hash; do not infer this from prompt text. Mark UNKNOWN when evidence cannot support a fact. "
                "Collection=" + collection_name + "; contract=" + collection_address + "; authority=" + authority
                + "; token_id=" + str(token_id) + "; locked_hash=" + locked_hash + "; locked_image=" + image_ref
                + "; registered_traits=" + trait_manifest + "; reference=" + reference_content
                + "; current=" + current_content
            )
            raw = gl.nondet.exec_prompt(prompt).strip()
            try:
                data = json.loads(raw)
                bounded = {
                    "authority": str(data["authority"]),
                    "duplicate": str(data["duplicate"]),
                    "identity": str(data["identity"]),
                    "image": str(data["image"]),
                    "misleading": str(data["misleading"]),
                    "reference_hash_matches": str(data["reference_hash_matches"]),
                    "source": str(data["source"]),
                    "traits": str(data["traits"]),
                }
                return json.dumps(bounded, sort_keys=True, separators=(",", ":"))
            except Exception:
                return "{\"authority\":\"UNKNOWN\",\"duplicate\":\"UNKNOWN\",\"identity\":\"UNKNOWN\",\"image\":\"UNKNOWN\",\"misleading\":\"UNKNOWN\",\"reference_hash_matches\":\"UNKNOWN\",\"source\":\"UNAVAILABLE\",\"traits\":\"UNKNOWN\"}"

        facts_json = gl.eq_principle.strict_eq(inspect)
        try:
            facts = json.loads(facts_json)
            source = facts["source"]
            authority_result = facts["authority"]
            identity = facts["identity"]
            traits = facts["traits"]
            image = facts["image"]
            duplicate = facts["duplicate"]
            misleading = facts["misleading"]
            reference_hash_matches = facts["reference_hash_matches"]
        except Exception:
            return "INVALID_CONSENSUS_OUTPUT"

        if source not in ("AVAILABLE", "UNAVAILABLE"):
            return "INVALID_CONSENSUS_OUTPUT"
        if authority_result not in ("MATCH", "MISMATCH", "UNKNOWN"):
            return "INVALID_CONSENSUS_OUTPUT"
        if identity not in ("SAME", "DIFFERENT", "UNKNOWN"):
            return "INVALID_CONSENSUS_OUTPUT"
        if traits not in ("SAME", "NON_MATERIAL", "MATERIAL", "UNKNOWN"):
            return "INVALID_CONSENSUS_OUTPUT"
        if image not in ("SAME", "REPLACED", "UNKNOWN"):
            return "INVALID_CONSENSUS_OUTPUT"
        if duplicate not in ("NONE", "SUSPECTED", "UNKNOWN"):
            return "INVALID_CONSENSUS_OUTPUT"
        if misleading not in ("NO", "YES", "UNKNOWN"):
            return "INVALID_CONSENSUS_OUTPUT"
        if reference_hash_matches not in ("TRUE", "FALSE", "UNKNOWN"):
            return "INVALID_CONSENSUS_OUTPUT"

        verdict = "VERIFIED"
        if source == "UNAVAILABLE" or reference_hash_matches != "TRUE" or authority_result == "UNKNOWN" or identity == "UNKNOWN" or traits == "UNKNOWN" or image == "UNKNOWN" or duplicate == "UNKNOWN" or misleading == "UNKNOWN":
            verdict = "UNVERIFIABLE"
        elif authority_result == "MISMATCH" or identity == "DIFFERENT" or traits == "MATERIAL" or image == "REPLACED" or duplicate == "SUSPECTED" or misleading == "YES":
            verdict = "CHANGED"

        self.verification_facts[verification_id] = facts_json
        self.verification_verdicts[verification_id] = verdict
        self.verification_statuses[verification_id] = "FINALIZED"
        return verdict

    @gl.public.view
    def get_collection(self, collection_id: u256) -> str:
        if collection_id >= self.collection_count:
            return "COLLECTION_NOT_FOUND"
        return self.collection_names[collection_id] + "|" + self.collection_chains[collection_id] + "|" + self.collection_contracts[collection_id] + "|" + self.collection_authorities[collection_id] + "|" + self.collection_statuses[collection_id] + "|" + str(self.collection_snapshot_counts[collection_id])

    @gl.public.view
    def get_snapshot(self, snapshot_id: u256) -> str:
        if snapshot_id >= self.snapshot_count:
            return "SNAPSHOT_NOT_FOUND"
        return str(self.snapshot_collection_ids[snapshot_id]) + "|" + str(self.snapshot_token_ids[snapshot_id]) + "|" + self.snapshot_metadata_urls[snapshot_id] + "|" + self.snapshot_metadata_hashes[snapshot_id] + "|" + self.snapshot_image_refs[snapshot_id] + "|" + self.snapshot_trait_manifests[snapshot_id] + "|" + self.snapshot_statuses[snapshot_id] + "|" + str(self.snapshot_verification_counts[snapshot_id])

    @gl.public.view
    def get_verification(self, verification_id: u256) -> str:
        if verification_id >= self.verification_count:
            return "VERIFICATION_NOT_FOUND"
        return str(self.verification_snapshot_ids[verification_id]) + "|" + self.verification_requesters[verification_id] + "|" + self.verification_current_urls[verification_id] + "|" + self.verification_statuses[verification_id] + "|" + self.verification_verdicts[verification_id] + "|" + self.verification_facts[verification_id]

    @gl.public.view
    def lookup_snapshot(self, collection_id: u256, token_id: u256) -> str:
        if collection_id >= self.collection_count or token_id >= u256(1000000000000):
            return "SNAPSHOT_NOT_FOUND"
        stored = self.snapshot_lookup.get(self._token_key(collection_id, token_id), u256(0))
        if stored == u256(0):
            return "SNAPSHOT_NOT_FOUND"
        return str(stored - u256(1))

    @gl.public.view
    def get_counts(self) -> str:
        return str(self.collection_count) + "|" + str(self.snapshot_count) + "|" + str(self.verification_count)
