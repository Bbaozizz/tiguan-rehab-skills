# Tguan Rehabilitation Skills

[Simplified Chinese](README.md) | English

> Let real rehabilitation work be seen instead of buried.

[![Version](https://img.shields.io/badge/version-0.1.2-17352D.svg?style=flat-square)](VERSION)
[![skills.sh](https://skills.sh/b/Bbaozizz/tiguan-rehab-skills)](https://skills.sh/Bbaozizz/tiguan-rehab-skills)
[![License](https://img.shields.io/badge/license-CC%20BY--NC%204.0-B1462F.svg?style=flat-square)](LICENSE)

**Supports WorkBuddy (verified locally on macOS; native PowerShell installer and CI for Windows), Claude Code, Codex, and other Agent Skills-compatible tools.**

Created by [Tguan Rehabilitation](https://tiguanrehab.cn/), this public Skill collection is designed for rehabilitation students, therapists working in hospitals or organizations, solo practitioners, and organization leaders. AI supports expression, documentation, analysis, operations, and review; it does not replace professional judgment, clinical responsibility, or organizational decisions.

Two Skills are downloadable today. The broader capability map below is a roadmap: planned capabilities will be designed, tested, and released progressively, but are not presented as currently available.

## Long-term capability map

The collection is organized around recurring cognitive shifts rather than output formats or workflow steps:

| Capability cluster | Intended shift | Main scope |
| --- | --- | --- |
| Practice calibration | From self-perception to evidence about the actual knowledge-action gap | Learning, onboarding, session review, supervised practice, role transitions |
| Verifiable service design | From stacking tests and interventions to goal, baseline, hypothesis, retest, and stage decisions | Client contact, assessment, planning, treatment, follow-up, reassessment, completion or referral |
| Professional value visibility | From treating communication as packaging to making real judgment and evidence understandable | Client communication, team collaboration, case explanation, public content |
| Practice-system diagnosis | From blaming every problem on technique, traffic, or execution to locating the actual system break | Solo practice, studio operations, organizational collaboration, quality management |

One stage does not automatically become one Skill. Questionnaires, reports, notices, homework cards, and other output formats remain modes or resources inside a deeper capability. Role differences remain branches. Deterministic integrations remain scripts or optional adapters. A new public Skill is added only when it owns a distinct recurring task, a distinct core judgment, and an independently testable cognitive shift.

## What is included

- `/tiguan-rehab`: onboarding and context-aware routing to released Skills.
- `/tiguan-assessment-session-design`: turns de-identified context into an assessment-session brief, client-understandable baseline, retest structure, one real-life action, a follow-up draft, and a printable report.

Planned practice-calibration, longitudinal service-design, professional-visibility, and practice-system capabilities are roadmap items, not downloadable capabilities. The router only invokes released Skills.

## Roadmap

| Capability | Status |
| --- | --- |
| Unified entry, installation, documentation, build, CI, and release path | Released |
| Assessment-session design | Released |
| Practice calibration | Planned |
| Longitudinal verifiable-service capabilities | Planned |
| Professional value visibility | Planned |
| Practice-system diagnosis | Planned |

Every future Skill must define its cognitive problem, role and trigger context, synthetic or de-identified test cases, privacy and clinical boundaries, failure handling, and an independent installation and real-task evaluation path.

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
