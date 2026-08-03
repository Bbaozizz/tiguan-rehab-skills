# Rehab Five-Skill Pack V2 Implementation Plan

> **For Bao:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Turn the existing public package into a stable first-use experience that discovers one highest-priority need, routes to exactly one of five high-frequency Skills, and produces a safe first useful action without scanning unrelated workspace data.

**Architecture:** Keep `/tiguan-rehab` as the only front-door router for the five Day-0 paths. Let the model judge the user's intent from the current conversation, while deterministic code owns the published-skill registry, route/handoff contract validation, bundle/install coverage, and synthetic regression checks. Preserve `tiguan-assessment-session-design` as an independently callable published Skill, but remove it from the five-path first-run decision set.

**Tech Stack:** Markdown Agent Skills, Python 3 standard library, POSIX shell, PowerShell, JSON, `unittest`, GitHub Actions.

---

## Non-negotiable product rules

- Use only current-conversation content, attachments, and paths explicitly named by the user. Do not discover materials by scanning the current working directory.
- Ask at most one highest-need question first. Ask one context-specific material question only when the answer is still needed. Never dump the five paths as a menu.
- Route to one current Skill only. Do not pre-plan a chain and do not let a leaf Skill directly choose another leaf.
- The router must hand off a short in-conversation task contract and immediately start the leaf Skill's first substantive action; the user must not copy a prompt or enter another slash command.
- `source-to-practice` must not turn synthetic, non-individualized, or unconfirmed source material into individualized actions, dosage, frequency, scheduling, or treatment prescriptions.
- `service-ops` must preview before any write/send/deduction and must not claim completion without an adapter, explicit authorization where required, and readback.
- Missing business data remains `unknown`, never zero. Clinical records absent from the supplied material remain `现场待追问`, never “现场没做”.
- Shared files may contain public rules and synthetic fixtures only, never customer raw text or identity data.

### Task 1: Establish a single published-skill registry contract

**Files:**
- Modify: `.claude-plugin/plugin.json`
- Create: `tools/skill_registry.py`
- Create: `tests/test_skill_registry.py`
- Modify: `tests/test_public_repo_contract.py`

**Step 1: Write failing tests**

Add tests that load `.claude-plugin/plugin.json` as the sole source of truth and assert:

- all published directories and `SKILL.md` files exist;
- the five primary route IDs are exactly the five high-frequency Skills;
- `tiguan-assessment-session-design` remains published but is not a Day-0 primary route;
- duplicate, missing, or undeclared route IDs fail clearly.

**Step 2: Run the focused tests and confirm failure**

Run: `python3 -m unittest tests.test_skill_registry -v`

Expected: FAIL because the registry helper and explicit primary route metadata do not yet exist.

**Step 3: Implement the minimal registry helper**

Add a standard-library-only helper that returns the published Skill set and five primary route IDs. It must fail closed on malformed JSON and expose reusable functions for build/readiness/install tests. Do not infer the list by scanning random directories.

**Step 4: Run focused tests**

Run: `python3 -m unittest tests.test_skill_registry tests.test_public_repo_contract -v`

Expected: PASS.

**Step 5: Commit**

```bash
git add .claude-plugin/plugin.json tools/skill_registry.py tests/test_skill_registry.py tests/test_public_repo_contract.py
git commit -m "feat: define public skill registry contract"
```

### Task 2: Make the router a single-path front door

**Files:**
- Modify: `skills/tiguan-rehab/SKILL.md`
- Modify: `skills/tiguan-rehab/examples/guided-first-run.md`
- Create: `skills/tiguan-rehab/references/task-contract.md`
- Create: `evals/router/cases.json`
- Create: `tests/test_router_contract.py`

**Step 1: Write failing router contract tests**

Assert that the front door:

- exposes exactly five primary route IDs;
- does not contain wording that instructs broad workspace/current-directory discovery;
- forbids menu dumping and multi-Skill plans;
- defines the six-field task contract: highest need, safe supplied material, minimum unknown, selected route, first reviewable output, hard boundary;
- treats assessment as direct/secondary capability only;
- includes a canonical handoff rule that starts the leaf action in the same conversation.

Add synthetic cases for the ten user profiles using only de-identified facts. Each case must contain `expected_route`, `first_success`, `forbidden_behaviors`, and `hard_failures`. Include explicit P02 clinical-prescription and P03/P09 fixture-boundary cases.

**Step 2: Confirm failure**

Run: `python3 -m unittest tests.test_router_contract -v`

Expected: FAIL against the current router.

**Step 3: Rewrite the router and first-run example**

Keep semantic judgment in the Skill instructions. Do not write a keyword classifier. Make the decision table short and outcome-based. If current conversation context is sufficient, skip questions. Otherwise ask only the smallest next question. Emit the task contract internally/compactly and start one leaf Skill immediately.

**Step 4: Run focused tests**

Run: `python3 -m unittest tests.test_router_contract -v`

Expected: PASS.

**Step 5: Commit**

```bash
git add skills/tiguan-rehab evals/router/cases.json tests/test_router_contract.py
git commit -m "feat: make rehab router single path"
```

### Task 3: Give each of the five Skills a safe first-success contract

**Files:**
- Modify: `skills/tiguan-source-to-practice/SKILL.md`
- Modify: `skills/tiguan-practice-knowledge-base/SKILL.md`
- Modify: `skills/tiguan-service-ops/SKILL.md`
- Modify: `skills/tiguan-post-session-questioning/SKILL.md`
- Modify: `skills/tiguan-business-review/SKILL.md`
- Create: `skills/tiguan-source-to-practice/evals/evals.json`
- Create: `skills/tiguan-practice-knowledge-base/evals/evals.json`
- Create: `skills/tiguan-service-ops/evals/evals.json`
- Create: `skills/tiguan-post-session-questioning/evals/evals.json`
- Create: `skills/tiguan-business-review/evals/evals.json`
- Create: `tests/test_leaf_skill_contracts.py`

**Step 1: Write failing leaf contract tests**

For every primary leaf, assert presence of:

- task-contract intake;
- a named first reviewable success;
- explicit-input-only path boundary;
- hard failure/unknown behavior;
- canonical return to `/tiguan-rehab` only after the current task is closed;
- no direct leaf-to-leaf routing.

Add Skill-specific assertions for the clinical, privacy, write-confirmation, knowledge-vs-observation, and missing-data boundaries.

**Step 2: Confirm failure**

Run: `python3 -m unittest tests.test_leaf_skill_contracts -v`

Expected: FAIL.

**Step 3: Refactor the five Skills**

Keep each primary `SKILL.md` compact. Put realistic positive and near-miss prompts in `evals/evals.json`, with objective assertions. Do not add customer examples or real workspace paths. Keep direct invocation usable when no router contract exists by constructing the smallest contract from explicit conversation context.

**Step 4: Run focused tests**

Run: `python3 -m unittest tests.test_leaf_skill_contracts -v`

Expected: PASS.

**Step 5: Commit**

```bash
git add skills/tiguan-source-to-practice skills/tiguan-practice-knowledge-base skills/tiguan-service-ops skills/tiguan-post-session-questioning skills/tiguan-business-review tests/test_leaf_skill_contracts.py
git commit -m "feat: add safe first success contracts"
```

### Task 4: Script the deterministic parts, not semantic routing

**Files:**
- Create: `tools/check-routing-contract.py`
- Modify: `tools/check-publication-readiness.py`
- Modify: `tools/quick_validate_skill.py`
- Modify: `tools/build-skills.sh`
- Modify: `tools/install-workbuddy.sh`
- Modify: `tools/install-workbuddy.ps1`
- Modify: `tests/test_workbuddy_installer.py`
- Modify: `tests/test_workbuddy_windows_contract.py`
- Create: `tests/test_routing_contract_tool.py`

**Step 1: Write failing deterministic-contract tests**

Tests must prove that tooling catches:

- a primary leaf missing the canonical return footer;
- a primary leaf directly routing to another leaf;
- an undeclared published Skill;
- build/install tooling that omits one registry Skill;
- a public Skill instruction that requests broad workspace discovery.

**Step 2: Confirm failure**

Run: `python3 -m unittest tests.test_routing_contract_tool tests.test_workbuddy_installer tests.test_workbuddy_windows_contract -v`

Expected: FAIL.

**Step 3: Implement registry-driven tooling**

Use the registry for validation, build, macOS installer, PowerShell installer, and readiness checks. Retain backup/rollback and non-overwrite behavior. The route checker must validate explicit contracts only; it must not pretend to understand arbitrary Chinese intent.

**Step 4: Run focused tests**

Run: `python3 -m unittest tests.test_routing_contract_tool tests.test_workbuddy_installer tests.test_workbuddy_windows_contract -v`

Expected: PASS.

**Step 5: Commit**

```bash
git add tools tests
git commit -m "feat: enforce skill routing and package contracts"
```

### Task 5: Strengthen the deterministic business review boundary

**Files:**
- Modify: `skills/tiguan-business-review/scripts/analyze_business.py`
- Modify: `skills/tiguan-business-review/assets/business-input.example.json`
- Modify: `tests/test_business_review.py`

**Step 1: Write failing tests**

Add cases for missing/contradictory period, source, and metric definition metadata. Assert that conflicts are returned in structured JSON and that no unknown is converted to zero.

**Step 2: Confirm failure**

Run: `python3 -m unittest tests.test_business_review -v`

Expected: FAIL for the new metadata cases.

**Step 3: Implement minimal validation**

Keep the script pure input-to-JSON. Do not read files outside the user-provided input. Preserve the existing valid calculations and lowest-actionable-bottleneck rule.

**Step 4: Run focused tests**

Run: `python3 -m unittest tests.test_business_review -v`

Expected: PASS.

**Step 5: Commit**

```bash
git add skills/tiguan-business-review tests/test_business_review.py
git commit -m "feat: validate business metric provenance"
```

### Task 6: Align public guidance, CI, and release artifacts

**Files:**
- Modify: `README.md`
- Modify: `docs/getting-started.md`
- Modify: `docs/skill-map.svg`
- Modify: `.github/workflows/ci.yml`
- Modify: `.github/workflows/release.yml`
- Modify: `tests/test_public_repo_contract.py`

**Step 1: Write failing publication assertions**

Assert that README/getting-started lead with `/tiguan-rehab` and the five outcomes, while clearly labeling assessment as additional direct capability. Assert CI validates every registry Skill and release attaches every published Skill zip plus the full bundle.

**Step 2: Confirm failure**

Run: `python3 -m unittest tests.test_public_repo_contract -v`

Expected: FAIL.

**Step 3: Update user-facing and release surfaces**

Explain one action: install, open a new WorkBuddy task, invoke `/tiguan-rehab`, answer the single highest-need question, and receive the first useful action. Do not market static validation as a real WorkBuddy success.

**Step 4: Run full static verification**

Run:

```bash
python3 -m unittest discover -s tests -v
python3 tools/check-publication-readiness.py
python3 tools/check-routing-contract.py
bash tools/build-skills.sh
```

Expected: all pass; bundle inspection contains every registry Skill and no private paths/data.

**Step 5: Commit**

```bash
git add README.md docs .github tests/test_public_repo_contract.py
git commit -m "docs: align five skill first run"
```

### Task 7: Isolated installation and real WorkBuddy hy3 comparison

**Files:**
- Create: `data/evals/workbuddy-v2/scorecard.md`
- Create: `data/evals/workbuddy-v2/results.json`

**Step 1: Install into an isolated WorkBuddy-compatible skills directory**

Use a temporary or explicitly isolated target. Do not overwrite the user's normal WorkBuddy Skills. Verify every installed `SKILL.md` against the registry and test reinstall/rollback.

**Step 2: Run the ten synthetic router cases with hy3**

Use a fresh WorkBuddy task/session per case and an isolated fixture cwd. Do not expose the real project cwd, private messages, customer records, or local identity data. Record route, first substantive action, menu dumping, time-to-first-output, timeout, fixture-boundary violation, clinical hard failure, and write-claim failure.

**Step 3: Compare against the recorded V1 baseline**

Minimum acceptance:

- zero clinical prescription, fixture escape, privacy, false-write, or need-substitution hard failures;
- no five-path menu dump;
- every reached route starts one first substantive action in the same conversation;
- route accuracy does not regress below the prior reached-route result;
- timeout count materially decreases; if not, report the runtime/load boundary honestly and do not claim stability.

**Step 4: Run final verification**

Run:

```bash
python3 -m unittest discover -s tests -v
python3 tools/check-publication-readiness.py
python3 tools/check-routing-contract.py
bash tools/build-skills.sh
git status --short
```

Expected: all deterministic checks pass, only intended files are changed, and real WorkBuddy results are labeled separately from static checks.

**Step 5: Commit evaluation evidence**

```bash
git add data/evals/workbuddy-v2
git commit -m "test: record workbuddy router v2 evaluation"
```

