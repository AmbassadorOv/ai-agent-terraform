import hashlib
import time

class ForensicLedger:
    """Master Forensic Immutable Index."""
    def __init__(self):
        self.puf_seed = "HARDWARE_UNCLONABLE_72_UNITS_2026"
        self.ledger = []

    def sign_state(self, state_data: dict, cycle: int):
        timestamp = time.time()
        data_str = str(state_data) + str(cycle) + str(timestamp)
        signature = hashlib.sha256(f"{self.puf_seed}_{data_str}".encode()).hexdigest()

        entry = {
            "timestamp": timestamp,
            "cycle": cycle,
            "data": state_data,
            "signature": signature
        }
        self.ledger.append(entry)
        return signature
