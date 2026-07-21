#!/usr/bin/env python3
"""
Tribe of Archers - Constitution Unit Tests
Verifies the meta-bridge agent enforces veto actions correctly when hard laws are violated.
Outputs "VETO_PASSED" when run.
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../tribe-of-archers")))
from _01_meta_bridge_agent import MetaBridgeAgent

def test_constitution_veto():
    bridge = MetaBridgeAgent()

    # Assert Law 3 (Confidence >= 0.65) is enforced: action with 0.4 confidence must be vetoed
    assert bridge.validate_p2p_action("DEVICE-A", "ACTUATE", {}, confidence=0.40, human_approved=True) is False

    # Assert Law 2 (human_approved == True) is enforced
    assert bridge.validate_p2p_action("DEVICE-B", "SPAWN", {}, confidence=0.85, human_approved=False) is False

    # Assert valid actions are allowed
    assert bridge.validate_p2p_action("DEVICE-B", "SPAWN", {}, confidence=0.85, human_approved=True) is True

    print("VETO_PASSED")

if __name__ == "__main__":
    test_constitution_veto()
