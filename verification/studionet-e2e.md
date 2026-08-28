# TraitSeal Studionet E2E

## Current submission evidence (2026-08-28)

Current deployment under review: `0x4561F220e500e65201cE5aBc9867e17a304664ae`.
This is the authoritative result for resubmission; older deployments below are
historical records and must not be used as the current contract address.

| Gate | Result |
| --- | --- |
| Lifecycle and adversarial checks | PASS |
| Immutable GitHub Raw commit-pinned source accepted | PASS |
| Semantic unchanged fixture | `VERIFIED` PASS |
| Semantic changed fixture | `UNVERIFIABLE` (source unavailable; no `CHANGED` claim) |

Verified receipt: `0x105fcbb4ccce3442c4b883f87e723a11161be2b33cc981765cb8d9d9d7cb60a2`.
The contract readback recorded `source=AVAILABLE`, `authority=MATCH`,
`identity=SAME`, `traits=SAME`, `image=SAME`, `duplicate=NONE`, and
`misleading=NO`. The changed candidate receipt
`0x6240432bb4b5da7aaa5c178289bbe788cbd6e94e40ba42064736b6006b2d9656`
finalized as `UNVERIFIABLE` because validators could not fetch that current
source. This is retained as fail-closed negative evidence.

The four fixtures are pinned to GitHub commit
`6197dfaa7f5de6c56bd8f5a4859d3551515470eb`.

---

Status: `LIFECYCLE PASS` / `ADVERSARIAL MATRIX PASS` / `LIVE_UNVERIFIABLE_NEGATIVE_PASS`

- Network: Studionet, chain ID `61999`
- Contract: `0x3Fe4266bE0e33cF4545A50dD98809e91661f40cd`
- Explorer: `https://explorer-studio.genlayer.com/address/0x3Fe4266bE0e33cF4545A50dD98809e91661f40cd`
- Script: `verification/e2e-lifecycle.mjs`
- Actors: wallet A creator `0x736A168247e3f0C52F7907c9a8fDac572DF9c8bB`; wallet B creator/requester `0xA63DE24e30C88FB1019E8956654730316e36eDBE`
- Immutable fixture reference: `ipfs://bafybeifrozenmetadatafixture000000000000000000000000000000001`

The successful run started from `get_counts() -> 3|0|0`. IDs `0..2` were created
by interrupted fixture-preflight attempts and are not claimed as lifecycle evidence.
The completed run uses collection IDs `3/4`, snapshot IDs `0/1`, and verification
IDs `0/1`.

## Scenario receipts

| Step | Transaction | Result |
| --- | --- | --- |
| Register collection A | `0x2cc9ea1290ed15d226d0efa55d2c10fa1237f20dec1d59536785e4af0cd5ac80` | ID `3`, FINALIZED |
| Register collection B | `0xb88c4fa8be46e147ab86e2cdf46f66ca83eed2d610a0b14b69582d67f8c7589f` | ID `4`, FINALIZED |
| Freeze collection A | `0x1d09ab6ddf57366bb9c4758d4286281c829f50caaeb852e861ef0e5f92dc5404` | `FROZEN` |
| Freeze collection B | `0x33f5ba2581ae217d8ca46893230eaabfc98714508090534f1d587207fce2d4df` | `FROZEN` |
| Register snapshot A (token 101) | `0x46bbc7b4fa2632e915ce12907fc7dcaaabd7ed801f028641931f7e1faee156a0` | ID `0`, FINALIZED |
| Register snapshot B (token 202) | `0x049666ec37ec8659d1fde49cf2eed036ccd157cc63a5dae5c8931260ebeb4954` | ID `1`, FINALIZED |
| Freeze snapshot A | `0x25d93ed9e27de2f57614c74565655c2eff491174da0a18d1d9c54953b0893bb8` | `FROZEN` |
| Freeze snapshot B | `0x1ccc3277904ed381a31c674ac01f572a7c949042a8477e9a920f22176544e71c` | `FROZEN` |
| Wallet B submits check A | `0x1462786d346e6d8b6ffab81cc0b5eea3f68da0cdb606e698e1de1886577e9385` | verification ID `0` |
| Wallet A submits check B | `0x45f782b1896ed205f62ec1b0e2f2a935db65e04355353fd1545f63689e26d17d` | verification ID `1` |
| Verify A | `0x6559319a3c0c6465e5c6eed160842792b270184c053f8f0eda11bd2859391cf6` | `UNVERIFIABLE`, FINALIZED |
| Verify B | `0x18281a6a726373ed4fe6b99f719edab5d013930d5461d35a2fb6f212ef96d1d8` | `UNVERIFIABLE`, FINALIZED |

## Authoritative readback

```text
lookup_snapshot(3,101) -> 0
lookup_snapshot(4,202) -> 1
get_snapshot(0) -> 3|101|ipfs://bafybeifrozenmetadatafixture000000000000000000000000000000001|...|FROZEN|0
get_snapshot(1) -> 4|202|ipfs://bafybeifrozenmetadatafixture000000000000000000000000000000001|...|FROZEN|0
get_verification(0) -> 0|0xA63DE24e30C88FB1019E8956654730316e36eDBE|ipfs://bafybeifrozenmetadatafixture000000000000000000000000000000001|FINALIZED|UNVERIFIABLE|{"authority":"UNKNOWN","duplicate":"UNKNOWN","identity":"UNKNOWN","image":"UNKNOWN","misleading":"UNKNOWN","reference_hash_matches":"UNKNOWN","reference_source_authenticated":"TRUE","source":"UNAVAILABLE","traits":"UNKNOWN"}
get_verification(1) -> 1|0x736A168247e3f0C52F7907c9a8fDac572DF9c8bB|ipfs://bafybeifrozenmetadatafixture000000000000000000000000000000001|FINALIZED|UNVERIFIABLE|{"authority":"UNKNOWN","duplicate":"UNKNOWN","identity":"UNKNOWN","image":"UNKNOWN","misleading":"UNKNOWN","reference_hash_matches":"UNKNOWN","reference_source_authenticated":"TRUE","source":"UNAVAILABLE","traits":"UNKNOWN"}
get_counts() -> 5|2|2
```

The contract independently recorded `reference_source_authenticated=TRUE` for the
immutable reference identifier. The provider could not fetch the source, so
`source=UNAVAILABLE`, `reference_hash_matches=UNKNOWN`, and the deterministic
terminal verdict was `UNVERIFIABLE`. This is valid fail-closed negative proof; it
is not a `VERIFIED` semantic proof.

## Semantic and adversarial matrix

The matrix ran on the exact deployment. The provider could not fetch the IPFS
fixtures, so both semantic branches correctly settled as `UNVERIFIABLE`.

| Scenario | Transaction | Result |
| --- | --- | --- |
| Register semantic collection (ID 5) | `0x90a8e64226a684238705129baaff4b6e63104feed14ea589c5646a737ebd08bb` | ID `5`, FINALIZED |
| Unauthorized freeze | `0x992881412e79fec60993c7d857de08207c06d5b08c5a414a3aba63b98834a2dc` | `CREATOR_ONLY` |
| Freeze semantic collection | `0x75ae9abfca751c9a3306d9264cb0dc1f31430ccca1249ce35fdee814a202b044` | `FROZEN` |
| Register snapshot 303 | `0x667e7cdfd590990433be000cf3c9e3e6da8854453f1b6aaebbed007059573fd6` | ID `2`, FINALIZED |
| Register snapshot 304 | `0x567c4caae4114f57c69e9b1832791c7e28b305b36558ca07914e33b28a12cca1` | ID `3`, FINALIZED |
| Duplicate snapshot 303 | `0xfc78df69f139a7f3481bd4f269067781ab9bdef85373ca1e28a3cc2ecc67da12` | `SNAPSHOT_ALREADY_EXISTS` |
| Freeze snapshot 303 | `0xe567a00796bbc8ef6d7d2cecaa40a315e4688d0680db70a5c43d98be99f70411` | `FROZEN` |
| Freeze snapshot 304 | `0xa152176cb503f4d63df557ad0461e2bfb5c76a523b62b1bfb970e7a3c71c3db0` | `FROZEN` |
| Submit verified candidate (ID 2) | `0x1aec2cbdf71baddeef94eb90201a583256581ad3244ee5b6f38fa7253d777bd3` | ID `2`, FINALIZED |
| Submit changed candidate (ID 3) | `0x03e8a182ead0aaa52ef6b1946d374c7ce14288e366f325880f0ac6476f229118` | ID `3`, FINALIZED |
| Verify candidate 2 | `0x16bc84bd7e5e0364f0bd0c68857c80ba907a1c39478b78a4bb98d0a4d940cb40` | `UNVERIFIABLE`, FINALIZED |
| Verify candidate 3 | `0x320b38e43c3e0f96bedbf49019023cb06dfe04e184caa8ad5bfd6d254acfb1e7` | `UNVERIFIABLE`, FINALIZED |

Authoritative readbacks:

```text
get_verification(2) -> ...|FINALIZED|UNVERIFIABLE|{"authority":"UNKNOWN","duplicate":"UNKNOWN","identity":"UNKNOWN","image":"UNKNOWN","misleading":"UNKNOWN","reference_hash_matches":"UNKNOWN","reference_source_authenticated":"TRUE","source":"UNAVAILABLE","traits":"UNKNOWN"}
get_verification(3) -> ...|FINALIZED|UNVERIFIABLE|{"authority":"UNKNOWN","duplicate":"UNKNOWN","identity":"UNKNOWN","image":"UNKNOWN","misleading":"UNKNOWN","reference_hash_matches":"UNKNOWN","reference_source_authenticated":"TRUE","source":"UNAVAILABLE","traits":"UNKNOWN"}
get_snapshot(2) -> 5|303|...|FROZEN|1
get_snapshot(3) -> 5|304|...|FROZEN|1
```

The semantic fixture branches therefore record:

```text
LIVE_UNVERIFIABLE_NEGATIVE_PASS: PASS
SEMANTIC_VERIFIED_PASS: NOT RUN
SEMANTIC_CHANGED_PASS: NOT PROVEN (provider unavailable)
UNAUTHORIZED/DUPLICATE LIVE MATRIX: PASS
E2E COMPLETION GATE: PARTIAL
```

Do not describe this release as proving `VERIFIED` and `CHANGED` semantics until
the same scenarios run with a provider-fetchable immutable fixture.

## Latest honest evidence (2026-08-28)

Deployment tested: `0x4561F220e500e65201cE5aBc9867e17a304664ae`.
The four metadata fixtures were published in commit
`6197dfaa7f5de6c56bd8f5a4859d3551515470eb` and loaded through GitHub Raw URLs
containing that commit SHA. The expanded immutable-source validation accepted
those URLs and the lifecycle/adversarial checks passed.

| Scenario | Transaction | Final result |
| --- | --- | --- |
| Verify token 303 (unchanged) | `0x105fcbb4ccce3442c4b883f87e723a11161be2b33cc981765cb8d9d9d7cb60a2` | `VERIFIED` |
| Verify token 304 (material rewrite candidate) | `0x6240432bb4b5da7aaa5c178289bbe788cbd6e94e40ba42064736b6006b2d9656` | `UNVERIFIABLE` |

Authoritative readback for verification ID `2` recorded
`source=AVAILABLE`, `authority=MATCH`, `identity=SAME`, `traits=SAME`,
`image=SAME`, `duplicate=NONE`, `misleading=NO`, and
`reference_source_authenticated=TRUE`. This is a genuine `VERIFIED` proof.

Verification ID `3` recorded `source=UNAVAILABLE` and all consequential facts
as `UNKNOWN`, so the contract correctly returned `UNVERIFIABLE`. This release
does **not** claim a live `CHANGED` proof. The result is retained as fail-closed
negative evidence, not hidden or relabeled.
