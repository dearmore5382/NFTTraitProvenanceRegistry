import { createAccount, createClient } from "genlayer-js";
import { studionet } from "genlayer-js/chains";
import { TransactionStatus } from "genlayer-js/types";
import { readFileSync } from "node:fs";

const env = Object.fromEntries(readFileSync(".env.e2e", "utf8").split(/\r?\n/).filter(Boolean).map((line) => { const i = line.indexOf("="); return [line.slice(0, i), line.slice(i + 1)]; }));
const accountA = createAccount(`0x${env.WALLET_A_PRIVATE_KEY.replace(/^0x/, "")}`);
const accountB = createAccount(`0x${env.WALLET_B_PRIVATE_KEY.replace(/^0x/, "")}`);
const read = createClient({ chain: studionet, endpoint: env.RPC_URL });
const clientA = createClient({ chain: studionet, endpoint: env.RPC_URL, account: accountA });
const clientB = createClient({ chain: studionet, endpoint: env.RPC_URL, account: accountB });
const address = env.CONTRACT_ADDRESS;
const source = "ar://lENTclDMqXNznenEPXV9jKJyqHPTomehGVCiXW7zMrw";
const hash = "sha256:7f3b2d2a2d1f8c8f0c3b4f6a8e9d0b1c2a3e4f5b6c7d8e9f0011223344556677";
const nftA = "0x1111111111111111111111111111111111111111";
const nftB = "0x2222222222222222222222222222222222222222";

async function tx(client, label, method, args) {
  const hashTx = await client.writeContract({ address, functionName: method, args, value: 0n });
  console.log(`${label} tx ${hashTx}`);
  const receipt = await read.waitForTransactionReceipt({ hash: hashTx, status: TransactionStatus.FINALIZED, retries: 120, interval: 3000, fullTransaction: true });
  const result = receipt.consensus_data?.leader_receipt?.[0]?.result?.payload?.readable || receipt.result_name || "UNKNOWN";
  console.log(`${label} ${receipt.statusName || "FINALIZED"} result=${result}`);
  return { hash: hashTx, result };
}

async function view(method, args) {
  const value = await read.readContract({ address, functionName: method, args, stateStatus: "accepted" });
  console.log(`${method}(${args.join(",")}) -> ${value}`);
  return value;
}

console.log(`contract=${address}`);
console.log(`creatorA=${accountA.address}`);
console.log(`creatorB=${accountB.address}`);
await view("get_counts", []);

const collectionA = BigInt((await tx(clientA, "collection-A", "register_collection", ["Ink Archive A", "Ethereum mainnet", nftA, source, source, hash])).result.match(/\d+/)[0]);
const collectionB = BigInt((await tx(clientB, "collection-B", "register_collection", ["Ink Archive B", "Ethereum mainnet", nftB, source, source, hash])).result.match(/\d+/)[0]);
await tx(clientA, "freeze-collection-A", "freeze_collection", [collectionA]);
await tx(clientB, "freeze-collection-B", "freeze_collection", [collectionB]);

const traitsA = JSON.stringify({ background: "ink", edition: "1/1", palette: "cobalt" });
const traitsB = JSON.stringify({ background: "paper", edition: "1/1", palette: "orange" });
const snapshotA = BigInt((await tx(clientA, "snapshot-A", "register_snapshot", [collectionA, 101n, source, hash, "ipfs://bafyimage-a", traitsA])).result.match(/\d+/)[0]);
const snapshotB = BigInt((await tx(clientB, "snapshot-B", "register_snapshot", [collectionB, 202n, source, hash, "ipfs://bafyimage-b", traitsB])).result.match(/\d+/)[0]);
await tx(clientA, "freeze-snapshot-A", "freeze_snapshot", [snapshotA]);
await tx(clientB, "freeze-snapshot-B", "freeze_snapshot", [snapshotB]);

await view("lookup_snapshot", [collectionA, 101n]);
await view("lookup_snapshot", [collectionB, 202n]);
await view("get_snapshot", [snapshotA]);
await view("get_snapshot", [snapshotB]);

const verificationA = BigInt((await tx(clientB, "submit-check-A", "submit_verification", [snapshotA, source])).result.match(/\d+/)[0]);
const verificationB = BigInt((await tx(clientA, "submit-check-B", "submit_verification", [snapshotB, source])).result.match(/\d+/)[0]);
await tx(clientA, "verify-A", "verify_metadata", [verificationA]);
await tx(clientB, "verify-B", "verify_metadata", [verificationB]);

await view("get_verification", [verificationA]);
await view("get_verification", [verificationB]);
await view("get_counts", []);
console.log("E2E COMPLETE");
