import os
from rules import SIGNATURES


MAX_FILE_SIZE = 200_000


IGNORED_DIRS = [
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
    "example",
    "dist",
    "build"
]

IGNORED_FILES = [
    "rules.py",
    "risk_score.py"
]

IGNORED_EXTENSIONS = [
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
    ".pdf",
    ".zip",
    ".tar",
    ".gz",
    ".7z",
    ".mp4",
    ".mp3"
]


def normalize_path(path):
    return str(path).replace("\\", "/")


def scan_file(file_path):
    findings = []
    categories_found = set()
    file_score = 0

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            content = file.read()
    except Exception:
        return None

    if len(content) > MAX_FILE_SIZE:
        return None

    normalized_file_path = normalize_path(file_path)

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

    has_strong_obfuscation = any(
        finding["pattern"] in ["base64.b64decode(", "marshal.loads("]
        for finding in findings
    )

    if len(categories_found) >= 3:
        file_score += 10

    if "obfuscation" in categories_found and "command_execution" in categories_found:
        if has_strong_obfuscation:
            file_score += 25

    if "network_activity" in categories_found and "command_execution" in categories_found:
        file_score += 20

    if "destructive_action" in categories_found and len(categories_found) >= 2:
        file_score += 15

    if "persistence" in categories_found and "command_execution" in categories_found:
        file_score += 20

    if "import socket" in content and "subprocess" in content:
        file_score += 20

    if "flask" in normalized_file_path and "SECRET_KEY" in content:
        file_score -= 10

    if file_score < 0:
        file_score = 0

    file_score = min(file_score, 100)

    return {
        "file": normalized_file_path,
        "score": file_score,
        "categories": sorted(list(categories_found)),
        "findings": findings
    }


def scan_folder(folder_path):
    results = []
    total_files = 0
    skipped_files = 0

    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for filename in files:
            if filename in IGNORED_FILES:
                skipped_files += 1
                continue

            _, extension = os.path.splitext(filename)

            if extension.lower() in IGNORED_EXTENSIONS:
                skipped_files += 1
                continue

            total_files += 1

            file_path = os.path.join(root, filename)
            result = scan_file(file_path)

            if result:
                results.append(result)

    return results, total_files, skipped_files