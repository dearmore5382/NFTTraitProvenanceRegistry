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
const source = "https://raw.githubusercontent.com/dearmore5382/DAOProposalContextVerifier/main/README.md";
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

await tx(clientA, "collection-A", "register_collection", ["Ink Archive A", "Ethereum mainnet", nftA, source, source, hash]);
await tx(clientB, "collection-B", "register_collection", ["Ink Archive B", "Ethereum mainnet", nftB, source, source, hash]);
await tx(clientA, "freeze-collection-A", "freeze_collection", [0n]);
await tx(clientB, "freeze-collection-B", "freeze_collection", [1n]);

const traitsA = JSON.stringify({ background: "ink", edition: "1/1", palette: "cobalt" });
const traitsB = JSON.stringify({ background: "paper", edition: "1/1", palette: "orange" });
await tx(clientA, "snapshot-A", "register_snapshot", [0n, 101n, source, hash, "ipfs://bafyimage-a", traitsA]);
await tx(clientB, "snapshot-B", "register_snapshot", [1n, 202n, source, hash, "ipfs://bafyimage-b", traitsB]);
await tx(clientA, "freeze-snapshot-A", "freeze_snapshot", [0n]);
await tx(clientB, "freeze-snapshot-B", "freeze_snapshot", [1n]);

await view("lookup_snapshot", [0n, 101n]);
await view("lookup_snapshot", [1n, 202n]);
await view("get_snapshot", [0n]);
await view("get_snapshot", [1n]);

await tx(clientB, "submit-check-A", "submit_verification", [0n, source]);
await tx(clientA, "submit-check-B", "submit_verification", [1n, source]);
await tx(clientA, "verify-A", "verify_metadata", [0n]);
await tx(clientB, "verify-B", "verify_metadata", [1n]);

await view("get_verification", [0n]);
await view("get_verification", [1n]);
await view("get_counts", []);
console.log("E2E COMPLETE");
