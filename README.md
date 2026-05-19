# 🛡️ AgentGuard

**AI-Powered Multi-Agent Code Security Scanner**

AgentGuard uses MiMo V2.5's advanced reasoning capabilities to perform deep code security analysis through a multi-agent architecture. Each agent specializes in a different aspect of security auditing, working together to find vulnerabilities that traditional scanners miss.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│                  AgentGuard Core                 │
├─────────────┬─────────────┬─────────────────────┤
│  Scanner    │  Analyzer   │  Test Generator     │
│  Agent      │  Agent      │  Agent              │
├─────────────┼─────────────┼─────────────────────┤
│ Detect      │ Deep        │ Auto-generate       │
│ vulns &     │ reasoning   │ security test       │
│ patterns    │ on findings │ cases               │
└─────────────┴─────────────┴─────────────────────┘
         │            │              │
         └────────────┼──────────────┘
                      │
              ┌───────▼───────┐
              │  MiMo V2.5    │
              │  API Engine   │
              └───────────────┘
```

## ✨ Features

- **Multi-Agent Pipeline**: Three specialized agents work in sequence
- **MiMo V2.5 Reasoning**: Chain-of-thought vulnerability detection
- **Smart Contract Auditing**: Solidity, Vyper, Move support
- **Auto Test Generation**: Security test cases from findings
- **CI/CD Integration**: GitHub Actions ready
- **Multi-Language**: Python, JavaScript, TypeScript, Go, Rust

## 🚀 Quick Start

```bash
pip install agentguard

# Scan a project
agentguard scan ./my-project

# Scan with specific agents
agentguard scan ./my-project --agents scanner,analyzer

# Generate security report
agentguard scan ./my-project --report html
```

## 📦 Installation

```bash
# From PyPI
pip install agentguard

# From source
git clone https://github.com/aazinfard/agentguard.git
cd agentguard
pip install -e .
```

## 🔧 Configuration

Create `agentguard.yaml` in your project root:

```yaml
mimo:
  api_key: ${MIMO_API_KEY}
  model: mimo-v2.5-pro

agents:
  scanner:
    enabled: true
    depth: deep
  analyzer:
    enabled: true
    chain_of_thought: true
  test_generator:
    enabled: true
    frameworks: [pytest, jest]

rules:
  severity: [critical, high, medium]
  categories: [injection, auth, crypto, access-control]
```

## 📊 Example Output

```
🛡️ AgentGuard Security Scan
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Scanning: ./src/auth/

🔍 Scanner Agent: Found 12 potential issues
🧠 Analyzer Agent: Deep reasoning on 12 findings
  ├─ Critical: 2 (SQL injection, hardcoded secret)
  ├─ High: 3 (missing auth, weak crypto, XSS)
  ├─ Medium: 4 (info disclosure, rate limiting)
  └─ Low: 3 (deprecated functions)
🧪 Test Generator: Generated 18 security test cases

📄 Report: ./agentguard-report.html
```

## 🤖 Why MiMo V2.5?

AgentGuard leverages MiMo V2.5's unique capabilities:

- **Deep Reasoning**: Chain-of-thought analysis catches multi-step vulnerabilities
- **Code Understanding**: Native code comprehension without tokenization loss
- **Context Window**: Analyze entire codebases, not just snippets
- **Speed**: Fast inference for real-time CI/CD scanning

## 📝 License

MIT License - see [LICENSE](LICENSE)
