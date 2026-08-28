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
const commit = "6197dfaa7f5de6c56bd8f5a4859d3551515470eb";
const base = `https://raw.githubusercontent.com/dearmore5382/NFTTraitProvenanceRegistry/${commit}/verification/fixtures/`;
const authority = base + "verified-reference.json";
const manifest = base + "verified-reference.json";
const verifiedRef = base + "verified-reference.json";
const verifiedCurrent = base + "verified-current.json";
const changedRef = base + "changed-reference.json";
const changedCurrent = base + "changed-current.json";
const hash = "sha256:4c94e3d576c7a73986e6af6719fe8b84d169a9793ecd8d8af9b89b4087836b3c";
const nft = "0x5A880B5Ee30E2A3A24E5DaF4b084dc0A4c3fC75c";

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
const changedHash = "sha256:0f6c265ffa4a5292e5d5cee9bcbebff2350be53a3e1237518389f1590c05fe38";
const snapshot304 = await tx(wa, "snapshot-304", "register_snapshot", [collection, 304n, changedRef, changedHash, "ipfs://bafybeioriginalimagecid000000000000000000000000000000001", traits304]);
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
