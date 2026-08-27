# TraitSeal Studionet E2E

Status: `LIFECYCLE PASS` / `LIVE PINATA NEGATIVE PROOF PASS` / `SEMANTIC RESULT UNVERIFIABLE (EXPECTED)`

- Network: Studionet, chain ID `61999`
- Contract: `0x7cd0582D385e7225d101012FD6e258a828528266`
- Script: `verification/e2e-lifecycle.mjs`
- Actors: wallet A creator `0x736A168247e3f0C52F7907c9a8fDac572DF9c8bB`; wallet B creator/requester `0xA63DE24e30C88FB1019E8956654730316e36eDBE`
- Source used for the fixture: `https://raw.githubusercontent.com/dearmore5382/DAOProposalContextVerifier/main/README.md`

## Scenario receipts

| Step | Transaction | Result |
| --- | --- | --- |
| Register collection A | `0x6ce0f5240745bf367c4e7597fa3e2064d01a3654656c1aae1954c6d27a2e7e67` | ID `0`, FINALIZED |
| Register collection B | `0x5c6f1fe6109a8092008ceeb7d0afe5e092a8c5a68619a8be1419647cb3236a49` | ID `1`, FINALIZED |
| Freeze collection A | `0x1b9d29460f611b4c75c3360789d3e8a58c81649cc23c25aadf446fd4804bb91d` | `FROZEN` |
| Freeze collection B | `0x7c4fa2be941152151257f4f363c04e4bf4e3df56d204d558ad391aa5ee93a088` | `FROZEN` |
| Register snapshot A (token 101) | `0xdf4367bc92c4c60128f6f8173dd998ff7ccbf79bf42a1b135e53e523c6a7ba5a` | ID `0`, FINALIZED |
| Register snapshot B (token 202) | `0x6a50754fc9bff92663b29b4ade2c35b0eea8f052df41d140a56f62740e461dab` | ID `1`, FINALIZED |
| Freeze snapshot A | `0xdbcf8edb739b1915957a7351566868058b0c7ba11d7e61af7fd46adff83b35f0` | `FROZEN` |
| Freeze snapshot B | `0xea3199b0824d3de193a5d702b40f14421865bff00ed71ea403050f00f03b4271` | `FROZEN` |
| Wallet B submits check A | `0xcc48d99acecad0d82ceaf77f05967cd257049225dfed514d1821315b84476c8f` | verification ID `0` |
| Wallet A submits check B | `0x680dabb560e8cfcee39ac5f44aed9d710c1f2850f4c2bcfef73a236ae49f341a` | verification ID `1` |
| Verify A | `0xc3f05643136f2109b8d9123e42bf5f27011c952d7d52bfcc7fa0f78d405a583b` | `UNVERIFIABLE` |
| Verify B | `0x9cbdce85cb7057a6b1c5c8a4c53732841daa6902c0d1016f201600560dad1aa7` | `UNVERIFIABLE` |

## Authoritative readback

```text
lookup_snapshot(0,101) -> 0
lookup_snapshot(1,202) -> 1
get_verification(0) -> 0|0xA63DE24e30C88FB1019E8956654730316e36eDBE|...|FINALIZED|UNVERIFIABLE|{"authority":"UNKNOWN","duplicate":"UNKNOWN","identity":"UNKNOWN","image":"UNKNOWN","misleading":"UNKNOWN","source":"UNAVAILABLE","traits":"UNKNOWN"}
get_verification(1) -> 1|0x736A168247e3f0C52F7907c9a8fDac572DF9c8bB|...|FINALIZED|UNVERIFIABLE|{"authority":"UNKNOWN","duplicate":"UNKNOWN","identity":"UNKNOWN","image":"UNKNOWN","misleading":"UNKNOWN","source":"UNAVAILABLE","traits":"UNKNOWN"}
get_counts() -> 2|2|2
```

`UNVERIFIABLE` is the intended terminal result for this fixture: the contract
correctly preserves an unavailable source as an explicit bounded outcome rather than
guessing `VERIFIED` or treating a finalized transaction as semantic success. The
registration, freeze, authorization-by-creator, direct lookup, submission and
consensus lifecycle all passed.

This Pinata result is retained as evidence that the contract fails closed. It must be
reported as `source=UNAVAILABLE -> verdict=UNVERIFIABLE`, not relabeled as a provider
or parser success.
