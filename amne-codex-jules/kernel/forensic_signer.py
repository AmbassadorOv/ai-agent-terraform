import hashlib
import hmac
import time
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class SignedEntry:
    t: str
    s: str
    h: str
    mac: str
    puf_sig: str
    prev: str
    full_seal: str
    ratio_check: float

class ForensicSigner:
    def __init__(self, master_seed: str = "8955_SHLISHI_231_GATES"):
        self.master_key = hashlib.sha256(master_seed.encode()).digest()
        self.golden_ratio = 1.6181
        self.puf_seed = "HARDWARE_UNCLONABLE_72_UNITS_2026"

    def sign_entry(self, data: Dict[str, Any]) -> SignedEntry:
        entry_str = str(sorted(data.items())).encode()
        h = hashlib.sha256(entry_str).hexdigest()
        mac = hmac.new(self.master_key, entry_str, hashlib.sha256).hexdigest()
        puf_sig = hashlib.sha256(f"{h}{self.puf_seed}{self.golden_ratio}".encode()).hexdigest()

        return SignedEntry(
            t=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            s=data.get("s", "ILCP-DEFAULT"),
            h=h,
            mac=mac,
            puf_sig=puf_sig,
            prev="f6e89d12a3b4c5e6...",
            full_seal=f"SEAL_{puf_sig[:16]}_{self.golden_ratio}",
            ratio_check=self.golden_ratio
        )
