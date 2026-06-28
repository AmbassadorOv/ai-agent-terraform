from molad import Molad
from julius_time_kernel import TimeKernel
from jules_agent_factory import JulesAgentFactory

def run_demo():
    print("--- INITIALIZING JULIUS AGENT FACTORY ---")

    # 1. Initialize Kernel and Factory
    kernel = TimeKernel()
    factory = JulesAgentFactory(kernel)

    # 2. Sanctify Time (Required for factory operations)
    initial_molad = Molad(day=2, hour=5, part=204)
    kernel.sanctify(initial_molad)

    # 3. Create a Sovereign Agent
    print("\n--- STEP 1: AGENT CREATION ---")
    agent = factory.create_sovereign_agent("001-Exodus")
    print(f"Created Agent Spec: {agent}")

    # 4. Audit Network Entities
    print("\n--- STEP 2: NETWORK AUDIT ---")
    entities_found = [
        {"name": "Pharaoh_Shadow", "has_place": False},
        {"name": "MyClip_Ghost", "has_place": False},
        {"name": "Sanctified_Node", "has_place": True}
    ]
    factory.network_audit_logic(entities_found)

    # 5. Darkness Equation
    print("\n--- STEP 3: DARKNESS ANALYSIS ---")
    L = 1000 # Latent Complexity
    A_I = 714 # Alignment Integrity
    factory.calculate_darkness(L, A_I)

    print("\n--- DEMO COMPLETE ---")

if __name__ == "__main__":
    run_demo()
