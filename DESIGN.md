# ChronoGov — Protocol Architecture & Governance Security Model

## 1. Asymmetric Equivalence Principle Design

ChronoGov partitions consensus verification into **Strict State-Driving Enums** and **Deterministic Governance Calculations**:

```
Consensus Payload
├── Strict Fields (100% Exact Match Required):
│   ├── security_verdict: enum ("APPROVED_MILESTONE_ESCROW", "BLOCKED_TROJAN_DISCREPANCY", "QUORUM_ESCALATED_COOLING_OFF")
│   ├── threat_class: enum ("BENIGN_COMMUNITY_GRANT", "CRITICAL_TROJAN_HORSE", "WHALE_OLIGARCHY_RAID")
│   └── clock_fresh: bool (Must be live atomic UTC clock)
└── Deterministic Contract State Machine:
    ├── adjusted_quorum_pct: int (Auto-scales 5% -> 25%)
    ├── timelock_hours: int (0 -> 48h -> Frozen)
    └── staged_tranches: int (4 Staged Milestone Releases)
```

---

## 2. Threat Model & Exploit Neutralization

| Attack Vector | Attacker Strategy | How ChronoGov Neutralizes It |
|---|---|---|
| **Trojan Horse Calldata** | Claims $25k on forum, calls $5M transfer in bytecode. | Net-Asset Outflow Invariant: Scrapes and compares text vs decoded calldata. Blocks execution on discrepancy. |
| **Flash-Loan Whale Ambush** | Borrows $50M in governance tokens to vote in last 5m. | Pre-Proposal Snapshot Lock: Voting power snapshotted pre-proposal. Flash-loans have 0 voting power. |
| **Sybil Sub-Account Splitting** | Splits whale tokens across 500 burner wallets. | Time-Weighted Staking Age (TWSA) + Funding cluster graph aggregation. |
| **Multi-Sig Grant Rug** | Takes lump-sum grant and disappears 30 days later. | Staged Milestone Escrow: Releases 25% kickoff; remaining 75% locked until AI verifies deliverable evidence. |
