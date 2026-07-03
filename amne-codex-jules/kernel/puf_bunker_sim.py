import hashlib
import random
import time
from dataclasses import dataclass

@dataclass
class PUFResponse:
    challenge: str
    response: str
    puf_id: str
    timestamp: str
    ratio_lock: float

class BunkerPUF:
    def __init__(self, num_units: int = 72):
        self.num_units = num_units
        self.golden_ratio = 1.6181
        self.seed = "SAADIA_BUNKER_PUF_8955"
        self.responses = {}

    def get_response(self, challenge: str, unit_id: int) -> PUFResponse:
        key = f"{challenge}_{unit_id}"
        if key not in self.responses:
            variation = random.random() * 0.001
            raw_response = hashlib.sha256(f"{self.seed}{challenge}{unit_id}{variation}".encode()).hexdigest()
            locked = int(int(raw_response, 16) * self.golden_ratio) % (10**16)
            self.responses[key] = str(locked)

        return PUFResponse(
            challenge=challenge,
            response=self.responses[key],
            puf_id=f"UNIT_{unit_id:02d}",
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            ratio_lock=self.golden_ratio
        )
