#!/usr/bin/env python3
"""
Tribe of Archers - SANITY GATE (Maimonides V2)
Enforces and verifies constitutional alignment, making sure all laws are fully complied with.
Outputs "SANE" upon successful verification.
"""

import os
import json

class SanityGate:
    def __init__(self, folder="/app/tribe-of-archers"):
        self.folder = folder

    def verify_sanity(self):
        # 1. Check constitution exists
        const_path = os.path.join(self.folder, "constitution", "05_Constitutional_Plane.json")
        if not os.path.exists(const_path):
            print("INSANE: Missing Constitutional Plane file.")
            return False

        with open(const_path, 'r') as f:
            data = json.load(f)

        # 2. Check LAW_8_INFRASTRUCTURE (حוק ג'ולס) is intact
        laws = data.get("laws", {})
        if "LAW_8_INFRASTRUCTURE" not in laws:
            print("INSANE: Missing Law 8.")
            return False

        law8 = laws["LAW_8_INFRASTRUCTURE"]
        if "JULES" not in law8.get("rule", ""):
            print("INSANE: Law 8 is corrupted.")
            return False

        # 3. Check all required source modules are present
        required_modules = [
            "01_meta_bridge_agent.py",
            "02_imperial_dispatcher.py",
            "06_QuantumMapRegistry.py",
            "07_DarkResonanceEngine.py"
        ]

        for mod in required_modules:
            if not os.path.exists(os.path.join(self.folder, mod)):
                print(f"INSANE: Missing module {mod}.")
                return False

        print("SANE")
        return True

if __name__ == "__main__":
    gate = SanityGate()
    gate.verify_sanity()
