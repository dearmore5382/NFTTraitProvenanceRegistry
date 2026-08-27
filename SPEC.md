# TraitSeal Registry specification

TraitSeal is an Intelligent Contract registry for immutable NFT metadata provenance.
Creators commit collection authority and token snapshots before inspection. A later
inspection fetches the locked reference and submitted current source through GenLayer
consensus, reduces the result to bounded facts, and derives `VERIFIED`, `CHANGED`, or
`UNVERIFIABLE` deterministically on-chain.

## Trust model

The registry proves consistency with the creator’s locked snapshot and configured
authority. It does not prove ownership, copyright, authenticity of the creator, or
that an image is free of infringement. `duplicate` is a validator signal, not a
collection-wide uniqueness proof.

## Consequential verdict rule

Unavailable/ambiguous source or any unknown fact is `UNVERIFIABLE`. A mismatched
authority/identity, material trait change, replaced image, suspected duplicate, or
misleading field is `CHANGED`. Only matching, available, non-ambiguous facts produce
`VERIFIED`. 

The live Pinata scenario is retained as an explicit negative proof. Although the CID
was successfully uploaded and readable from the developer machine, the Studionet
validator provider returned no fetchable source. The expected on-chain result is
`source=UNAVAILABLE` and `verdict=UNVERIFIABLE`; this demonstrates fail-closed
behavior rather than a semantic verification failure.

## Frontend boundary

The Vite frontend is an integration artifact. It reads counts and submits real
transactions through `genlayer-js` against the configured deployment. It never
simulates validator output or stores a private key in a Vite environment variable.
