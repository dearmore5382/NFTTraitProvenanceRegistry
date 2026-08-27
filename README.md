# TraitSeal Registry

TraitSeal is a provenance laboratory for NFT metadata. A creator registers a
collection authority and immutable token snapshot; a buyer or marketplace submits
the current metadata URL; GenLayer validators compare both sources and the contract
records a tamper-evident verdict.

## Why GenLayer

NFT metadata can be JSON, HTML, IPFS content, or a JavaScript-rendered page. A normal
contract cannot read and interpret those sources. GenLayer validators fetch and
normalize the content, then consensus binds the bounded facts to on-chain state.

## Build locally

```powershell
npm install
Copy-Item .env.example .env.local
# set VITE_CONTRACT_ADDRESS after a user-approved deployment
npm run dev
```

The app runs on localhost and uses `genlayer-js` with the `studionet` chain. It
requires a funded MetaMask account for writes and switches to chain `61999` before
signing. No deployment or production hosting is automated by this repository.

## Contract checks

```powershell
python -c "import ast; ast.parse(open('contracts/NFTTraitProvenanceRegistry.py', encoding='utf-8').read())"
python -m pytest -q
```

The contract has three immutable layers: collection authority, token snapshot, and
verification receipt. Every write validates IDs, role, lifecycle state and input
before mutation. Snapshot lookup uses a direct composite index rather than scanning
historical records.

## Verification evidence

The submission evidence will record source parity, schema, deployment transaction,
all lifecycle receipts, consensus payloads, execution results, and post-write
readbacks. The verdict is derived from these bounded facts:

- `VERIFIED`: all consequential facts match.
- `CHANGED`: a material trait/identity/image/authority issue is detected.
- `UNVERIFIABLE`: a source is unavailable or evidence is ambiguous.

### Live Pinata negative proof

The live Studionet Pinata run is intentionally recorded as a valid negative
scenario, not hidden as a test failure. Pinata accepted the uploaded CID and the
local gateway returned HTTP 200, but the GenLayer validator web provider could not
fetch that gateway. The finalized contract facts were therefore:

```text
source = UNAVAILABLE
verdict = UNVERIFIABLE
```

This is an important safety proof: when an external source cannot be read, TraitSeal
fails closed and does not guess `VERIFIED`. The complete receipts and readbacks are
in [`verification/studionet-e2e.md`](verification/studionet-e2e.md).

## Limits

TraitSeal proves consistency against a creator-configured snapshot and authority. It
does not prove NFT ownership, copyright, creator identity, or legal authenticity.
Duplicate detection is a validator signal and not a global uniqueness guarantee.
