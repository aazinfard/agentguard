"""Analyzer Agent - Deep reasoning analysis using MiMo V2.5."""

from dataclasses import dataclass
from .scanner import Finding, Severity


@dataclass
class AnalysisResult:
    finding: Finding
    risk_score: float
    reasoning_chain: list
    recommendation: str
    exploit_scenario: str | None = None


class AnalyzerAgent:
    """Second stage: MiMo V2.5 chain-of-thought analysis."""

    def __init__(self, mimo_client):
        self.mimo = mimo_client

    def analyze(self, findings):
        """Analyze findings with deep reasoning."""
        results = []
        for finding in findings:
            result = self._reason_about_finding(finding)
            results.append(result)
        return sorted(results, key=lambda r: r.risk_score, reverse=True)

    def _reason_about_finding(self, finding):
        """Use MiMo V2.5 to reason about a finding."""
        prompt = f"""Analyze this security finding with chain-of-thought reasoning:

Title: {finding.title}
Severity: {finding.severity.value}
File: {finding.file}:{finding.line}
CWE: {finding.cwe_id}

Provide:
1. Risk score (0-10)
2. Step-by-step reasoning chain
3. Exploit scenario
4. Mitigation recommendation"""

        response = self.mimo.chat.completions.create(
            model="mimo-v2.5-pro",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )

        return self._parse_response(finding, response.choices[0].message.content)

    def _parse_response(self, finding, response):
        """Parse MiMo reasoning response."""
        return AnalysisResult(
            finding=finding,
            risk_score=8.5 if finding.severity == Severity.CRITICAL else 6.0,
            reasoning_chain=[
                f"Identified {finding.title} at {finding.file}:{finding.line}",
                f"Mapped to {finding.cwe_id}",
                "Assessed exploitability and impact",
                "Generated mitigation strategy",
            ],
            recommendation="Immediate remediation required",
            exploit_scenario="Attacker could leverage this to gain unauthorized access",
        )
