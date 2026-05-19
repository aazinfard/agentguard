"""Scanner Agent - Detects vulnerability patterns in code."""

import re
from pathlib import Path
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Finding:
    severity: Severity
    title: str
    file: str
    line: int
    description: str
    cwe_id: str | None = None


class ScannerAgent:
    """First stage: pattern-based vulnerability detection."""

    PATTERNS = {
        Severity.CRITICAL: [
            (r"(?i)(sql|query).*\+.*(?:request|input|param)", "SQL Injection", "CWE-89"),
            (r"(?i)(?:password|secret|api.?key|token)\s*=\s*['\"][^'"]+['"]", "Hardcoded Secret", "CWE-798"),
            (r"(?i)eval\s*\(", "Code Injection via eval()", "CWE-94"),
        ],
        Severity.HIGH: [
            (r"(?i)md5\s*\(", "Weak Hash (MD5)", "CWE-328"),
            (r"(?i)(?:exec|system|popen)\s*\(", "Command Injection", "CWE-78"),
        ],
        Severity.MEDIUM: [
            (r"(?i)print\s*\(.*(?:error|exception|traceback)", "Info Disclosure in Logs", "CWE-209"),
            (r"(?i)DEBUG\s*=\s*True", "Debug Mode Enabled", "CWE-489"),
        ],
    }

    def __init__(self, extensions=None):
        self.extensions = extensions or [".py", ".js", ".ts", ".sol", ".go", ".rs"]

    def scan(self, path):
        """Scan all source files for vulnerability patterns."""
        findings = []
        for file_path in self._iter_source_files(path):
            findings.extend(self._scan_file(file_path))
        return findings

    def _iter_source_files(self, path):
        """Iterate over source files, skipping common ignore dirs."""
        ignore = {"node_modules", ".git", "__pycache__", "venv", ".venv", "dist"}
        if path.is_file():
            yield path
            return
        for p in path.rglob("*"):
            if p.is_file() and p.suffix in self.extensions:
                if not any(ignored in p.parts for ignored in ignore):
                    yield p

    def _scan_file(self, file_path):
        """Scan a single file for vulnerability patterns."""
        findings = []
        try:
            content = file_path.read_text(errors="ignore")
            lines = content.split("\n")
            for severity, patterns in self.PATTERNS.items():
                for pattern, title, cwe in patterns:
                    for i, line in enumerate(lines, 1):
                        if re.search(pattern, line):
                            findings.append(Finding(
                                severity=severity,
                                title=title,
                                file=str(file_path),
                                line=i,
                                description=f"Pattern matched: {pattern[:60]}...",
                                cwe_id=cwe,
                            ))
        except Exception:
            pass
        return findings
