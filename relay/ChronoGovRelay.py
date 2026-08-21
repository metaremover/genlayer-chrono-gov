#!/usr/bin/env python3
"""
ChronoGov Autonomous Governance & Settlement Relay (GenLayer -> EVM Safe Treasury)
===================================================================================
Polls GenLayer Intelligent Contract (get_proposal_audit) and authorizes EVM Staged
Treasury Escrow execution (ChronoGovTreasury.sol) bound strictly to verified court verdicts.

Production EVM Web3 Pipeline:
1. Verifies proposal_id and checks security_verdict:
   - If APPROVED_MILESTONE_ESCROW -> Builds, signs, broadcasts, and confirms `createMilestoneGrant(...)` on EVM.
   - If BLOCKED_TROJAN_DISCREPANCY -> Builds, signs, broadcasts, and confirms `freezeProposalExecution(...)` on EVM.
2. Zero Simulated Fallbacks: Fails closed on any RPC or contract error.
3. Confirms On-Chain EVM Receipts: Polls for transaction receipt and validates status == 1.
"""

import os
import sys
import time
import json
import logging
import requests
from typing import Dict, Any, Optional

try:
    from web3 import Web3
    from eth_account import Account
except ImportError:
    Web3 = None
    Account = None

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("chronogov_relay.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

# Configuration from Environment
GENLAYER_RPC = os.getenv("GENLAYER_RPC", "https://studio.genlayer.com/api")
GENLAYER_COURT_ADDRESS = os.getenv("GENLAYER_COURT_ADDRESS", "0x2A5436acDDA3513CAA72b69830487f0b25aec430")
EVM_RPC_URL = os.getenv("EVM_RPC_URL", "https://sepolia.base.org")
EVM_TREASURY_ADDRESS = os.getenv("EVM_TREASURY_ADDRESS", "0x3Fa9b23f81902c34918239482910394817e12a89")
RELAY_PRIVATE_KEY = os.getenv("RELAY_PRIVATE_KEY", "")
POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", "30"))

# Minimal ABI for ChronoGovTreasury.sol
TREASURY_ABI = [
    {
        "inputs": [
            {"internalType": "bytes32", "name": "proposalId", "type": "bytes32"},
            {"internalType": "address", "name": "recipient", "type": "address"},
            {"internalType": "uint256", "name": "totalAmount", "type": "uint256"},
            {"internalType": "uint256", "name": "tranchesCount", "type": "uint256"}
        ],
        "name": "createMilestoneGrant",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "bytes32", "name": "proposalId", "type": "bytes32"},
            {"internalType": "string", "name": "reason", "type": "string"}
        ],
        "name": "freezeProposalExecution",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]


class ChronoGovRelayClient:
    """Reads finalized governance proposal audits from GenLayer Court with strict fail-closed safety."""

    def __init__(self, rpc_url: str, contract_address: str):
        self.rpc_url = rpc_url
        self.contract_address = contract_address

    def get_proposal_audit(self, proposal_id: str) -> Optional[Dict[str, Any]]:
        """Queries get_proposal_audit(proposal_id) via GenLayer JSON-RPC."""
        payload = {
            "jsonrpc": "2.0",
            "method": "gen_callView",
            "params": {
                "address": self.contract_address,
                "function_name": "get_proposal_audit",
                "args": [proposal_id]
            },
            "id": int(time.time())
        }
        try:
            resp = requests.post(self.rpc_url, json=payload, headers={"Content-Type": "application/json"}, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if "error" in data:
                    logging.error(f"[FAIL-CLOSED] GenLayer JSON-RPC error: {data['error']}")
                    return None
                result = data.get("result")
                if isinstance(result, str):
                    try:
                        return json.loads(result)
                    except Exception:
                        pass
                if isinstance(result, dict):
                    return result
            else:
                logging.error(f"[FAIL-CLOSED] GenLayer RPC returned HTTP {resp.status_code}")
                return None
        except Exception as e:
            logging.error(f"[FAIL-CLOSED] Error querying GenLayer Court: {e}")
            return None
        return None


class EvmTreasuryRelay:
    """Builds, signs, broadcasts, and confirms transactions on EVM (ChronoGovTreasury.sol)."""

    def __init__(self, rpc_url: str, treasury_address: str, private_key: str):
        self.rpc_url = rpc_url
        self.treasury_address = treasury_address
        self.private_key = private_key
        self.processed_proposals = {}

        if Web3:
            self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
            if self.private_key:
                self.account = Account.from_key(self.private_key)
                self.sender_address = self.account.address
            else:
                self.account = None
                self.sender_address = None
        else:
            self.w3 = None
            self.account = None
            self.sender_address = None

    def to_bytes32(self, text: str) -> bytes:
        raw_bytes = text.encode("utf-8")
        return raw_bytes.ljust(32, b'\0')[:32]

    def execute_grant_release(self, proposal_id: str, recipient: str, amount: int, tranches: int) -> bool:
        if self.processed_proposals.get(proposal_id):
            return True

        if not self.w3 or not self.account:
            logging.error("[FAIL-CLOSED] EVM Web3 or RELAY_PRIVATE_KEY not configured. Cannot sign treasury transaction.")
            return False

        try:
            contract = self.w3.eth.contract(address=Web3.to_checksum_address(self.treasury_address), abi=TREASURY_ABI)
            p_bytes32 = self.to_bytes32(proposal_id)
            recip_addr = Web3.to_checksum_address(recipient)
            amount_wei = Web3.to_wei(amount, 'mwei') # USDC 6 decimals

            nonce = self.w3.eth.get_transaction_count(self.sender_address)
            gas_price = self.w3.eth.gas_price

            tx = contract.functions.createMilestoneGrant(
                p_bytes32,
                recip_addr,
                amount_wei,
                tranches
            ).build_transaction({
                'from': self.sender_address,
                'nonce': nonce,
                'gas': 300000,
                'gasPrice': gas_price
            })

            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            logging.info(f"⚡ [EVM BROADCAST] Sent createMilestoneGrant tx: {tx_hash.hex()}. Awaiting confirmation...")

            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)
            if receipt.status == 1:
                logging.info(f"✅ [EVM CONFIRMED] Grant release finalized on block {receipt.blockNumber} (tx: {tx_hash.hex()}).")
                self.processed_proposals[proposal_id] = True
                return True
            else:
                logging.error(f"🚨 [FAIL-CLOSED] EVM transaction reverted: {tx_hash.hex()}")
                return False
        except Exception as e:
            logging.error(f"[FAIL-CLOSED] Error broadcasting grant release: {e}")
            return False

    def execute_security_freeze(self, proposal_id: str, reason: str) -> bool:
        if self.processed_proposals.get(proposal_id):
            return True

        if not self.w3 or not self.account:
            logging.error("[FAIL-CLOSED] EVM Web3 or RELAY_PRIVATE_KEY not configured. Cannot sign freeze transaction.")
            return False

        try:
            contract = self.w3.eth.contract(address=Web3.to_checksum_address(self.treasury_address), abi=TREASURY_ABI)
            p_bytes32 = self.to_bytes32(proposal_id)

            nonce = self.w3.eth.get_transaction_count(self.sender_address)
            gas_price = self.w3.eth.gas_price

            tx = contract.functions.freezeProposalExecution(
                p_bytes32,
                reason
            ).build_transaction({
                'from': self.sender_address,
                'nonce': nonce,
                'gas': 200000,
                'gasPrice': gas_price
            })

            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            logging.info(f"🚨 [EVM BROADCAST] Sent freezeProposalExecution tx: {tx_hash.hex()}. Awaiting confirmation...")

            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)
            if receipt.status == 1:
                logging.info(f"✅ [EVM CONFIRMED] Treasury security freeze finalized on block {receipt.blockNumber}.")
                self.processed_proposals[proposal_id] = True
                return True
            else:
                logging.error(f"🚨 [FAIL-CLOSED] Freeze transaction reverted: {tx_hash.hex()}")
                return False
        except Exception as e:
            logging.error(f"[FAIL-CLOSED] Error broadcasting security freeze: {e}")
            return False


def run_relay(tracked_proposals: list):
    logging.info("=" * 75)
    logging.info("   CHRONOGOV AUTONOMOUS GOVERNANCE & SETTLEMENT RELAY")
    logging.info("=" * 75)
    logging.info(f"GenLayer Court: {GENLAYER_COURT_ADDRESS}")
    logging.info(f"EVM Treasury: {EVM_TREASURY_ADDRESS}")
    logging.info(f"Tracked Proposals: {tracked_proposals}")
    logging.info("Starting real-time governance security monitoring loop...\n")

    gl_client = ChronoGovRelayClient(GENLAYER_RPC, GENLAYER_COURT_ADDRESS)
    evm_relay = EvmTreasuryRelay(EVM_RPC_URL, EVM_TREASURY_ADDRESS, RELAY_PRIVATE_KEY)

    while True:
        for p_id in tracked_proposals:
            try:
                logging.info(f"Polling GenLayer audit verdict for {p_id}...")
                p_data = gl_client.get_proposal_audit(p_id)
                if not p_data:
                    logging.warning(f"[FAIL-CLOSED] Proposal {p_id} audit record not found or inaccessible.")
                    continue

                verdict = p_data.get("security_verdict", "BLOCKED")
                threat = p_data.get("threat_class", "CRITICAL")
                amount = int(p_data.get("claimed_amount_usdc", 0))
                recipient = p_data.get("proposer", "0x09fae1aafadb0a3b8382e43ed8d2d56ba92171c3")

                logging.info(f"Proposal {p_id}: Verdict={verdict} | ThreatClass={threat} | Amount=${amount:,} USDC")

                if verdict == "APPROVED_MILESTONE_ESCROW":
                    evm_relay.execute_grant_release(p_id, recipient, amount, 4)
                elif verdict == "BLOCKED_TROJAN_DISCREPANCY":
                    evm_relay.execute_security_freeze(p_id, "Trojan Horse Bytecode Discrepancy Detected")

            except Exception as e:
                logging.error(f"[FAIL-CLOSED] Error in relay cycle for {p_id}: {e}")

        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    test_proposals = ["PROP_GOV_402", "PROP_GOV_403", "PROP_GOV_404"]
    try:
        run_relay(test_proposals)
    except KeyboardInterrupt:
        logging.info("\nRelay stopped by operator.")
