import time
import uuid
import random
import sys
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
    def __init__(self, vector: List[float], source_branch: str, source_sub: str, payload_metadata: Dict[str, Any]):
        self.vector = vector
        self.source_branch = source_branch  # e.g., "SEL-MOB"
        self.source_sub = source_sub        # e.g., "SUWON-01"
        self.payload_metadata = payload_metadata
        self.timestamp = time.time()
        self.id = str(uuid.uuid4())

    def __repr__(self):
        return f"Embedding(ID={self.id[:8]}, Source={self.source_branch}/{self.source_sub}, VectorDim={len(self.vector)})"


# =====================================================================
# WGI BRANCH REGISTRY (Grounded on the multi-branch JSON topology)
# =====================================================================
WGI_BRANCH_TOPOLOGY = [
    {
        "Branch_ID": "TLV-HQ",
        "Sub_Branch_ID": "TLV-HQ-CORE-01",
        "Sub_Branch_Name": "Data Normalization & Protocol Bridge",
        "Operational_Role": "ניהול אינטגרציה, נורמליזציה שפתית וסנכרון פרוטוקולים מול WGI-HQ",
        "Active_Agents": 5000,
        "Agent_Type": "Data_Bridge_Agents",
        "ID_Range": "hybrid_00000 - hybrid_04999",
        "Hardware_Requirement": "Edge CPU (No-GPU / Zero-NVIDIA)",
        "Execution_Command": "python /app/agent_worker.py --branch TLV --sub CORE-01"
    },
    {
        "Branch_ID": "TLV-HQ",
        "Sub_Branch_ID": "TLV-HQ-GOV-02",
        "Sub_Branch_Name": "Consortium Compliance & Audit",
        "Operational_Role": "בקרת תאימות רגולטורית, ניהול קונסורציום מקומי וארכוב החלטות",
        "Active_Agents": 5000,
        "Agent_Type": "Governance_Audit_Agents",
        "ID_Range": "hybrid_05000 - hybrid_09999",
        "Hardware_Requirement": "Edge CPU (No-GPU / Zero-NVIDIA)",
        "Execution_Command": "python /app/agent_worker.py --branch TLV --sub GOV-02"
    },
    {
        "Branch_ID": "AUH-GOV",
        "Sub_Branch_ID": "AUH-GOV-API-01",
        "Sub_Branch_Name": "Government API Actuation",
        "Operational_Role": "אקטיואציה מבוזרת, ממשק ישיר ל-APIs ממשלתיים ואימות פקודות",
        "Active_Agents": 10000,
        "Agent_Type": "Actuator_Core_Agents",
        "ID_Range": "actuator_00000 - actuator_09999",
        "Hardware_Requirement": "Edge CPU / Micro-Controller",
        "Execution_Command": "python /app/agent_worker.py --branch AUH --sub API-01"
    },
    {
        "Branch_ID": "AUH-GOV",
        "Sub_Branch_ID": "AUH-GOV-INFRA-02",
        "Sub_Branch_Name": "Infrastructure State Sync",
        "Operational_Role": "סנכרון מצב תשתיות לאומיות בזמן אמת ללא השהיית ענן",
        "Active_Agents": 10000,
        "Agent_Type": "Actuator_State_Agents",
        "ID_Range": "actuator_10000 - actuator_19999",
        "Hardware_Requirement": "Edge CPU / Micro-Controller",
        "Execution_Command": "python /app/agent_worker.py --branch AUH --sub INFRA-02"
    },
    {
        "Branch_ID": "SEL-MOB",
        "Sub_Branch_ID": "SEL-MOB-SUWON-01",
        "Sub_Branch_Name": "Suwon Base Physical AI & Delivery Fleet",
        "Operational_Role": "ניהול ניווט עצמאי ובטיחות בזמן אמת עבור רובוטי סיור ומשלוחים ב-Suwon Base-Type",
        "Active_Agents": 7000,
        "Agent_Type": "Physical_AI_Edge_Agents",
        "ID_Range": "sensor_00000 - sensor_06999",
        "Hardware_Requirement": "On-Board Edge CPU (Zero-GPU)",
        "Execution_Command": "python /app/agent_worker.py --branch SEL --sub SUWON-01"
    },
    {
        "Branch_ID": "SEL-MOB",
        "Sub_Branch_ID": "SEL-MOB-SNG-02",
        "Sub_Branch_Name": "Seongnam ADL Healthcare & Shuttles",
        "Operational_Role": "ניטור סמוי של מדדי ADL לקשישים ותיאום שאטלים אוטונומיים ב-Seongnam Complex",
        "Active_Agents": 7000,
        "Agent_Type": "Privacy_ADL_Shuttle_Agents",
        "ID_Range": "sensor_07000 - sensor_13999",
        "Hardware_Requirement": "IoT Domestic Edge CPU",
        "Execution_Command": "python /app/agent_worker.py --branch SEL --sub SNG-02"
    },
    {
        "Branch_ID": "SEL-MOB",
        "Sub_Branch_ID": "SEL-MOB-PUSAN-03",
        "Sub_Branch_Name": "Busan Centum AX Standardization Engine",
        "Operational_Role": "תרגום זרמי וידאו ונתוני מצלמות לפורמט טקסטואלי קל ב-Busan Centum AX",
        "Active_Agents": 6000,
        "Agent_Type": "AX_Textual_Standardization_Agents",
        "ID_Range": "sensor_14000 - sensor_19999",
        "Hardware_Requirement": "Edge CPU (Replacing GPU Clusters)",
        "Execution_Command": "python /app/agent_worker.py --branch SEL --sub PUSAN-03"
    },
    {
        "Branch_ID": "SGP-FIN",
        "Sub_Branch_ID": "SGP-FIN-ALLOC-01",
        "Sub_Branch_Name": "Dynamic Edge Resource Allocation",
        "Operational_Role": "אופטימיזציית משאבי מחשוב ואנרגיה בקצה, מניעת תשלום על ענן / GPU",
        "Active_Agents": 10000,
        "Agent_Type": "Resource_Optimization_Agents",
        "ID_Range": "hybrid_10000 - hybrid_19999",
        "Hardware_Requirement": "Low-Power Edge CPU",
        "Execution_Command": "python /app/agent_worker.py --branch SGP --sub ALLOC-01"
    },
    {
        "Branch_ID": "SGP-FIN",
        "Sub_Branch_ID": "SGP-FIN-COST-02",
        "Sub_Branch_Name": "Zero-Cost Execution Ledger",
        "Operational_Role": "מאזן תפעולי רציף 24/7 להבטחת אפס עלויות תפעול קבועות (GitHub Free / Local Hardware)",
        "Active_Agents": 10000,
        "Agent_Type": "Cost_Ledger_Agents",
        "ID_Range": "hybrid_20000 - hybrid_29999",
        "Hardware_Requirement": "Low-Power Edge CPU",
        "Execution_Command": "python /app/agent_worker.py --branch SGP --sub COST-02"
    },
    {
        "Branch_ID": "ZRH-SEC",
        "Sub_Branch_ID": "ZRH-SEC-VERIF-01",
        "Sub_Branch_Name": "Zero-Trust Edge Verification",
        "Operational_Role": "אימות קצה היקפי, בקרת שלמות נתונים ומניעת זיוף קלט ברשת הסוכנים",
        "Active_Agents": 15000,
        "Agent_Type": "Security_Verification_Agents",
        "ID_Range": "sensor_20000 - sensor_27499 / actuator_20000 - actuator_27499",
        "Hardware_Requirement": "Secure Edge Node (CPU)",
        "Execution_Command": "python /app/agent_worker.py --branch ZRH --sub VERIF-01"
    },
    {
        "Branch_ID": "ZRH-SEC",
        "Sub_Branch_ID": "ZRH-SEC-PRIV-02",
        "Sub_Branch_Name": "Data Hub Regulatory Firewall",
        "Operational_Role": "חסימת זליגת מידע אישי מזהה והתאמה לתקני Data Hub של MOLIT",
        "Active_Agents": 15000,
        "Agent_Type": "Privacy_Firewall_Agents",
        "ID_Range": "sensor_27500 - sensor_34999 / actuator_27500 - actuator_34999",
        "Hardware_Requirement": "Secure Edge Node (CPU)",
        "Execution_Command": "python /app/agent_worker.py --branch ZRH --sub PRIV-02"
    },
    {
        "Branch_ID": "THALAMUS-CORE",
        "Sub_Branch_ID": "THALAMUS-CORE-GLOBAL",
        "Sub_Branch_Name": "Deterministic Micro-Decision Thalamus",
        "Operational_Role": "גישור וניתוב קלטים בינאריים בזמן אמת ללא השהייה וללא תלות בעיבוד מרכזי",
        "Active_Agents": 0,
        "Agent_Type": "Deterministic_Core_Router",
        "ID_Range": "N/A",
        "Hardware_Requirement": "Embedded CPU Bridge",
        "Execution_Command": "python /app/neuron_city_bridge.py"
    }
]


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
            "target_system": "AUH-GOV-API-01" if is_critical else "LOGGING_LEDGER",
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
        print(f"\n⚡ [Neural Impulse Triggered] Routing embedding {embedding.id[:8]} from {embedding.source_branch}/{embedding.source_sub}...")

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
    print("=" * 80)
    print("    OPERATION NEURON CITY: THALAMUS IMPLANT - GLOBAL MULTI-BRANCH SIMULATION")
    print("=" * 80)
    print(f"Loaded {len(WGI_BRANCH_TOPOLOGY)} WGI Network Topology Branches successfully.\n")

    # Initialize the systems
    thalamus = SL0000Thalamus(noise_threshold=0.65)
    wego_bridge = WeGOMENAProtocolBridge(thalamus)

    # Scenario 1: Robot error in SEL-MOB-SUWON-01 (Suwon Base Physical AI)
    print("\n--- SCENARIO 1: ROBOT ERROR IN SEOUL (SEL-MOB-SUWON-01) -> ACTUATE ABU DHABI ---")
    seoul_error_embedding = Embedding(
        vector=[0.98, -0.12, 0.45, 0.88, 0.01],
        source_branch="SEL-MOB",
        source_sub="SUWON-01",
        payload_metadata={
            "event_type": "robot_error",
            "severity": 0.95,
            "location": "Suwon Base Assembly Sector G",
            "recommended_remedy": "ENGAGE_HYUNDAI_EMERGENCY_STOP_ABU_DHABI"
        }
    )

    try:
        # Expected to complete in ~10-25ms (well below 100ms)
        propagation_result = wego_bridge.route_signal(seoul_error_embedding, simulate_network_delay=0.01) # 10ms network delay
        decision = propagation_result["thalamus_decision"]

        print("\n🤖 [Hyundai Robots / Abu Dhabi Motor Cortex Actuation via AUH-GOV-API-01]")
        if decision["decision"] == "ACTUATE_IMMEDIATELY":
            print(f"💥 ACTION EXECUTED: Translating decision to Abu Dhabi Robot controllers.")
            print(f"👉 TARGET COGNITIVE NODE: {decision['target_system']}")
            print(f"👉 COMMAND SENT: {decision['action_command']}")
            print("🟢 STATUS: Abu Dhabi assembly system safely locked/re-routed.")
        else:
            print("⚪ STATUS: No emergency action required.")

    except LatencyExceededError as e:
        print(e)

    # Scenario 2: Routine Traffic in Seongnam ADL Healthcare (Filtered out by Thalamus "Fire > Traffic" Rule 3)
    print("\n--- SCENARIO 2: ROUTINE TELEMETRY (SEL-MOB-SNG-02) -> NO ACTION (FILTER NOISE) ---")
    seoul_routine_embedding = Embedding(
        vector=[0.11, 0.05, -0.02, 0.04, 0.12],
        source_branch="SEL-MOB",
        source_sub="SNG-02",
        payload_metadata={
            "event_type": "routine_traffic",
            "severity": 0.15,
            "location": "Seongnam Complex ADL monitor 14",
            "recommended_remedy": "LOG_ROUTINE_FLOW"
        }
    )

    propagation_result = wego_bridge.route_signal(seoul_routine_embedding, simulate_network_delay=0.005)
    decision = propagation_result["thalamus_decision"]
    print(f"Thalamus Decision Priority: {decision['priority']}")
    print(f"Action Code: {decision['decision']}")
    print(f"Routed To: {decision['target_system']}")
    print("🟢 STATUS: Noise successfully filtered out. Zero urban desensitization.")

    # Scenario 3: Hard Null Check Failure (Simulated fiber-optic drop / delay > 100ms)
    print("\n--- SCENARIO 3: NETWORK DEGRADATION (HARD_NULL_CHECK EXCEPTION TRIGGERED) ---")
    delayed_embedding = Embedding(
        vector=[0.99, -0.11, 0.44, 0.89, 0.02],
        source_branch="SEL-MOB",
        source_sub="PUSAN-03",
        payload_metadata={
            "event_type": "robot_error",
            "severity": 0.95,
            "location": "Busan Centum AX",
            "recommended_remedy": "HALT_CRITICAL_CONVEYOR_BELT"
        }
    )

    try:
        # Simulate network delay of 120ms (exceeding 100ms limit)
        wego_bridge.route_signal(delayed_embedding, simulate_network_delay=0.12)
    except LatencyExceededError as e:
        print(f"\n❌ EXCEPTION CAUGHT SUCCESSFULLY as part of safety guarantees:")
        print(f"{e}")
        print("🛡️ Safety protocols successfully engaged: Prevented stale/delayed decision execution in Abu Dhabi.")

    print("\n" + "=" * 80)
    print("    OPERATION NEURON CITY: SYSTEM DEMO COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    run_simulation()
