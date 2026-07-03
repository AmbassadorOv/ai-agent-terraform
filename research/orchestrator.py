import json
import os
from typing import List, Dict, Any

def load_ledger_data(filepath: str) -> List[Dict[str, Any]]:
    """
    טוען את נתוני השיחה (Ledger) מקובץ JSON.
    """
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def orchestrate_data(data: List[Dict[str, Any]]) -> None:
    """
    מחלץ ומסדר את הנתונים לפי סדר רציף (sequence_id),
    ומכין אותם להפצה או שימוש מודולרי.
    """
    sorted_data = sorted(data, key=lambda x: x.get('sequence_id', 0))

    for block in sorted_data:
        print(f"--- [SEQUENCE ID: {block.get('sequence_id')}] ---")
        print(f"TIMESTAMP: {block.get('timestamp')}")
        print(f"CATEGORY: {block.get('category')}")
        print("DIRECTIVES:")
        for directive in block.get('directives', []):
            print(f"  -> {directive}")
        if 'code_reference' in block:
            print(f"CODE REF: {block.get('code_reference')}")
        print("\n")

def initialize_orchestrator(json_filepath: str) -> Dict[str, Any]:
    """
    פונקציית הפעלה מרכזית המשמשת נקודת כניסה ליישומים אחרים.
    """
    ledger_data = load_ledger_data(json_filepath)
    if ledger_data:
        orchestrate_data(ledger_data)
        return {
            "status": "LOADED",
            "blocks_processed": len(ledger_data),
            "state": "LOCKED_TO_LEDGER"
        }
    return {"status": "FAILED", "reason": "FILE_NOT_FOUND"}

if __name__ == "__main__":
    result = initialize_orchestrator('research/ledger_data.json')
    print(f"SYSTEM STATE: {result}")
