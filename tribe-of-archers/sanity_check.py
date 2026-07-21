#!/usr/bin/env python3
"""
Tribe of Archers - Sanity Check Package Endpoint
Outputs "SANE" upon execution.
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from _08_SANITY_GATE import SanityGate

def main():
    gate = SanityGate()
    gate.verify_sanity()

if __name__ == "__main__":
    main()
