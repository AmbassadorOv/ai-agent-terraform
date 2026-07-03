import re
import json

def extract_patterns_from_html(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Simple extraction of text segments that look like logic or patterns
        # Removing HTML tags
        clean_text = re.sub(r'<[^>]*>', ' ', content)

        # Find words with high complexity or unique structures
        words = re.findall(r'\w{5,}', clean_text)
        unique_patterns = list(set(words))[:50]

        return unique_patterns
    except Exception as e:
        return [f"ERROR: {e}"]

if __name__ == "__main__":
    gemini_patterns = extract_patterns_from_html("gemini_share.html")
    drive_patterns = extract_patterns_from_html("drive_view.html")

    context = {
        "gemini_context": gemini_patterns,
        "drive_context": drive_patterns
    }

    with open("amne-codex-jules/orchestrator/extracted_context.json", "w") as f:
        json.dump(context, f, indent=2)

    print(f"[*] EXTRACTED {len(gemini_patterns)} PATTERNS FROM GEMINI.")
    print(f"[*] EXTRACTED {len(drive_patterns)} PATTERNS FROM DRIVE.")
