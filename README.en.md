# Tguan Rehabilitation Skills

[Simplified Chinese](README.md) | English

> Public, installable workflows for rehabilitation professionals who want AI to handle structuring, documentation, presentation, and review without replacing clinical judgment or responsibility.

[![Version](https://img.shields.io/badge/version-0.1.0-17352D.svg?style=flat-square)](VERSION)
[![skills.sh](https://skills.sh/b/Bbaozizz/tiguan-rehab-skills)](https://skills.sh/Bbaozizz/tiguan-rehab-skills)
[![License](https://img.shields.io/badge/license-CC%20BY--NC%204.0-B1462F.svg?style=flat-square)](LICENSE)

**Supports WorkBuddy (verified locally on macOS; native PowerShell installer and CI for Windows), Claude Code, Codex, and other Agent Skills-compatible tools.**

## What is included

- `/tiguan-rehab`: onboarding and context-aware routing to released Skills.
- `/tiguan-assessment-session-design`: turns de-identified context into an assessment-session brief, client-understandable baseline, retest structure, one real-life action, a follow-up draft, and a printable report.

Planned post-session, progress, and studio-operations Skills are roadmap items, not downloadable capabilities.

## Installation

WorkBuddy on macOS (install or update both Skills with one command):

```bash
curl -fsSL https://raw.githubusercontent.com/Bbaozizz/tiguan-rehab-skills/main/tools/install-workbuddy.sh | bash
```

WorkBuddy on Windows (run in PowerShell; Node, Git, and WSL are not required):

```powershell
irm https://raw.githubusercontent.com/Bbaozizz/tiguan-rehab-skills/main/tools/install-workbuddy.ps1 | iex
```

This installer only manages the two Tguan directories under `~/.workbuddy/skills`. Refresh or restart WorkBuddy after installation.

For agents supported by the generic `skills` installer:

```bash
npx -y skills add Bbaozizz/tiguan-rehab-skills -g --all
```

The generic installer does not currently recognize WorkBuddy; use the dedicated command above for WorkBuddy.

For a local clone, run from the repository root:

```bash
npx -y skills add . --all
```

## Safety boundary

Use de-identified or synthetic inputs. These Skills do not diagnose, prescribe, select exercises or dosage, decide progression, send client messages, write formal records, charge, or check out sessions. A qualified rehabilitation professional remains responsible for every clinical decision and client-facing output.

See the [Chinese README](README.md) and [getting started guide](docs/getting-started.md) for the complete user journey.

## License

[CC BY-NC 4.0](LICENSE). Personal, educational, research, and noncommercial use is permitted with attribution. Commercial use requires separate permission. Real client data, private business databases, credentials, and internal operational workflows are outside this repository.
