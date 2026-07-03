import json
import os

def process_map_index(file_path):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r") as f:
        data = json.load(f)

    print(f"[*] ANALYZING MAP INDEX: {len(data)} ENTRIES FOUND.")

    anomalies = []
    prev_val = float('inf')

    for entry in data:
        # Use minted_coins as a proxy for efficiency jumps
        curr_val = entry.get("minted_coins", 0)
        if curr_val > prev_val * 2:
            anomalies.append({
                "iteration": entry["iteration"],
                "event": "Significant Coin Minting Spike",
                "delta": round(curr_val - prev_val, 4)
            })
        prev_val = curr_val

    print(f"[*] NON-LINEAR STRUCTURES EXTRACTED: {len(anomalies)}")

    clusters = {
        "High-Scale-Zone": [e["iteration"] for e in data if e["active_agents"] > 1000],
        "Optimal-Integrity-Zone": [e["iteration"] for e in data if e["integrity_score"] > 0.9]
    }

    with open("amne-codex-jules/orchestrator/processed_analysis.json", "w") as f:
        json.dump({"anomalies": anomalies, "clusters": clusters}, f, indent=2)

    print("[*] ANALYSIS COMPLETE. Results saved to processed_analysis.json")

if __name__ == "__main__":
    process_map_index("amne-codex-jules/orchestrator/map_index.json")
