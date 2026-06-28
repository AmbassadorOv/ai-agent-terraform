from jules_sanitizer.ontological_sanitizer import JulesOntologicalSanitizer

def main():
    print("--- [ JULES ONTOLOGICAL SANITIZER DEPLOYMENT ] ---")
    sanitizer = JulesOntologicalSanitizer()
    result = sanitizer.scan_and_clean(".")
    print(f"\n[FINAL STATUS] {result}")

if __name__ == "__main__":
    main()
