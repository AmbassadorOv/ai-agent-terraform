import hashlib
from typing import List, Dict, Any

class ReedSolomonECC:
    def __init__(self, nsym: int = 8):
        self.nsym = nsym
        self.prime = 929

    def gf_mult(self, x: int, y: int) -> int:
        if x == 0 or y == 0: return 0
        return (x * y) % self.prime

    def encode(self, data: List[int]) -> List[int]:
        parity = [0] * self.nsym
        for d in data:
            for i in range(self.nsym - 1, -1, -1):
                parity[i] = self.gf_mult(parity[i], 2) if i == 0 else (parity[i-1] + self.gf_mult(parity[i], 2)) % self.prime
            parity[0] = (parity[0] + d) % self.prime
        return data + parity
