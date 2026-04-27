import os
from rules import SIGNATURES


def scan_file(file_path):
    findings = []
    categories_found = set()
    file_score = 0

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            content = file.read()
    except Exception:
        return None

    # Skip very large files to reduce noise and improve performance
    if len(content) > 200_000:
        return None

    for category, rule in SIGNATURES.items():
        severity = rule["severity"]

        for pattern in rule["patterns"]:
            if pattern in content:
                findings.append({
                    "category": category,
                    "pattern": pattern,
                    "severity": severity
                })

                if category not in categories_found:
                    categories_found.add(category)
                    file_score += severity

    if not findings:
        return None

    # Multi-signal risk bonuses
    if len(categories_found) >= 2:
        file_score += 15

    if "obfuscation" in categories_found and "command_execution" in categories_found:
        file_score += 25

    if "network_activity" in categories_found and "command_execution" in categories_found:
        file_score += 20

    if "destructive_action" in categories_found:
        file_score += 20

    # More realistic suspicious behavior combination
    if "import socket" in content and "subprocess" in content:
        file_score += 20

    file_score = min(file_score, 100)

    return {
        "file": file_path,
        "score": file_score,
        "categories": list(categories_found),
        "findings": findings
    }


def scan_folder(folder_path):
    results = []
    total_files = 0

    ignored_dirs = [
        ".git",
        "__pycache__",
        "venv",
        ".venv",
        "node_modules",
        "tests",
        "test",
        "docs",
        "doc",
        "examples",
        "example"
    ]

    ignored_files = [
        "rules.py",
        "risk_score.py"
    ]

    ignored_extensions = [
        ".md",
        ".txt",
        ".rst",
        ".json",
        ".toml",
        ".yaml",
        ".yml",
        ".lock",
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".svg",
        ".ico",
        ".pdf"
    ]

    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if d not in ignored_dirs]

        for filename in files:
            if filename in ignored_files:
                continue

            _, extension = os.path.splitext(filename)

            if extension in ignored_extensions:
                continue

            total_files += 1

            file_path = os.path.join(root, filename)
            result = scan_file(file_path)

            if result:
                results.append(result)

    return results, total_files