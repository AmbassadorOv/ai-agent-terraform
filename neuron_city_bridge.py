import time
import uuid
import random
from typing import List, Dict, Any, Optional

class LatencyExceededError(Exception):
    """Exception raised when Urban Backpropagation latency exceeds the critical 100ms threshold."""
    pass

class Embedding:
    """
    Represents an Edge Federated Neural Signal.
    In compliance with Rule 1, no central raw data or heavy state is transmitted;
    only the low-dimensional mathematical representation (Embeddings) flows between nodes.
    """
    def __init__(self, vector: List[float], source_neuron: str, payload_metadata: Dict[str, Any]):
        self.vector = vector
        self.source_neuron = source_neuron  # e.g., "SEOUL_S_MAP_EYE_04"
        self.payload_metadata = payload_metadata
        self.timestamp = time.time()
        self.id = str(uuid.uuid4())

    def __repr__(self):
        return f"Embedding(ID={self.id[:8]}, Source={self.source_neuron}, VectorDim={len(self.vector)})"


class SL0000Thalamus:
    """
    ARK GENESIS PRIME = SL0000 = The Thalamus.
    Acts as the brain's central relay and filter.
    Enforces Rule 3: "Fire > Traffic".
    Filters routine urban noise (routine telemetry) and elevates high-priority critical spikes (e.g., fire, structural faults, robot_error).
    """
    def __init__(self, noise_threshold: float = 0.65):
        self.noise_threshold = noise_threshold
        print("🤖 [SL0000 Thalamus] Implanted & Initialized. Synapses established.")

    def process(self, embedding: Embedding) -> Dict[str, Any]:
        """
        Processes an incoming Embedding.
        Determines the priority index and routes or filters the signal.
        """
        # Calculate mock attention score or "importance vector"
        # In this simulation, critical errors (like robot_error) produce high priority signals
        event_type = embedding.payload_metadata.get("event_type", "routine_traffic")
        intensity = embedding.payload_metadata.get("severity", 0.1)

        # Rule 3: Fire > Traffic (Critical events bypass standard queue, regular noise is filtered)
        is_critical = event_type in ["robot_error", "fire", "structural_failure"] or intensity >= self.noise_threshold

        priority = "CRITICAL_FIRE" if is_critical else "ROUTINE_TRAFFIC"

        # Simulated Core42 GPU processing time
        gpu_processing_delay = random.uniform(0.005, 0.015) # 5ms to 15ms
        time.sleep(gpu_processing_delay)

        return {
            "embedding_id": embedding.id,
            "decision": "ACTUATE_IMMEDIATELY" if is_critical else "LOG_AND_DROP",
            "priority": priority,
            "relevance_score": intensity,
            "target_system": "HYUNDAI_ACTUATORS",
            "action_command": embedding.payload_metadata.get("recommended_remedy", "STANDBY")
        }


class WeGOMENAProtocolBridge:
    """
    WeGO MENA = Vagus Nerve / Protocol Bridge.
    Translates "Seoul" spatial/neural state transformations to "Abu Dhabi" motor commands.
    Enforces Rule 2: Urban Backpropagation (Seoul -> Abu Dhabi < 100ms).
    Contains Hard_Null_Check for strict latency compliance.
    """
    def __init__(self, thalamus: SL0000Thalamus):
        self.thalamus = thalamus
        print("🧠 [WeGO MENA] Protocol Bridge online. Vagus Nerve connection initialized.")

    def hard_null_check(self, start_time: float):
        """
        Strict latency barrier.
        If current elapsed time exceeds 100 milliseconds, instantly raise LatencyExceededError
        to prevent out-of-order execution or desynchronization of the digital twin.
        """
        elapsed_ms = (time.time() - start_time) * 1000.0
        if elapsed_ms > 100.0:
            raise LatencyExceededError(
                f"🚨 CRITICAL HARD_NULL_CHECK VIOLATION: Urban Backpropagation latency is {elapsed_ms:.2f}ms "
                f"(Exceeds the maximum permissible 100ms limit). Neural desync risk detected!"
            )

    def route_signal(self, embedding: Embedding, simulate_network_delay: float = 0.0) -> Dict[str, Any]:
        """
        Receives an edge federated embedding from Seoul, processes it via the Thalamus,
        and translates it for Abu Dhabi's Hyundai Robot Motor Cortex.
        """
        start_time = time.time()
        print(f"\n⚡ [Neural Impulse Triggered] Routing embedding {embedding.id[:8]} from {embedding.source_neuron}...")

        # Simulate network or transmission delay
        if simulate_network_delay > 0:
            print(f"⏳ [Network Congestion Simulated] Injecting {simulate_network_delay * 1000:.2f}ms delay...")
            time.sleep(simulate_network_delay)

        # Perform Hard_Null_Check during early transit
        self.hard_null_check(start_time)

        # Process through SL0000 Thalamus
        thalamus_decision = self.thalamus.process(embedding)

        # Perform Hard_Null_Check post-processing
        self.hard_null_check(start_time)

        elapsed_ms = (time.time() - start_time) * 1000.0
        print(f"✅ [Urban Backpropagation Complete] Total latency: {elapsed_ms:.2f}ms (Under 100ms Limit)")

        return {
            "status": "PROPAGATED",
            "latency_ms": elapsed_ms,
            "thalamus_decision": thalamus_decision
        }


# ==========================================
# DEMO SCENARIOS
# ==========================================

def run_simulation():
    print("=" * 70)
    print("    OPERATION NEURON CITY: THALAMUS IMPLANT - DEMO LIVE RUN")
    print("=" * 70)

    # Initialize the systems
    thalamus = SL0000Thalamus(noise_threshold=0.65)
    wego_bridge = WeGOMENAProtocolBridge(thalamus)

    # Mock Seoul S-Map (Eyes + Spatial Transformer)
    print("\n[Seoul S-Map] Digital Twin updated (Refresh interval: 5m).")

    # Scenario 1: Robot error in Seoul (S-Map registers failure -> immediate Urban Backpropagation)
    print("\n--- SCENARIO 1: ROBOT ERROR IN SEOUL (URBAN BACKPROPAGATION < 100ms) ---")
    seoul_error_embedding = Embedding(
        vector=[0.98, -0.12, 0.45, 0.88, 0.01],
        source_neuron="SEOUL_S_MAP_SECTOR_4_CAM_09",
        payload_metadata={
            "event_type": "robot_error",
            "severity": 0.95,
            "location": "Seoul Assembly Line B",
            "recommended_remedy": "ENGAGE_HYUNDAI_EMERGENCY_STOP_ABU_DHABI"
        }
    )

    try:
        # Expected to complete in ~10-25ms (well below 100ms)
        propagation_result = wego_bridge.route_signal(seoul_error_embedding, simulate_network_delay=0.01) # 10ms network delay
        decision = propagation_result["thalamus_decision"]

        print("\n🤖 [Hyundai Robots / Abu Dhabi Motor Cortex Actuation]")
        if decision["decision"] == "ACTUATE_IMMEDIATELY":
            print(f"💥 ACTION EXECUTED: Translating decision to Abu Dhabi Robot controllers.")
            print(f"👉 COMMAND SENT: {decision['action_command']}")
            print("🟢 STATUS: Abu Dhabi assembly system safely locked/re-routed.")
        else:
            print("⚪ STATUS: No emergency action required.")

    except LatencyExceededError as e:
        print(e)

    # Scenario 2: Routine Traffic in Seoul (Filtered out by Thalamus "Fire > Traffic" Rule 3)
    print("\n--- SCENARIO 2: ROUTINE TRAFFIC (SL0000 FILTERS NOISE) ---")
    seoul_routine_embedding = Embedding(
        vector=[0.11, 0.05, -0.02, 0.04, 0.12],
        source_neuron="SEOUL_S_MAP_SECTOR_1_LIDAR_22",
        payload_metadata={
            "event_type": "routine_traffic",
            "severity": 0.15,
            "location": "Seoul Public Plaza Checkpoint",
            "recommended_remedy": "LOG_ROUTINE_FLOW"
        }
    )

    propagation_result = wego_bridge.route_signal(seoul_routine_embedding, simulate_network_delay=0.005)
    decision = propagation_result["thalamus_decision"]
    print(f"Thalamus Decision Priority: {decision['priority']}")
    print(f"Action Code: {decision['decision']}")
    print("🟢 STATUS: Noise successfully filtered out. Zero urban desensitization.")

    # Scenario 3: Hard Null Check Failure (Simulated fiber-optic drop / delay > 100ms)
    print("\n--- SCENARIO 3: NETWORK DEGRADATION (HARD_NULL_CHECK EXCEPTION TRIGGERED) ---")
    delayed_embedding = Embedding(
        vector=[0.99, -0.11, 0.44, 0.89, 0.02],
        source_neuron="SEOUL_S_MAP_SECTOR_4_CAM_09",
        payload_metadata={
            "event_type": "robot_error",
            "severity": 0.95,
            "location": "Seoul Assembly Line B",
            "recommended_remedy": "ENGAGE_HYUNDAI_EMERGENCY_STOP_ABU_DHABI"
        }
    )

    try:
        # Simulate network delay of 120ms (exceeding 100ms limit)
        wego_bridge.route_signal(delayed_embedding, simulate_network_delay=0.12)
    except LatencyExceededError as e:
        print(f"\n❌ EXCEPTION CAUGHT SUCCESSFULLY as part of safety guarantees:")
        print(f"{e}")
        print("🛡️ Safety protocols successfully engaged: Prevented stale/delayed decision execution in Abu Dhabi.")

    print("\n" + "=" * 70)
    print("    OPERATION NEURON CITY: SYSTEM DEMO COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    run_simulation()
