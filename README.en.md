# Tguan Rehabilitation Skills

[Simplified Chinese](README.md) | English

> Let real rehabilitation work be seen instead of buried.

[![Version](https://img.shields.io/badge/version-0.2.2-17352D.svg?style=flat-square)](VERSION)

This public bundle helps rehabilitation practitioners amplify their existing evidence-based, service, and operating judgment with AI. It does not replace professional judgment, clinical responsibility, or business decisions.

The first run does not require a knowledge base, client archive, standardized business spreadsheet, or system adapter. A newly installed WorkBuddy user can start with one source, one de-identified verbal account, or a few numbers with known provenance.

Version 0.2.2 contains seven Skills:

- `/tiguan-rehab`: one guided front door that identifies the highest need, inspects available material, and starts the fastest relevant path;
- `/tiguan-source-to-practice`: ask the user to explain first, then compare that explanation with the source before teaching or planning a verification;
- `/tiguan-practice-knowledge-base`: start the first reusable entry from the current conversation; no existing knowledge base is required;
- `/tiguan-assessment-session-design`: upload your own questionnaire once, then turn de-identified answers into pre-session preparation;
- `/tiguan-service-ops`: turn one de-identified session account into a professional record draft, client take-home explanation, and next-session focus; use an adapter only after explicit confirmation;
- `/tiguan-post-session-questioning`: start from a de-identified archive, transcript, or after-the-fact account and conduct evidence-led, multi-turn questioning;
- `/tiguan-business-review`: create a minimum seven-day collection sheet when no data exists; with de-identified data, separate cash, delivered revenue, prepaid service obligations, owner-wage targets, capacity, and funnel metrics without treating missing data as zero.

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
