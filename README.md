# ChronoGov — Autonomous Anti-Whale DAO Constitution & Governance Guardian

> **"The world's first self-optimizing DAO Constitution on GenLayer. Detects Trojan proposals, neutralizes whale ambushes, and adapts governance rules in real time."**

An Intelligent Contract protocol built on **GenLayer** that eliminates whale governance manipulation, detects Trojan Horse calldata drains, dynamically scales quorum requirements, and enforces staged milestone payouts for DAO grants.

---

## 🔗 Live Deployment & Repository Links

- **GenLayer Explorer Contract**: [`[DEPLOYED_CONTRACT_ADDRESS]`](https://explorer-studio.genlayer.com/)
- **GitHub Repository**: [`https://github.com/[YOUR_USERNAME]/genlayer-chronogov`](https://github.com/)
- **Live Governance Terminal**: [`https://chronogov-web.vercel.app/`](https://chronogov-web.vercel.app/)

---

## 🌟 The Core Problem with Traditional DAOs

Traditional DAO governance (Compound, Tornado Cash, Arbitrum) suffers from 3 critical structural vulnerabilities:
1. **Trojan Horse Calldata Exploits**: Proposals with innocent titles (*"$25,000 Marketing Grant"*) attaching malicious bytecode that drains millions from the DAO treasury.
2. **Whale Ambush & Flash-Voting**: Whales dumping millions of votes in the final 10 minutes of a vote to overpower retail voters.
3. **Lump-Sum Multi-Sig Rugs**: DAOs sending multi-million dollar grants upfront to colluding multi-sigs that abandon the project.

**ChronoGov solves this completely with GenLayer AI Consensus**:
- Audits semantic proposal intent against raw smart contract bytecode.
- Calculates voter concentration entropy (Gini coefficient) and enforces 48h cooling-off timelocks.
- Locks approved funds in a **Staged Milestone Escrow (`ChronoGovTreasury.sol`)** with automatic clawbacks.

---

## 🛡️ The 5-Angle Whale-Proof Defense Matrix

```
+--------------------------------------------------------------------------------------------------+
|                              CHRONOGOV 5-ANGLE WHALE-PROOF SHIELD                                |
+--------------------------------------------------------------------------------------------------+
| Angle 1: Sybil Sub-Account Splitting   -> Time-Weighted Staking Age (TWSA) + Funding Graph Audit  |
| Angle 2: Flash-Loan & Bribes           -> Pre-Proposal Snapshot Lock + Semantic Rationale Gate   |
| Angle 3: Trojan Bytecode / Proxy Calls -> Deep Internal Call-Trace & Net-Flow Invariant Guard     |
| Angle 4: Multi-Sig "Take Money & Run"  -> Staged Milestone Escrow + AI Deliverable Release        |
| Angle 5: Stealth Midnight Proposals    -> Dynamic Attention Entropy & Auto-Cooling Extensions     |
+--------------------------------------------------------------------------------------------------+
```

---

## 📖 Project Explorer: How to Try It (Step-by-Step)

### 1. Open the Live Governance Radar
Open [`https://chronogov-web.vercel.app/`](https://chronogov-web.vercel.app/) to inspect the live DAO Constitution and proposal risk feed.

### 2. Test Safe Community Grant (`audit_governance_proposal`)
* **Proposal ID**: `"PROP_GOV_402"`
* **Evidence URL**: `"https://chronogov-web.vercel.app/demo/mock_proposal_safe_grant.html"`
> *Result: `security_verdict: "APPROVED_MILESTONE_ESCROW"`, matching $50,000 USDC calldata verified. Released to 4-stage milestone vault.*

### 3. Test Trojan Horse Bytecode Drain
* **Proposal ID**: `"PROP_GOV_403"`
* **Evidence URL**: `"https://chronogov-web.vercel.app/demo/mock_proposal_trojan_horse.html"`
> *Result: `security_verdict: "BLOCKED_TROJAN_DISCREPANCY"`, 200x overage detected ($25k title vs $5M drain). Execution permanently frozen!*

### 4. Test Whale Ambush Mitigation
* **Proposal ID**: `"PROP_GOV_404"`
* **Evidence URL**: `"https://chronogov-web.vercel.app/demo/mock_proposal_whale_raid.html"`
> *Result: `security_verdict: "QUORUM_ESCALATED_COOLING_OFF"`, Quorum escalated from 5% to 25% + 48-Hour cooling timelock activated.*

---

## 🚀 Running the Verified Settlement Relay

```bash
export GENLAYER_RPC="https://studio.genlayer.com/api"
export GENLAYER_COURT_ADDRESS="[DEPLOYED_CONTRACT_ADDRESS]"
export EVM_RPC_URL="https://sepolia.base.org"
export EVM_TREASURY_ADDRESS="0x3Fa9b23f81902c34918239482910394817e12a89"

# Run autonomous governance relay bound to court verdicts
python3 relay/ChronoGovRelay.py PROP_GOV_402
```
