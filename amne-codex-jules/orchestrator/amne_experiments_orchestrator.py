import ray
import torch
import torch.nn as nn
from ray import train
from ray.train.torch import TorchTrainer
from ray.train import ScalingConfig
from dataclasses import dataclass
import torch.nn.functional as F
import argparse
import json
import os

@dataclass
class ScalingState:
    crp_inflight: int
    router_entropy: float
    active_agents: int
    queue_depth: int
    avg_latency_ms: float
    cluster_utilization: float

class MetaAutoscaler:
    def __init__(self, min_agents=500, max_agents=1000):
        self.min_agents = min_agents
        self.max_agents = max_agents

    def compute_target_scale(self, state: ScalingState):
        def normalize(val, max_val=10000): return min(val / max_val, 1.0)
        demand = (0.4 * normalize(state.queue_depth, 5000) +
                  0.3 * normalize(state.crp_inflight, 2000) +
                  0.2 * state.router_entropy +
                  0.1 * normalize(state.avg_latency_ms, 500))
        target = int(self.min_agents + (self.max_agents - self.min_agents) * demand)
        return max(self.min_agents, min(target, self.max_agents))

class MetaRouter(nn.Module):
    def __init__(self, n_experts=1000, hidden_dim=256):
        super().__init__()
        self.gate = nn.Linear(hidden_dim, n_experts)
        self.temperature = nn.Parameter(torch.tensor(2.0))

    def forward(self, x, top_k=20):
        logits = self.gate(x)
        tau = torch.clamp(self.temperature, 0.1, 5.0)
        probs = torch.softmax(logits / tau, dim=-1)
        topk_probs, topk_indices = torch.topk(probs, top_k, dim=-1)
        entropy = -torch.sum(probs * torch.log(probs + 1e-9), dim=-1).mean()
        return topk_probs, topk_indices, entropy

def train_loop_per_worker(config):
    model = MetaRouter(n_experts=100) # Reduced for demo
    model = train.torch.prepare_model(model)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    for epoch in range(config.get("epochs", 5)):
        inputs = torch.randn(32, 256)
        targets = torch.rand(32, 100)

        optimizer.zero_grad()
        topk_probs, topk_indices, entropy = model(inputs)
        dense_outputs = torch.zeros(32, 100, device=inputs.device)
        dense_outputs.scatter_(1, topk_indices, topk_probs)

        loss = nn.MSELoss()(dense_outputs, targets) - (0.01 * entropy)
        loss.backward()
        optimizer.step()

        train.report({
            "loss": loss.item(),
            "temperature": model.module.temperature.item() if hasattr(model, 'module') else model.temperature.item(),
            "entropy": entropy.item()
        })

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Path to config file")
    parser.add_argument("--versions", help="Comma-separated versions")
    args = parser.parse_args()

    print(f"Starting AMNE Orchestrator with config: {args.config}")

    ray.init(ignore_reinit_error=True)
    scaling_config = ScalingConfig(num_workers=1, use_gpu=False)
    trainer = TorchTrainer(
        train_loop_per_worker=train_loop_per_worker,
        train_loop_config={"epochs": 2},
        scaling_config=scaling_config
    )
    result = trainer.fit()
    print("Training loop complete. Meta-Router updated.")

    os.makedirs("outputs", exist_ok=True)
    with open("outputs/meta_summary.json", "w") as f:
        json.dump({"status": "success", "versions": args.versions}, f)
