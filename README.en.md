# Tguan Rehabilitation Skills

[Simplified Chinese](README.md) | English

> Let real rehabilitation work be seen instead of buried.

[![Version](https://img.shields.io/badge/version-0.2.0-17352D.svg?style=flat-square)](VERSION)

This public bundle helps rehabilitation practitioners amplify their existing evidence-based, service, and operating judgment with AI. It does not replace professional judgment, clinical responsibility, or business decisions.

Version 0.2.0 contains seven Skills:

- `/tiguan-rehab`: one guided front door that identifies the highest need, inspects available material, and starts the fastest relevant path;
- `/tiguan-source-to-practice`: turn source material into one verifiable practice action;
- `/tiguan-practice-knowledge-base`: preserve provenance, judgment, and verification status;
- `/tiguan-assessment-session-design`: upload your own questionnaire once, then turn de-identified answers into pre-session preparation;
- `/tiguan-service-ops`: preview appointment, record, checkout, and follow-up state changes, then use an existing adapter only after explicit confirmation;
- `/tiguan-post-session-questioning`: conduct evidence-led, multi-turn questioning rather than producing a one-shot report;
- `/tiguan-business-review`: calculate de-identified funnel metrics without treating missing data as zero.

The built-in questionnaire is only a starter. A PDF is optional, not the default success criterion.

## Installation

WorkBuddy on macOS:

```bash
curl -fsSL https://raw.githubusercontent.com/Bbaozizz/tiguan-rehab-skills/main/tools/install-workbuddy.sh | bash
```

WorkBuddy on Windows PowerShell:

```powershell
irm https://raw.githubusercontent.com/Bbaozizz/tiguan-rehab-skills/main/tools/install-workbuddy.ps1 | iex
```

Other Agent Skills-compatible tools:

```bash
npx -y skills add Bbaozizz/tiguan-rehab-skills -g --all
```

After installation, start with `/tiguan-rehab Help me find the most important problem to solve first.` The router asks one question at a time, matches the highest need with material already available, and continues into the selected Skill without making the user re-enter context.

Use synthetic or de-identified inputs. No Skill diagnoses, prescribes, selects dosage or progression, or silently performs client-facing and business writes. See the [Chinese README](README.md) and [getting started guide](docs/getting-started.md) for the complete workflow and boundaries.

## License

[CC BY-NC 4.0](LICENSE). Commercial use requires separate permission.
