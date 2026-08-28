# TraitSeal Studionet Evidence

## Submission status

- Network: GenLayer Studionet, chain ID `61999`
- Current contract: `0x4561F220e500e65201cE5aBc9867e17a304664ae`
- Explorer: <https://explorer-studio.genlayer.com/address/0x4561F220e500e65201cE5aBc9867e17a304664ae>
- Fixture commit: `6197dfaa7f5de6c56bd8f5a4859d3551515470eb`
- Scripts: `verification/e2e-lifecycle.mjs` and `verification/semantic-matrix.mjs`

This file contains evidence only for the current deployment above. It makes no
claim that a live `CHANGED` verdict has been proven.

## Honest completion gate

| Gate | Result |
| --- | --- |
| Contract source and deployment parity | PASS |
| Collection lifecycle | PASS |
| Creator-only freeze guard | PASS |
| Immutable snapshot registration | PASS |
| Duplicate snapshot rejection | PASS |
| GitHub commit-pinned source authentication | PASS |
| Live semantic `VERIFIED` | PASS |
| Live semantic `CHANGED` | NOT PROVEN |
| Unavailable-source fail-closed behavior | PASS |
| Overall semantic matrix | PARTIAL |

## Current lifecycle receipts

| Step | Transaction | Result |
| --- | --- | --- |
| Register semantic collection | `0xaa831d9d592c7a597b1acab4afc1eed0183261cb6a8e8f9b3f80c8c55b88e83f` | ID `1`, FINALIZED |
| Unauthorized freeze | `0x8209313567f7ea2eb2e5fa6f9be46dc6720fa23017c063614357b614610e3963` | `CREATOR_ONLY` |
| Freeze collection | `0xb809bc777464a3138a5b400e8d37ca56a684ca2ee6a642962117de3e100b6e7b` | `FROZEN` |
| Register unchanged snapshot | `0xde6f5618a863bedf0c0b7ef42d70f9f4983e70a6906dda2562940b99fe5fcdc4` | ID `2`, FINALIZED |
| Register changed snapshot | `0x7b4d700f96f102474a25ab244f27d766becdbf4d8f1861941265f1b951b7623e` | ID `3`, FINALIZED |
| Reject duplicate snapshot | `0x8faaa6719ddc310d171eb35b6c3509075083a579862c0c820dcf33878f80f530` | `SNAPSHOT_ALREADY_EXISTS` |
| Freeze unchanged snapshot | `0xf095d9e3e19ca7869305a1702ecc75fa0e1e32f50b54f725937dc6ac072bf1ef` | `FROZEN` |
| Freeze changed snapshot | `0xf2b2ea6e75ead113c401dc7d9ba8613dc3158b389a1faa030f46c39512287901` | `FROZEN` |
| Submit unchanged verification | `0xc57dc45d13b446a53a4b5d537effc713e67eebd0d33ff3f2d099391576eecbf2` | ID `2`, FINALIZED |
| Submit changed verification | `0xcc8e404d315cf004e70f38deeb9159f0712d6710ec8eae6066e418b6eec9adc8` | ID `3`, FINALIZED |

## Semantic receipt: VERIFIED

- Transaction: `0x105fcbb4ccce3442c4b883f87e723a11161be2b33cc981765cb8d9d9d7cb60a2`
- Verification ID: `2`
- Final verdict: `VERIFIED`

Authoritative readback:

```json
{
  "authority": "MATCH",
  "duplicate": "NONE",
  "identity": "SAME",
  "image": "SAME",
  "misleading": "NO",
  "reference_hash_matches": "UNKNOWN",
  "reference_source_authenticated": "TRUE",
  "source": "AVAILABLE",
  "traits": "SAME"
}
```

The reference hash is an optional diagnostic. The immutable GitHub URL is pinned
to the fixture commit, and all consequential semantic facts agreed.

## Semantic receipt: unavailable changed candidate

- Transaction: `0x6240432bb4b5da7aaa5c178289bbe788cbd6e94e40ba42064736b6006b2d9656`
- Verification ID: `3`
- Final verdict: `UNVERIFIABLE`

Readback recorded `source=UNAVAILABLE`; all consequential facts were `UNKNOWN`.
The contract therefore failed closed instead of guessing `CHANGED`. This is valid
negative safety evidence but is not presented as a successful `CHANGED` proof.

## Immutable fixtures

The reference and current JSON files are stored in `verification/fixtures/` and
addressed through GitHub Raw URLs containing the full fixture commit SHA. A branch
name such as `main` is not accepted as an immutable source by the contract.
