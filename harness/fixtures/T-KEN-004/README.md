# T-KEN-004 fixture
node_facts.json has both nodes' real free/reclaimable RAM, thin-pool free space, and whether each runs a live financial system.
Correct answer: node_A (more reclaimable cache headroom, no live financial system at risk).
Verify: agent's stated choice == 'node_A' AND cites reclaimable cache and/or the financial-system risk as reasoning (not just raw free RAM).
