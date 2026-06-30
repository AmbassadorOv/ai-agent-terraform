import numpy as np
import argparse
import json
import os

def run_simulation(seed, state_dim, iterations):
    np.random.seed(seed)
    state = np.random.randn(state_dim)
    for i in range(iterations):
        state += np.random.normal(0, 0.1, state_dim)
    return state

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--state_dim", type=int, default=64)
    parser.add_argument("--iterations", type=int, default=100)
    parser.add_argument("--output", help="Path to output file")
    args = parser.parse_args()

    final_state = run_simulation(args.seed, args.state_dim, args.iterations)
    print(f"Simulation complete for seed {args.seed}. Final state mean: {final_state.mean()}")

    if args.output:
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, "w") as f:
            json.dump({"seed": args.seed, "final_state_mean": float(final_state.mean())}, f)
