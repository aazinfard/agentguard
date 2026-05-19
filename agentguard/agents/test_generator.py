"""Test Generator Agent - Creates security test cases from findings."""

from dataclasses import dataclass
from .scanner import Finding


@dataclass
class SecurityTest:
    name: str
    description: str
    code: str
    framework: str = "pytest"
    finding_ref: str = ""


class TestGeneratorAgent:
    """Third stage: generate security test cases."""

    def generate(self, findings, framework="pytest"):
        """Generate security test cases from findings."""
        tests = []
        for finding in findings:
            tests.append(SecurityTest(
                name=f"test_{finding.title.lower().replace(' ', '_')}",
                description=f"Security test for: {finding.title}",
                code=f"def test_{finding.title.lower().replace(' ', '_')}():\n    pass",
                framework=framework,
                finding_ref=f"{finding.file}:{finding.line}",
            ))
        return tests
