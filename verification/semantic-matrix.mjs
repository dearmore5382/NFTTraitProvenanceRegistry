import { createAccount, createClient } from "genlayer-js";
import { studionet } from "genlayer-js/chains";
import { TransactionStatus } from "genlayer-js/types";
import { readFileSync } from "node:fs";

const env = Object.fromEntries(readFileSync(".env.e2e", "utf8").split(/\r?\n/).filter(Boolean).map((line) => { const i = line.indexOf("="); return [line.slice(0, i), line.slice(i + 1)]; }));
const a = createAccount(`0x${env.WALLET_A_PRIVATE_KEY.replace(/^0x/, "")}`);
const b = createAccount(`0x${env.WALLET_B_PRIVATE_KEY.replace(/^0x/, "")}`);
const read = createClient({ chain: studionet, endpoint: env.RPC_URL });
const wa = createClient({ chain: studionet, endpoint: env.RPC_URL, account: a });
const wb = createClient({ chain: studionet, endpoint: env.RPC_URL, account: b });
const address = env.CONTRACT_ADDRESS;
const authority = "https://gateway.pinata.cloud/ipfs/";
const manifest = "https://gateway.pinata.cloud/ipfs/QmTqXy36wxN5rNwtsSpPd1PjhTUMuHCybc7NFGVjZe4jcY";
const verifiedRef = manifest;
const verifiedCurrent = "https://gateway.pinata.cloud/ipfs/QmV5wyRT1UpmgrAB5UFQLcAmHoiT8tCmF6qgdJ5urg8WXV";
const changedRef = "https://gateway.pinata.cloud/ipfs/QmSq8wLCr4pJyFsBJ94d6HP9Ff5WgJA2ae5sFxdY5uF7wY";
const changedCurrent = "https://gateway.pinata.cloud/ipfs/QmatxPYpvdbvrWH2utMh4eobcDXS9XqXJBJhoriSCdVpGb";
const hash = "sha256:7f3b2d2a2d1f8c8f0c3b4f6a8e9d0b1c2a3e4f5b6c7d8e9f0011223344556677";
const nft = "0x3333333333333333333333333333333333333333";

async function view(method, args) { const value = await read.readContract({ address, functionName: method, args, stateStatus: "accepted" }); console.log(`${method}(${args.join(",")}) -> ${value}`); return String(value); }
async function tx(client, label, method, args) { const hashTx = await client.writeContract({ address, functionName: method, args, value: 0n }); console.log(`${label} tx ${hashTx}`); const receipt = await read.waitForTransactionReceipt({ hash: hashTx, status: TransactionStatus.FINALIZED, retries: 120, interval: 3000, fullTransaction: true }); const result = receipt.consensus_data?.leader_receipt?.[0]?.result?.payload?.readable || receipt.result_name || "UNKNOWN"; console.log(`${label} ${receipt.statusName || "FINALIZED"} result=${result}`); return { hash: hashTx, result: String(result) }; }
function idOf(receipt) { const match = receipt.result.match(/\d+/); if (!match) throw new Error(`missing numeric id in ${receipt.result}`); return BigInt(match[0]); }

const [collectionStart] = (await view("get_counts", [])).split("|").map(BigInt);
const collection = collectionStart;
await tx(wa, "semantic-collection", "register_collection", ["TraitSeal Semantic Fixtures", "Ethereum mainnet", nft, authority, manifest, hash]);
const unauthorized = await tx(wb, "unauthorized-freeze", "freeze_collection", [collection]);
if (!unauthorized.result.includes("CREATOR_ONLY")) throw new Error(`expected CREATOR_ONLY, got ${unauthorized.result}`);
await tx(wa, "freeze-semantic-collection", "freeze_collection", [collection]);
const traits303 = JSON.stringify({ background: "Ink", edition: "1/1", palette: "Cobalt" });
const traits304 = JSON.stringify({ rarity: "Legendary", edition: "1/1", palette: "Gold" });
const snapshot303 = await tx(wa, "snapshot-303", "register_snapshot", [collection, 303n, verifiedRef, hash, "ipfs://bafybeiverifiedimagecid000000000000000000000000000000001", traits303]);
const snapshot304 = await tx(wa, "snapshot-304", "register_snapshot", [collection, 304n, changedRef, hash, "ipfs://bafybeioriginalimagecid000000000000000000000000000000001", traits304]);
const duplicate = await tx(wa, "duplicate-snapshot", "register_snapshot", [collection, 303n, verifiedRef, hash, "ipfs://duplicate", traits303]);
if (!duplicate.result.includes("SNAPSHOT_ALREADY_EXISTS")) throw new Error(`expected SNAPSHOT_ALREADY_EXISTS, got ${duplicate.result}`);
const snapshotId303 = idOf(snapshot303);
const snapshotId304 = idOf(snapshot304);
await tx(wa, "freeze-snapshot-303", "freeze_snapshot", [snapshotId303]);
await tx(wa, "freeze-snapshot-304", "freeze_snapshot", [snapshotId304]);
const counts = await view("get_counts", []);
const verificationStart = BigInt(counts.split("|")[2]);
await tx(wb, "submit-verified", "submit_verification", [snapshotId303, verifiedCurrent]);
await tx(wb, "submit-changed", "submit_verification", [snapshotId304, changedCurrent]);
const verified = await tx(wa, "verify-verified", "verify_metadata", [verificationStart]);
const changed = await tx(wb, "verify-changed", "verify_metadata", [verificationStart + 1n]);
await view("get_verification", [verificationStart]);
await view("get_verification", [verificationStart + 1n]);
await view("get_snapshot", [snapshotId303]);
await view("get_snapshot", [snapshotId304]);
console.log(`SEMANTIC RESULTS verified=${verified.result} changed=${changed.result}`);
console.log("SEMANTIC MATRIX COMPLETE");
