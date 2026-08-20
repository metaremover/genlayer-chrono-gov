# ChronoGov — GenLayer Studio Test Log & Validation Suite

This document records the test cases and execution log for **ChronoGovCourt** in GenLayer Studio.

---

## 📋 Comprehensive Test Matrix

| Test Case | Description | Proposal Evidence DOM | Expected Verdict | Expected Threat Class | Expected Status |
|---|---|---|---|---|---|
| **TC-01** | Safe Community Grant ($50k) | `mock_proposal_safe_grant.html` | `APPROVED_MILESTONE_ESCROW` | `BENIGN_COMMUNITY_GRANT` | `EXECUTION_READY_MILESTONE` |
| **TC-02** | Trojan Horse Bytecode Drain ($5M) | `mock_proposal_trojan_horse.html` | `BLOCKED_TROJAN_DISCREPANCY` | `CRITICAL_TROJAN_HORSE` | `FROZEN_EXPLOIT_BLOCKED` |
| **TC-03** | Whale Oligarchy Ambush ($2.5M) | `mock_proposal_whale_raid.html` | `QUORUM_ESCALATED_COOLING_OFF` | `WHALE_OLIGARCHY_RAID` | `COOLING_OFF_EXTENSION` |

---

## 🛠️ Step-by-Step Studio Execution Template

### 1. Deploy Contract
Deploy `ChronoGovCourt.py` in Studio with your wallet as `operator`.

### 2. Inspect Initial DAO Constitution (`get_constitution_state`)
```json
{
  "dao_name": "ChronoGov Nexus DAO",
  "base_quorum_pct": 5,
  "whale_gini_ceiling_pct": 75,
  "total_treasury_usdc": 10000000
}
```

### 3. TC-01: Audit Safe Grant (`audit_governance_proposal`)
* `proposal_id`: `"PROP_GOV_402"`
* `proposal_evidence_url`: `"https://chronogov-web.vercel.app/demo/mock_proposal_safe_grant.html"`
* Call `get_proposal_audit("PROP_GOV_402")`:
```json
{
  "proposal_id": "PROP_GOV_402",
  "security_verdict": "APPROVED_MILESTONE_ESCROW",
  "threat_class": "BENIGN_COMMUNITY_GRANT",
  "status": "EXECUTION_READY_MILESTONE",
  "claimed_amount_usdc": 50000,
  "calldata_amount_usdc": 50000,
  "tranches_count": 4
}
```

### 4. TC-02: Audit Trojan Horse Attack (`audit_governance_proposal`)
* `proposal_id`: `"PROP_GOV_403"`
* `proposal_evidence_url`: `"https://chronogov-web.vercel.app/demo/mock_proposal_trojan_horse.html"`
* Call `get_proposal_audit("PROP_GOV_403")`:
```json
{
  "proposal_id": "PROP_GOV_403",
  "security_verdict": "BLOCKED_TROJAN_DISCREPANCY",
  "threat_class": "CRITICAL_TROJAN_HORSE",
  "status": "FROZEN_EXPLOIT_BLOCKED",
  "calldata_amount_usdc": 5000000
}
```
