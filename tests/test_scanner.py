"""Tests for the Scanner Agent."""

import pytest
from pathlib import Path
from agentguard.agents.scanner import ScannerAgent, Severity


class TestScannerAgent:
    def test_init_defaults(self):
        agent = ScannerAgent()
        assert ".py" in agent.extensions
        assert ".js" in agent.extensions

    def test_init_custom_extensions(self):
        agent = ScannerAgent(extensions=[".sol"])
        assert agent.extensions == [".sol"]

    def test_scan_empty_dir(self, tmp_path):
        agent = ScannerAgent()
        findings = agent.scan(tmp_path)
        assert findings == []

    def test_scan_python_with_vuln(self, tmp_path):
        vuln_file = tmp_path / "vuln.py"
        vuln_file.write_text(
            'password = "supersecret123"\n'
            'query = "SELECT * FROM users WHERE id=" + user_input\n'
        )
        agent = ScannerAgent()
        findings = agent.scan(tmp_path)
        assert len(findings) >= 1
        severities = {f.severity for f in findings}
        assert Severity.CRITICAL in severities

    def test_scan_clean_file(self, tmp_path):
        clean_file = tmp_path / "clean.py"
        clean_file.write_text("import os\ndef hello():\n    return \"world\"\n")
        agent = ScannerAgent()
        findings = agent.scan(tmp_path)
        assert len(findings) == 0
