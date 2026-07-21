#!/usr/bin/env python3
"""
Tribe of Archers - 1,000 Agents Simulation Runner
Runs the deployment and exits with status 0.
"""

import sys
import os

# Add parent directory to path to resolve imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from _02_imperial_dispatcher import ImperialDispatcher

def main():
    print("[*] Running 1,000 agents simulation...")
    dispatcher = ImperialDispatcher()
    dispatcher.run_deployment()
    sys.exit(0)

if __name__ == "__main__":
    main()
