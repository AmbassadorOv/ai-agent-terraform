import os
from molad import Molad
from julius_time_kernel import TimeKernel
from ontological_sanitizer import JulesOntologicalSanitizer
from github_manager import initialize_clean_repository

def main():
    print("--- JULIUS ONTOLOGICAL INTEGRITY SYSTEM ---")

    # 1. Initialize Kernel
    kernel = TimeKernel()

    # 2. Sanctify Time (Required for operations)
    initial_molad = Molad(day=2, hour=5, part=204)
    kernel.sanctify(initial_molad)

    # 3. Execute Sanitizer
    print("\n--- STEP 1: SCAN AND CLEAN ---")
    sanitizer = JulesOntologicalSanitizer(kernel)
    result = sanitizer.scan_and_clean(".")
    print(result)

    # 4. Initialize Clean Repository (Requires GITHUB_TOKEN environment variable)
    print("\n--- STEP 2: REPOSITORY INITIALIZATION ---")
    token = os.getenv("GITHUB_TOKEN", "YOUR_TOKEN")
    repo_name = "Ontological-Integrity-System"

    if token == "YOUR_TOKEN":
        print("[!] Skipping GitHub repository creation: GITHUB_TOKEN not set.")
    else:
        repo_result = initialize_clean_repository(kernel, token, repo_name)
        print(repo_result)

    print("\n--- SYSTEM CHECK COMPLETE ---")

if __name__ == "__main__":
    main()
