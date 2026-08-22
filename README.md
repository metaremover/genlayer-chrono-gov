# ChronoGov — Autonomous Anti-Whale DAO Constitution & Governance Guardian

> **"The world's first self-optimizing DAO Constitution on GenLayer. Detects Trojan proposals, neutralizes whale ambushes, and adapts governance rules in real time."**

An Intelligent Contract protocol built on GenLayer that eliminates whale governance manipulation, detects Trojan Horse calldata drains, dynamically scales quorum requirements, and enforces staged milestone payouts for DAO grants.

---

## 🔗 Live Deployment & Repository Links

- **GenLayer Explorer Contract**: [`0x2A5436acDDA3513CAA72b69830487f0b25aec430`](https://explorer-studio.genlayer.com/address/0x2A5436acDDA3513CAA72b69830487f0b25aec430)
- **GitHub Repository**: [`https://github.com/metaremover/genlayer-chrono-gov`](https://github.com/metaremover/genlayer-chrono-gov)
- **Live Governance Terminal**: [`https://genlayer-chrono-gov.vercel.app/`](https://genlayer-chrono-gov.vercel.app/)

---

## 🌟 The Core Problem with Traditional DAOs

Traditional DAO governance (Compound, Tornado Cash, Arbitrum) suffers from 3 critical structural vulnerabilities:
1. **Trojan Horse Calldata Exploits**: Proposals with innocent titles ("$25,000 Marketing Grant") attaching malicious bytecode that drains millions from the DAO treasury.
2. **Whale Ambush & Flash-Voting**: Whales dumping millions of votes in the final 10 minutes of a vote to overpower retail voters.
3. **Lump-Sum Multi-Sig Rugs**: DAOs sending multi-million dollar grants upfront to colluding multi-sigs that abandon the project.

**ChronoGov solves this completely with GenLayer AI Consensus**:
- Audits semantic proposal intent against raw smart contract bytecode.
- Calculates voter concentration entropy (Gini coefficient) and enforces 48h cooling-off timelocks.
- Locks approved funds in a Staged Milestone Escrow (`ChronoGovTreasury.sol`) with automatic clawbacks.

---

## 🛡️ The 5-Angle Whale-Proof Defense Matrix

```
+--------------------------------------------------------------------------------------------------+
|                              CHRONOGOV 5-ANGLE WHALE-PROOF SHIELD                                |
+--------------------------------------------------------------------------------------------------+
| Angle 1: Sybil Sub-Account Splitting -> Time-Weighted Staking Age (TWSA) + Funding Graph Audit   |
| Angle 2: Flash-Loan & Bribes        -> Pre-Proposal Snapshot Lock + Semantic Rationale Gate      |
| Angle 3: Trojan Bytecode / Proxy     -> Deep Internal Call-Trace & Net-Flow Invariant Guard       |
| Angle 4: Multi-Sig "Take Money"      -> Staged Milestone Escrow + AI Deliverable Release          |
| Angle 5: Stealth Midnight Proposals  -> Dynamic Attention Entropy & Auto-Cooling Extensions      |
+--------------------------------------------------------------------------------------------------+
```

---

## 📖 Project Explorer: How to Try It (Step-by-Step)

### 1. Open the Live Governance Radar
Open [`https://genlayer-chrono-gov.vercel.app/`](https://genlayer-chrono-gov.vercel.app/) to inspect the live DAO Constitution and proposal risk feed.

### 2. Test Trojan Horse Attack (`PROP_GOV_403`)
* **Scenario**: Proposer requests $25,000 in plain English, but encodes a 200x extraction ($5,000,000 USDC) in bytecode.
* Click **"2. Trojan Horse"** $\rightarrow$ **"Execute GenLayer Autonomous Governance Audit"**.
> *Result: AI Consensus detects discrepancy and executes an emergency freeze on the EVM treasury.*

### 3. Test Whale Ambush (`PROP_GOV_404`)
* **Scenario**: Single whale wallet provides 92.4% of total votes.
* Click **"3. Whale Ambush"** $\rightarrow$ **"Execute GenLayer Autonomous Governance Audit"**.
> *Result: Gini index exceeds 75% ceiling $\rightarrow$ Quorum dynamically escalates from 5% to 25% + 48h cooling-off timelock enforced.*

### 4. Test Safe Sub-Grant (`PROP_GOV_402`)
* Click **"1. Safe Sub-Grant"** $\rightarrow$ Approved for 4-stage milestone release (25% kickoff).

---

## 🚀 Running the Production Web3 Relay

```bash
export GENLAYER_RPC="https://studio.genlayer.com/api"
export GENLAYER_COURT_ADDRESS="0x2A5436acDDA3513CAA72b69830487f0b25aec430"
export EVM_RPC_URL="https://sepolia.base.org"
export EVM_TREASURY_ADDRESS="0x3Fa9b23f81902c34918239482910394817e12a89"
export RELAY_PRIVATE_KEY="0x..."

# Run real Web3 signed relay
python3 relay/ChronoGovRelay.py
```
