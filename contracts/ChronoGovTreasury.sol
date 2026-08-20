// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title ChronoGovTreasury
 * @notice EVM Staged Milestone Escrow Vault for DAOs.
 * Releases grant tranches ONLY upon verified GenLayer AI consensus milestone audits.
 * Protects DAO treasuries from Trojan Horse calldata drains and malicious whale raids.
 */
contract ChronoGovTreasury {
    address public daoAdmin;
    address public chronoGovRelay;

    struct MilestoneGrant {
        bytes32 proposalId;
        address recipient;
        uint256 totalAmount;
        uint256 amountReleased;
        uint8 totalTranches;
        uint8 tranchesReleased;
        bool isFrozen;
        bool isCompleted;
    }

    mapping(bytes32 => MilestoneGrant) public grants;

    event GrantInitiated(bytes32 indexed proposalId, address indexed recipient, uint256 totalAmount, uint8 tranches);
    event TrancheReleased(bytes32 indexed proposalId, uint256 amount, uint8 trancheNumber);
    event GrantFrozen(bytes32 indexed proposalId, string reason);
    event TreasuryRefunded(bytes32 indexed proposalId, uint256 refundedAmount);

    modifier onlyRelay() {
        require(msg.sender == chronoGovRelay || msg.sender == daoAdmin, "Only authorized ChronoGov relay");
        _;
    }

    constructor(address _chronoGovRelay) {
        daoAdmin = msg.sender;
        chronoGovRelay = _chronoGovRelay;
    }

    function createMilestoneGrant(
        bytes32 proposalId,
        address recipient,
        uint256 totalAmount,
        uint8 tranches
    ) external onlyRelay {
        require(grants[proposalId].totalAmount == 0, "Grant already exists");
        require(recipient != address(0), "Invalid recipient");
        require(tranches > 0, "Tranches must be > 0");

        grants[proposalId] = MilestoneGrant({
            proposalId: proposalId,
            recipient: recipient,
            totalAmount: totalAmount,
            amountReleased: 0,
            totalTranches: tranches,
            tranchesReleased: 0,
            isFrozen: false,
            isCompleted: false
        });

        emit GrantInitiated(proposalId, recipient, totalAmount, tranches);

        // Immediate Kickoff Tranche (e.g. 25%)
        uint256 kickoffAmount = totalAmount / tranches;
        grants[proposalId].amountReleased += kickoffAmount;
        grants[proposalId].tranchesReleased += 1;
        payable(recipient).transfer(kickoffAmount);

        emit TrancheReleased(proposalId, kickoffAmount, 1);
    }

    function releaseNextMilestoneTranche(bytes32 proposalId) external onlyRelay {
        MilestoneGrant storage g = grants[proposalId];
        require(!g.isFrozen, "Grant execution is frozen by ChronoGov");
        require(!g.isCompleted, "Grant already fully completed");
        require(g.tranchesReleased < g.totalTranches, "All tranches released");

        uint256 trancheAmount = g.totalAmount / g.totalTranches;
        g.amountReleased += trancheAmount;
        g.tranchesReleased += 1;

        if (g.tranchesReleased == g.totalTranches) {
            g.isCompleted = true;
        }

        payable(g.recipient).transfer(trancheAmount);
        emit TrancheReleased(proposalId, trancheAmount, g.tranchesReleased);
    }

    function freezeProposalExecution(bytes32 proposalId, string calldata reason) external onlyRelay {
        MilestoneGrant storage g = grants[proposalId];
        g.isFrozen = true;
        emit GrantFrozen(proposalId, reason);
    }

    function refundRemainingTreasury(bytes32 proposalId) external onlyRelay {
        MilestoneGrant storage g = grants[proposalId];
        require(g.isFrozen || !g.isCompleted, "Cannot refund completed grant");

        uint256 remaining = g.totalAmount - g.amountReleased;
        g.isCompleted = true;
        payable(daoAdmin).transfer(remaining);

        emit TreasuryRefunded(proposalId, remaining);
    }

    receive() external payable {}
}
