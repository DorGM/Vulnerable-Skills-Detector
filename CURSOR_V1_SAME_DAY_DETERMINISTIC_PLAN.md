# V1 SAME-DAY COMPLETION PLAN — Deterministic Post-Processing Evaluation

> **Status:** This plan supersedes the previous V1 recovery/completion plan from the current blocked `P1-06` state onward.
>
> **Primary goal:** reach a valid 400-sample labeling checkpoint today without any further long scanner/LLM execution, then finish the final analysis immediately after the user returns the 400 ground-truth labels.
>
> **Scientific direction preserved:** the confirmatory experiment evaluates whether deterministic, context-aware post-processing reduces false positives from deployed agent-skill scanners while preserving genuine findings.
>
> **Critical design change:** corpus-scale native-LLM scanner profiles and external LLM evaluation are removed from the confirmatory experiment because their measured local runtime is incompatible with same-day completion.

---

# 0. Current approved starting state

The current stopped state is:

| Profile | Preserved smoke result |
|---|---:|
| SS0 `skillspector_static` | 10/10 successful |
| SS1 `skillspector_native_llm` | 10/10 successful |
| CS0 `cisco_core` | 10/10 successful |
| CS1 `cisco_behavioral` | 10/10 successful |
| CS2 `cisco_native_llm` | 10/10 successful |
| CS3 `cisco_native_full` | 0 completed |
| Pilot | not started |
| Full | not started |

Additional confirmed facts:

- SS1 smoke alone required roughly one hour for 10 Skills and is too expensive for corpus-scale execution.
- Smoke/pilot/full currently use separate result trees and would duplicate work.
- Strict UTF-8 subprocess decoding can fail on scanner stdout/stderr byte `0x97`.
- Protected V0/baseline work must remain unchanged.
- The full committed SS0 and CS1 baseline outputs remain the populations used by the confirmatory experiment, subject to integrity validation.
- The existing 50 manually labeled findings remain development/exploratory data and must be excluded from the final 400.
- Existing SS1/CS2 smoke outputs are preserved only as native-LLM integration/runtime feasibility evidence. They are **not** used to estimate corpus-scale LLM effectiveness.

---

# 1. Revised confirmatory research design

The final confirmatory experiment is:

```text
Frozen 735-Skill corpus
        |
        +--> SkillSpector SS0 committed baseline
        |
        +--> Cisco CS1 committed behavioral baseline
                 |
                 v
        Eligible security findings
                 |
                 v
       Frozen blind 400-finding sample
       - 200 SkillSpector
       - 200 Cisco
                 |
                 v
   Deterministic post-processing only
       - RAW / no post-processing
       - O1 Markdown Context
       - O1 Dataflow
       - O1 Semantic Context
       - Existing deterministic combined policy
                 |
                 v
          Human ground truth
                 |
                 v
    Paired precision / FP-suppression /
      TP-retention evaluation + statistics
```

## Confirmatory question

> Can deterministic context-aware post-processing significantly reduce false-positive findings produced by deployed agent-skill scanners while preserving genuine security findings?

## Explicitly excluded from the confirmatory experiment

Do **not** run or use as confirmatory methods:

- SS1 full/pilot;
- CS2 full/pilot;
- CS3;
- O2;
- any cloud/local LLM evaluator;
- LLM-dependent O3/O4/H1/H2/H3;
- LLM stability as a primary final experiment.

Do not delete their code or existing artifacts. Preserve already completed smoke evidence for discussion/limitations only.

---

# 2. Same-day execution contract

## 2.1 No more long scanner/LLM execution

From this point until the user returns the completed 400-label ground-truth file:

```text
DO NOT launch SkillSpector.
DO NOT launch Cisco skill-scanner.
DO NOT launch Ollama.
DO NOT start any native-LLM profile.
DO NOT start O2.
```

The pre-label path must operate only on already-existing validated baseline artifacts and deterministic Python processing.

## 2.2 Per-action runtime rule

No experiment action may be allowed to run blindly for a long period.

Before a potentially nontrivial operation:

1. run a small representative benchmark if runtime is unknown;
2. record measured duration;
3. estimate full duration;
4. continue only when projected duration is within this plan's limit.

Default hard limit:

```text
15 minutes per experiment action
```

Final project-only test/lint/type-check validation may use:

```text
20 minutes total
```

If an operation is projected to exceed its limit:

```text
STOP.
Do not start the full operation.
Report projected duration.
Wait for user approval.
```

## 2.3 Mandatory error/mismatch stop

For any unexpected error, mismatch, missing artifact, count mismatch, hash mismatch, invalid evidence, duplicate identity, failed hard gate, or required work outside this plan:

1. STOP immediately.
2. Update trace + ledger.
3. Do not improvise.
4. Print:

```text
ERROR_BLOCKED

Step:
Expected:
Observed:
Error or mismatch:
Evidence/log paths:
Minimal proposed fix:
Estimated fix duration:
Artifacts affected:

WAITING_FOR_USER_APPROVAL
```

5. Wait for explicit user approval.

Known repairs explicitly authorized inside a step may be completed without asking first.

## 2.4 Reuse only

- Do not reinstall scanners.
- Do not reinstall Ollama.
- Do not redownload models.
- Do not rerun scanner baselines.
- Do not rerun valid deterministic predictions.
- Do not mass-format files.
- Do not normalize line endings repository-wide.
- Ignore unrelated CRLF/LF Git noise.

---

# 3. Execution trace

Continue using:

```text
vulnerability-scanner/docs/experiments/v1/PART1_PRE_LABEL_EXECUTION_TRACE.md
vulnerability-scanner/docs/experiments/v1/TASK_EXECUTION_LEDGER.md
```

The old P1-06 must be closed as:

```text
SUPERSEDED_BY_REVISED_DETERMINISTIC_V1
```

Record that all preserved smoke artifacts remain available but no longer gate the confirmatory experiment.

For every revised step below record:

```markdown
## <Step> — <name>

- Status: PENDING | RUNNING | PASSED | BLOCKED | FAILED | REUSED
- Start:
- End:
- Duration:
- Work performed:
- Reused artifacts:
- Expected gate:
- Observed gate:
- Output paths:
- Errors/mismatches:
- Next allowed step:
```

---

# PART 1 — PRE-LABEL SAME-DAY PATH

Target Cursor compute time for Part 1:

```text
~60–120 minutes
```

No individual experiment action should exceed 15 minutes.

---

## R1 — Close the superseded LLM path

**Target: <= 5 minutes**

### Do

1. Mark old P1-06:
   `SUPERSEDED_BY_REVISED_DETERMINISTIC_V1`.
2. Preserve all existing smoke results.
3. Record:
   - SS0 10/10;
   - SS1 10/10;
   - CS0 10/10;
   - CS1 10/10;
   - CS2 10/10;
   - CS3 incomplete;
   - pilot not started;
   - full not started.
4. Mark SS1/CS2 smoke as:
   `exploratory_native_llm_feasibility_only`.
5. Mark the following outside the confirmatory experiment:
   - SS1 pilot/full;
   - CS2 pilot/full;
   - CS3;
   - O2;
   - LLM-dependent policies.
6. Do not delete any artifact.

### Hard gate

No protected or previously valid artifact is modified/deleted.

### Next

R2 only.

---

## R2 — Create a scanner-free deterministic V1 execution path

**Target: <= 20 minutes**

### Goal

Make it structurally impossible for the remaining Part 1 workflow to accidentally start scanner or Ollama work.

### Do

Create the smallest maintainable deterministic execution path using existing project modules.

Preferred implementation:

```text
configs/deterministic_postprocessing_v1.yaml
scripts/run_deterministic_v1.py
```

A minimal dedicated mode inside the existing orchestrator is acceptable only if it is simpler and equally safe.

### Allowed operations

The deterministic path may perform only:

- protected baseline validation;
- baseline finding loading;
- development-set exclusion;
- deterministic sampling;
- evidence assembly;
- O1 components;
- deterministic policy prediction;
- hard freeze;
- labeling checkpoint;
- future post-label metrics/statistics/reports.

### Forbidden calls

The deterministic path must have a hard guard preventing execution of:

- SkillSpector CLI;
- Cisco skill-scanner CLI;
- Ollama;
- SS1;
- CS2;
- CS3;
- O2.

### Also repair the confirmed subprocess decoding defect

Fix scanner subprocess capture so a Windows-1252-like byte such as `0x97` cannot crash result collection if scanners are run in the future.

Preserve raw output as safely as practical and decode logs defensively.

Add a focused regression test.

**Do not run scanners after fixing it.**

### Focused tests

Test:

- deterministic path cannot invoke scanners;
- deterministic path cannot invoke Ollama;
- UTF-8/non-UTF-8 scanner output capture regression;
- protected baseline load;
- deterministic resume.

### Hard gate

All focused tests pass.

### Runtime stop

If this repair expands beyond 20 minutes because a broader refactor appears necessary, stop and request approval. Do not refactor the entire orchestration framework.

---

## R3 — Validate the two confirmatory baseline populations

**Target: <= 5 minutes**

### Use only existing protected/committed outputs

#### SkillSpector

Confirm expected SS0 security population:

```text
2,309 security findings
```

#### Cisco

Confirm CS1 contains:

```text
508 security findings
615 advisories
```

The confirmatory 400-sample population uses:

```text
Cisco security findings only
```

Do not mix the 615 advisories into the 200 Cisco sample.

### Also validate

- protected baseline hashes;
- V0 hash;
- exactly 735 Skills;
- source paths resolve;
- finding IDs are unique or duplicate structure is explicit;
- development-set finding identities can be identified and excluded.

### Hard gate

Two unambiguous eligible security-finding populations exist:

- SkillSpector SS0;
- Cisco CS1 security findings.

### Error stop

If Cisco security findings cannot be cleanly separated from advisories, STOP and ask for approval.

---

## R4 — Build deterministic sampling populations and reserve order

**Target: <= 10 minutes**

### Critical rule

Sampling occurs before O1 predictions are used.

Do not sample based on:

- O1 outcome;
- suppression;
- disagreement;
- LLM result;
- previous native-LLM smoke behavior.

### For each scanner separately

1. Start from eligible security findings.
2. Exclude all 50-development-set findings.
3. Exclude invalid/missing-source candidates.
4. Remove duplicate evidence instances using the existing identity/evidence mechanism.
5. Preserve the eligible-population count after exclusions.
6. Randomize deterministically using:

```text
seed = 20260805
```

7. Save the complete deterministic reserve order.

### Primary sample

Take the first evidence-valid:

```text
200 SkillSpector
200 Cisco
```

If evidence assembly later rejects a selected candidate, replacement must use the next candidate in the frozen reserve order.

### Hard gate

Before evidence replacement:

- 400 unique selected finding IDs;
- exactly 200/200 scanner split;
- 0 development-set overlap;
- 0 duplicate evidence instances.

### Save

Sampling report must state:

- original population;
- security-only population;
- exclusions;
- eligible population;
- seed;
- reserve order hash;
- sample probability/selection procedure.

---

## R5 — Build blind evidence-complete review packets

**Target: <= 20 minutes**

### Visible review unit must contain

- neutral risk family;
- neutral behavior description;
- Skill purpose;
- file path and location;
- flagged evidence;
- surrounding source/text context;
- complete relevant function/class when applicable;
- source-to-sink context when applicable;
- related-file evidence when necessary;
- relevant raw metadata required for judgment.

### Visible review unit must NOT contain

- scanner name;
- vendor rule ID;
- scanner profile;
- O1 result;
- deterministic policy result;
- sampling population/source;
- native-LLM result;
- model identity;
- LLM confidence.

### Evidence replacement rule

If a candidate lacks enough evidence for a defensible human judgment:

1. reject it;
2. record the rejection reason privately;
3. select the next finding in that scanner's frozen reserve order;
4. rebuild the packet.

Do not accept:

```text
[file not found]
```

or equivalent missing evidence as a review unit.

### Hard gate

Exactly:

```text
400 review units
200 SkillSpector
200 Cisco
0 insufficient-evidence units
0 blind-field leaks
0 development overlap
0 duplicate finding IDs
0 duplicate evidence instances
```

---

## R6 — Run O1 only on the frozen 400 findings

**Target: <= 15 minutes**

### Methods

Run separately:

- `markdown_context`;
- `dataflow`;
- `semantic_context`.

Preserve independent component outputs.

### Runtime benchmark gate

Before running all 400:

1. run exactly 20 representative frozen findings;
2. measure wall-clock time;
3. estimate the 400-finding runtime.

If projected runtime is:

```text
<= 15 minutes
```

continue automatically.

If projected runtime is:

```text
> 15 minutes
```

STOP and request approval before the full O1 run.

### Output per finding/component

Preserve:

- finding ID;
- applicability;
- verdict;
- recommended action;
- reason codes;
- explanation;
- component version/hash.

### Hard gate

All 400 frozen findings have an explicit O1 component result or a documented non-applicable state.

No placeholder output.

---

## R7 — Freeze deterministic policies

**Target: <= 10 minutes**

### Compare only predeclared deterministic methods

Required:

1. `RAW`
   - scanner finding retained;
   - represents no post-processing.

2. `O1_MARKDOWN`

3. `O1_DATAFLOW`

4. `O1_SEMANTIC`

5. `O1_COMBINED`
   - use the project's existing deterministic combined/filtering policy;
   - do not invent a new combination after seeing labels.

If a deterministic aggressive/conservative ablation already exists and is already specified in project code before labeling, it may be retained and documented.

Do not create extra methods just to increase experiment count.

### Freeze now, before labels

For every method preserve:

- method name;
- policy version;
- code/config hash;
- component inputs;
- final keep/suppress/abstain decision;
- reason codes.

### Hard gate

Every one of the 400 frozen findings has complete predictions for every applicable declared deterministic method.

---

## R8 — Hard-freeze the revised 400-sample V1

**Target: <= 10 minutes**

Generate/finalize:

```text
data/evaluation/v1/test_set_400_v1_manifest.jsonl
data/evaluation/v1/test_set_400_v1_sampling_report.json
data/evaluation/v1/test_set_400_v1_sha256.txt
data/evaluation/v1/review_packets/
data/evaluation/v1/label_template_v1.jsonl
```

### Hidden manifest may contain

- scanner identity;
- finding ID;
- source population;
- policy/prediction linkage;
- private provenance.

### Visible packets remain blind

### Freeze assertions

All must be true:

```text
400 total
200 SkillSpector
200 Cisco
0 duplicate finding IDs
0 duplicate evidence instances
0 development-set overlap
0 insufficient-evidence units
0 invalid evidence paths
0 blind-field leaks
all deterministic predictions frozen
all policy hashes frozen
manifest hash reproducible
```

An issues list must be empty.

### Hard gate

Freeze passes every assertion.

Any issue -> `ERROR_BLOCKED`; do not create checkpoint.

---

## R9 — Final pre-label quality and resume validation

**Target: <= 20 minutes**

From `vulnerability-scanner/` run project-only validation:

```powershell
python -m pytest tests/ -q
ruff check src tests
mypy src
```

Do not run vendored scanner test suites.

Do not launch scanner executables.

Do not launch Ollama.

### Resume check

Run the deterministic V1 command again with resume.

The second invocation must:

- perform zero new O1 evaluations;
- preserve the 400 manifest;
- preserve the test-set SHA;
- reuse unchanged deterministic predictions;
- perform zero scanner work;
- perform zero LLM work.

### Final integrity

Reverify:

- V0 protected hash;
- SS0 protected baseline;
- CS1 protected baseline;
- exactly 735 Skills.

### Hard gate

All required validation/integrity/resume checks pass.

---

## R10 — Create labeling checkpoint and STOP

**Target: <= 5 minutes**

Create/finalize:

```text
CHECKPOINT_LABELING_REQUIRED_V1
```

Update:

```text
PART1_PRE_LABEL_EXECUTION_TRACE.md
TASK_EXECUTION_LEDGER.md
```

### Print only

```text
CHECKPOINT_LABELING_REQUIRED_V1

Test set:
<path>

Review packets:
<path>

Label template:
<path>

Test-set SHA-256:
<hash>

Evaluation methods:
RAW
O1_MARKDOWN
O1_DATAFLOW
O1_SEMANTIC
O1_COMBINED
<any pre-existing deterministic ablation explicitly retained>

Native-LLM smoke feasibility artifacts:
<path>

Part 1 trace:
<path>

Resume command after labels:
<command>
```

Then STOP.

Do not generate labels.

Do not inspect future labels.

Do not tune policies.

---

# MANUAL LABELING PHASE — OUTSIDE CURSOR

The user will label the exact frozen 400 blind review units externally.

Expected gold file:

```text
data/evaluation/v1/test_set_400_v1_gold.jsonl
```

Expected:

```text
exactly 400 unique review IDs
```

Allowed ground-truth values must follow the project's frozen label schema, including explicit `uncertain` if defined.

Cursor must not resume until the user explicitly provides the completed gold file.

---

# PART 2 — POST-LABEL SAME-DAY PATH

Create:

```text
vulnerability-scanner/docs/experiments/v1/PART2_POST_LABEL_EXECUTION_TRACE.md
```

Target Cursor compute time:

```text
~30–60 minutes
```

No scanner or LLM execution is allowed in Part 2.

---

## P2-R1 — Validate supplied gold labels

**Target: <= 5 minutes**

Validate:

- exactly 400 records;
- unique review IDs;
- every review ID exists in frozen manifest;
- no missing IDs;
- no extra IDs;
- frozen manifest hash unchanged;
- test-set SHA unchanged;
- allowed label values only;
- `uncertain` preserved explicitly.

### Hard gate

Gold labels map exactly to the frozen 400.

Any mismatch -> STOP and ask user.

---

## P2-R2 — Join frozen labels and deterministic predictions

**Target: <= 5 minutes**

Join only:

```text
gold.review_id
→ frozen_manifest.finding_id
→ frozen_prediction.finding_id
```

Do not guess identity.

### Hard gate

Every analyzable gold record joins deterministically to all applicable frozen method predictions.

---

## P2-R3 — Compute final method metrics

**Target: <= 10 minutes**

Primary results must be reported separately for SkillSpector and Cisco.

For:

- RAW;
- O1_MARKDOWN;
- O1_DATAFLOW;
- O1_SEMANTIC;
- O1_COMBINED;
- any frozen deterministic ablation.

Compute:

- precision;
- false-positive suppression rate;
- true-positive retention;
- false suppression rate;
- coverage;
- abstention rate;
- F1;
- MCC;
- balanced accuracy;
- Skill-level metrics;
- error rate.

### Important

Do not naively pool the 200 SkillSpector and 200 Cisco findings as if they represent equal underlying populations.

If a pooled descriptive estimate is generated, clearly distinguish it from the scanner-specific primary results and use an explicitly documented weighting rule.

---

## P2-R4 — Statistical analysis

**Target: <= 20 minutes**

Run the predeclared applicable deterministic-method statistics:

- Skill-clustered bootstrap;
- repository-clustered sensitivity bootstrap where repository identity exists;
- paired bootstrap;
- McNemar tests;
- Cochran's Q when appropriate;
- corrected pairwise comparisons;
- effect sizes;
- 95% confidence intervals;
- TP-retention non-inferiority analysis using the predeclared margin.

Do not alter methods after inspecting favorable/unfavorable results.

### Hard gate

Every reported comparison has valid paired inputs and complete sample accounting.

---

## P2-R5 — Generate final reports

**Target: <= 10 minutes**

Generate nonempty:

- Markdown;
- JSON;
- JSONL;
- CSV.

Reports must cover:

- eligible baseline populations;
- final 400 composition;
- RAW scanner precision;
- each O1 component;
- O1 combined policy;
- FP suppression;
- TP retention;
- coverage/abstention;
- scanner-specific results;
- statistical results;
- limitations;
- preserved native-LLM feasibility/runtime observation.

### Native-LLM limitation language

Do not report SS1/CS2 smoke as an effectiveness benchmark.

It may be reported only as an operational observation such as:

> Native LLM-assisted scanner modes were successfully integrated on a controlled smoke subset, but their multi-call local inference structure required several minutes per Skill on the available hardware. Corpus-scale native-LLM scanning was therefore excluded from the confirmatory evaluation, which focuses on deterministic context-aware post-processing.

---

## P2-R6 — Final integrity and completion

**Target: <= 10 minutes**

Verify:

- V0 unchanged;
- SS0 baseline unchanged;
- CS1 baseline unchanged;
- frozen 400 unchanged;
- deterministic policy hashes unchanged;
- no post-label policy tuning;
- no scanner execution after revised plan start;
- no Ollama/LLM execution after revised plan start;
- all final metrics trace to frozen predictions and supplied gold labels.

Finalize:

```text
PART2_POST_LABEL_EXECUTION_TRACE.md
TASK_EXECUTION_LEDGER.md
```

### Successful endpoint

Print:

```text
V1_EXPERIMENT_COMPLETE

Frozen test-set SHA-256:
<hash>

SkillSpector sample:
200

Cisco sample:
200

Confirmatory methods:
<list>

Part 1 trace:
<path>

Part 2 trace:
<path>

Final report directory:
<path>

Protected baseline verification:
PASSED

Post-label tuning:
NONE

Scanner executions after revised-plan start:
NONE

LLM/Ollama executions after revised-plan start:
NONE
```

---

# 4. Absolute prohibitions

From this revised-plan start onward Cursor must never:

- continue old P1-06 pilot;
- start old P1-07;
- run SS1 beyond preserved smoke;
- run CS2 beyond preserved smoke;
- run CS3;
- run O2;
- call Ollama;
- call a hosted LLM for experiment inference;
- rerun SS0 or CS1 scanners;
- sample based on O1 outcomes;
- tune a deterministic policy after labels are revealed;
- include development findings in the final 400;
- mix Cisco advisories into the Cisco security-finding sample;
- accept an evidence-incomplete review unit;
- silently continue after a hard-gate mismatch;
- create fake delta/disagreement strata;
- rerun expensive work merely for resume testing;
- claim native-LLM effectiveness from the 10-Skill smoke data.

---

# 5. Same-day schedule target

This plan is intentionally bounded.

Expected Cursor-side work before labeling:

| Stage | Target |
|---|---:|
| R1 | 5 min |
| R2 | 20 min |
| R3 | 5 min |
| R4 | 10 min |
| R5 | 20 min |
| R6 | 15 min |
| R7 | 10 min |
| R8 | 10 min |
| R9 | 20 min |
| R10 | 5 min |
| **Target total Part 1** | **~120 min maximum planned** |

Expected Cursor-side work after the user returns labels:

| Stage | Target |
|---|---:|
| P2-R1 | 5 min |
| P2-R2 | 5 min |
| P2-R3 | 10 min |
| P2-R4 | 20 min |
| P2-R5 | 10 min |
| P2-R6 | 10 min |
| **Target total Part 2** | **~60 min maximum planned** |

These are execution targets, not permission to weaken hard gates.

If any operation is projected to violate the same-day budget, Cursor must stop before launching it and request approval.

The major remaining human-time dependency is the manual labeling of the frozen 400 review units; Cursor-side computation is deliberately designed not to become a multi-hour or multi-day bottleneck.

---

# 6. Final priority order

```text
VALID GROUND-TRUTH DESIGN
→ PROTECTED BASELINE INTEGRITY
→ DETERMINISTIC REPRODUCIBILITY
→ NO DATA LEAKAGE
→ NO UNNECESSARY SCANNER/LLM EXECUTION
→ SAME-DAY COMPLETION
```

No speed optimization may invalidate the 400-sample evaluation, but no legacy experiment requirement may trigger a long scanner/LLM run after this plan supersedes it.
