import os, re, json
from pathlib import Path
from typing import Iterator, Dict, Any

AWS_KEY = re.compile(r"\bAKIA[0-9A-Z]{16}\b")
PRIVATE_KEY = re.compile(r"-----BEGIN (?:RSA|EC|DSA)? ?PRIVATE KEY-----")
GENERIC_CREDS = re.compile(r"(?i)\b(password|passwd|secret|token)\s*[:=]\s*[^ \t\n]+")

PATTERNS = {
    "aws_access_key": AWS_KEY,
    "private_key": PRIVATE_KEY,
    "generic_creds": GENERIC_CREDS,
}

TEXT_EXTS = {".py", ".sh", ".txt", ".cfg", ".ini", ".json", ".yml", ".yaml", ".env"}

def iter_text_files(root: Path) -> Iterator[Path]:
    for p in root.rglob("*"):
        if p.is_file() and (p.suffix.lower() in TEXT_EXTS or p.suffix == ""):
            yield p

def scan_file(path: Path) -> Iterator[Dict[str, Any]]:
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            for i, line in enumerate(fh, 1):
                for name, pat in PATTERNS.items():
                    if pat.search(line):
                        yield {"rule": name, "file": str(path), "line": i, "snippet": line.strip()}
    except Exception:
        return

def scan_repo(root: str) -> str:
    root_path = Path(root)
    findings = [f for p in iter_text_files(root_path) for f in scan_file(p)]
    return json.dumps({"count": len(findings), "findings": findings}, indent=2)

# Example:
# print(scan_repo("."))
