import json
import os
import sys

def validate_parameters(params: dict) -> bool:
    """
    בדיקת עמידה בתנאי הסף של שער ה-BRST למניעת הטיות או פרשנות הסתברותית.
    """
    if params.get("entropy_allowance", 1.0) > 0.0:
        print("Error: Entropy detected. Validation failed.", file=sys.stderr)
        return False
    if params.get("validation_criteria") != "deterministic_logic_only":
        print("Error: Invalid validation criteria.", file=sys.stderr)
        return False
    return True

def compile_templates(params: dict):
    """
    מיפוי ערכי ה-JSON אל תוך תגי ה-LaTeX הקיימים בתבניות.
    """
    mapping = {
        "<TITLE>": params.get("title", ""),
        "<OBJECTIVE>": params.get("objective", ""),
        "<SCOPE>": params.get("scope", ""),
        "<METHODOLOGY>": params.get("methodology", ""),
        "<INCLUSION>": params.get("inclusion_criteria", ""),
        "<EXCLUSION>": params.get("exclusion_criteria", ""),
        "<DELIVERABLES>": params.get("deliverables", ""),
        "<CONSTRAINTS>": params.get("constraints", ""),
        "<METRICS>": params.get("evaluation_metrics", ""),
        "<TONE>": params.get("tone", ""),
        "<LENGTH_FORMAT>": params.get("length_format", "")
    }

    # עיבוד רשימות עבור תבניות ה-LaTeX
    rq_list = params.get("research_questions", [])
    rq_formatted = " \\\\ \n".join([f"\\item {rq}" for rq in rq_list])
    mapping["<RQ1>; <RQ2>; <RQ3>"] = rq_formatted
    mapping["<RQ1>"] = rq_list[0] if len(rq_list) > 0 else ""
    mapping["<RQ2>"] = rq_list[1] if len(rq_list) > 1 else ""

    mapping["<DATA_SOURCES>"] = ", ".join(params.get("data_sources", []))
    mapping["<List data sources and access details>"] = ", ".join(params.get("data_sources", []))
    mapping["<EXTRACTION_FIELDS>"] = ", ".join(params.get("extraction_fields", []))

    # רשימת הקבצים המיועדים לעדכון
    templates = [
        "prompt_generator.tex",
        "parameters.tex",
        "extraction_list.tex",
        "research_template.tex",
        "README.tex",
        "master_index.tex"
    ]

    for template_name in templates:
        # Check in the current directory and in the research directory
        possible_paths = [template_name, os.path.join("research", template_name)]
        actual_path = None
        for path in possible_paths:
            if os.path.exists(path):
                actual_path = path
                break

        if not actual_path:
            print(f"Warning: Template '{template_name}' not found. Skipping.")
            continue

        with open(actual_path, 'r', encoding='utf-8') as f:
            content = f.read()

        for tag, val in mapping.items():
            content = content.replace(tag, str(val))

        output_name = f"gen_{template_name}"
        output_path = os.path.join("research", output_name)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully compiled {output_path}")

if __name__ == "__main__":
    param_path = "research/research_parameters.json"
    if not os.path.exists(param_path):
        print(f"Error: {param_path} not found.", file=sys.stderr)
        sys.exit(1)

    with open(param_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if validate_parameters(data):
        compile_templates(data)
        print("Compilation pipeline completed successfully.")
    else:
        sys.exit(1)
