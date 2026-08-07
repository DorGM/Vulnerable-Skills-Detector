# Vulnerable-Skills-Detector V1 — Strict Two-Part Completion Plan

> **This file supersedes and replaces the previous `CURSOR_V1_RECOVERY_AND_COMPLETION_PLAN.md`.**
>
> It is the **only recovery/completion execution plan Cursor may follow** for V1.  
> Do not add work, refactors, experiments, models, metrics, or stages that are not explicitly authorized here.
>
> The original 38-task research specification remains the scientific acceptance reference behind this plan, but Cursor must execute **only the numbered steps below**, in this order.

---

# 0. Objective and audited starting point

The project must be completed in two strictly separated parts:

- **PART 1 — PRE-LABEL:** repair/validate the experiment, run the required scanners/evaluators, and freeze exactly 400 blind evidence-complete review units.
- **MANUAL LABELING STOP:** the user will label the 400 units externally with ChatGPT and return the completed ground-truth file.
- **PART 2 — POST-LABEL:** validate the supplied gold labels, run the final experiments/statistics/reports, verify integrity, and finish the research run.

Current audited state that must be respected:

- Protected V0/baseline assets are reusable and must remain immutable.
- The 735-Skill corpus is expected to remain intact.
- The previous false labeling checkpoint is invalid.
- The current `llama3.1:8b` model lock is **not scientifically valid** and must not be trusted.
- The previous model qualification used insufficient finding context and selected a model with catastrophic TP loss.
- Package 4 / one-Skill probing was interrupted.
- Several execution-control defects still exist or require revalidation: stage completion on failures, nested raw-result normalization, cloud fallback text/path, exact matching behavior, fake-delta sampling fallback, and freeze-with-warnings behavior.
- Reuse valid artifacts only when their hashes, provenance, configuration, code dependencies, and semantic gates still match the corrected pipeline.

The goal is to finish **as quickly as possible without invalidating the research**.

---

# 1. Non-negotiable execution contract

## 1.1 Sequential execution

1. Execute steps strictly in order.
2. Do not start the next step until the current step has **PASSED** its hard gate.
3. Never mark a step complete because a command merely returned exit code 0.
4. Completion requires the stated **semantic** acceptance gate.
5. Do not silently relax any count, hash, identity, provenance, error-rate, model, evidence, blindness, or reproducibility condition.

## 1.2 Mandatory approval stop on any unexpected error or mismatch

Known defects explicitly listed inside a step are **authorized repair work** and do not themselves require approval.

However, if any of the following occurs:

- an unexpected error;
- an unexpected mismatch;
- a hard-gate failure after the authorized work;
- a required count differs from expected;
- a hash/provenance check fails;
- a scanner/profile behaves differently from the defined profile;
- a model/digest differs from the active lock;
- a parser/schema failure violates the step gate;
- an output is missing, empty, contaminated, duplicated, ambiguous in an unsafe way, or semantically invalid;
- a required dependency/configuration is unavailable;
- the required fix would go outside this plan;

then Cursor must:

1. **STOP immediately.**
2. Update the active Part trace MD and `TASK_EXECUTION_LEDGER.md` as `BLOCKED` or `FAILED`.
3. Do not start the next step.
4. Do not invent an unplanned workaround.
5. Do not broaden scope.
6. Print exactly this concise block to the user:

```text
ERROR_BLOCKED

Part:
Step:
Expected:
Observed:
Error or mismatch:
Evidence/log paths:
Minimal proposed fix:
Artifacts/stages that would be invalidated:
Trace updated at:

WAITING_FOR_USER_APPROVAL
```

7. Wait for explicit user approval before corrective work or continuation.

### Allowed non-blocking cases

These do **not** require approval when explicitly permitted by the current step:

- an intentionally negative test that fails in the expected way;
- the single explicitly allowed timeout retry;
- documented per-Skill failures that remain inside an explicitly stated accepted error-rate gate;
- reuse/skipping of already-valid work when hash/provenance/state validation passes.

All such cases must still be recorded in the trace.

## 1.3 Local LLM only

All experimental LLM inference must use local Ollama only:

```text
127.0.0.1:11434
```

Never use or fall back to:

- OpenAI hosted inference;
- Anthropic;
- Gemini;
- OpenRouter;
- NVIDIA hosted inference;
- remote Ollama/cloud models;
- any other paid or hosted inference API.

`ollama-local` may be used only as the local dummy compatibility API-key value.

A non-local experiment LLM base URL is a hard failure.

## 1.4 Protected research assets

Never modify protected V0/baseline research data.

Verify hashes at the beginning of Part 1, at the Part 1 freeze, and at final Part 2 completion.

## 1.5 Scope control

- Modify only files required by the numbered steps below.
- Avoid broad refactors.
- Do not mass-format files.
- Do not normalize repository line endings.
- Ignore unrelated CRLF/LF-only Git noise.
- Do not run vendored scanner test suites.
- Do not reinstall scanners/Ollama/models when the existing installation passes validation.
- Do not create placeholder outputs that can satisfy a stage.
- Do not generate gold labels.

---

# 2. Mandatory live trace files

Cursor must maintain **two separate concise execution traces**.

## Part 1 trace

Create at the beginning of Part 1:

```text
vulnerability-scanner/docs/experiments/v1/PART1_PRE_LABEL_EXECUTION_TRACE.md
```

## Part 2 trace

Create only when the user supplies the completed gold-label file:

```text
vulnerability-scanner/docs/experiments/v1/PART2_POST_LABEL_EXECUTION_TRACE.md
```

## Trace rules

The trace is a live audit document, not a final retrospective.

For every step:

1. Before work: set the step to `RUNNING`.
2. Immediately after success: set it to `PASSED`.
3. On a stop: set it to `BLOCKED` or `FAILED` before messaging the user.
4. Never backfill the whole trace only at the end.
5. Keep it full but short. Do not paste large logs.
6. Point to raw logs/artifacts by path.
7. Never delete previous results or failure history; append corrections/amendments.

Use this compact structure for each step:

```markdown
## <Step ID> — <name>

- Status: PENDING | RUNNING | PASSED | BLOCKED | FAILED | REUSED
- Start:
- End:
- Duration:
- Reused work:
- Work performed:
- Hard gate expected:
- Hard gate observed:
- Tests/checks:
- Key output paths/hashes:
- Errors/mismatches:
- User approval required: yes/no
- Next allowed step:
```

Also continue updating:

```text
vulnerability-scanner/docs/experiments/v1/TASK_EXECUTION_LEDGER.md
```

The two trace files are the concise human-readable progress record; the ledger remains the detailed task/state record.

---

# 3. Speed-first execution rules

The run should be as short as scientifically safe.

1. **Reuse before rerun.** Reuse an artifact only when current code/config/model/upstream hashes and semantic validity prove it is still valid.
2. Use focused tests during repair. Run the full project test/lint/type-check suite only at the explicit final gates.
3. Preserve per-Skill resume/caching. Never repeat a valid scanner or O2 result unnecessarily.
4. Do not reinstall existing valid scanner environments, Ollama, or models.
5. Do not repeat model downloads.
6. Keep Ollama experimental concurrency at the locked safe value; do not trade reproducibility/stability for aggressive parallelism.
7. Use the existing Windows keep-awake guard for long runs.
8. For O2, use the smallest controlled candidate pool necessary for the frozen 400-unit set; do not evaluate every baseline finding by default.
9. Do not generate final gold-based analyses in Part 1.
10. If a long stage is interrupted, resume from valid per-Skill/per-finding state instead of restarting the stage.

---

# PART 1 — BEFORE THE 400-SAMPLE LABELING

The only successful Part 1 endpoint is:

```text
CHECKPOINT_LABELING_REQUIRED_V1
```

After this checkpoint Cursor must stop and wait for the user's completed gold labels.

---

## P1-01 — Establish the valid starting state

### Do

1. Record current Git commit.
2. Create/update `PART1_PRE_LABEL_EXECUTION_TRACE.md`.
3. Verify protected baseline hashes.
4. Verify the protected V0 manifest hash.
5. Verify exactly **735 valid Skill directories**.
6. Verify existing invalid-attempt archives remain preserved.
7. Verify the false previous active V1 checkpoint/state cannot be reused.
8. Invalidate/archive the scientifically invalid current model lock and every downstream artifact that depends on it.
9. Invalidate the interrupted one-Skill/Package-4 continuation state where required.
10. Preserve valid scanner installations, Ollama installation, downloaded models, V0, SS0, CS1, and independent valid preflight evidence.

### Hard gate

- Protected hashes pass.
- Exactly 735 Skills load.
- Invalid model-lock/downstream V1 work cannot be resumed accidentally.
- Valid protected/reusable assets remain untouched.

### Mandatory error stop

Any unexpected hash/count/state/provenance mismatch → update trace + ledger, emit `ERROR_BLOCKED`, and wait for user approval.

---

## P1-02 — Repair and prove execution-control correctness

This step authorizes repair of the already-audited pipeline-control defects only.

### Do

Repair/revalidate:

1. Stage status semantics:
   - `pending`
   - `running`
   - `completed`
   - `partial`
   - `failed`
   - `blocked`
   - `invalidated`

2. Scanner stage completion:
   - `requested > 0`;
   - every requested Skill has an explicit terminal state;
   - success/failure accounting is complete;
   - a stage cannot be completed merely because its orchestration command returned 0.

3. Failed/blocked/parser-failed/fail-open profiles must never produce downstream-valid empty normalized outputs.

4. Raw-result parsing/normalization must correctly read the current nested result structure, including `run.parsed_data`.

5. Preserve complete:
   - stdout;
   - stderr;
   - exit code;
   - parser result;
   - duration;
   - retry state;
   - analyzers;
   - model identity/digest.

6. Remove/disable every V1 cloud fallback/configuration path. The only local-LLM setup checkpoint is:

```text
CHECKPOINT_LOCAL_LLM_SETUP_REQUIRED
```

7. Ensure profile arguments are authoritative and exact:
   - no Cisco scanner CLI use of `--enable-llm`;
   - use `--use-llm`.

8. Ensure Cisco LLM and Meta use `ollama/<selected-model>` and localhost.

9. Required quality commands must fail their stage on nonzero exit.

10. Matching must use exact maximum-weight bipartite matching; no silent greedy fallback.

11. Ambiguous matches remain ambiguous, never silently converted to suppressed.

12. Sampling may never fill a missing `native_delta` quota with ordinary baseline findings.

13. Freeze may never pass when an issues list is nonempty.

14. Resume must validate result hashes and semantic success before skipping work.

15. Downstream invalidation must follow the dependency DAG.

### Focused validation only

Run focused tests for the corrected invariants. Do not run the full suite yet.

### Hard gate

All listed execution-control invariants are proven by focused tests.

### Mandatory error stop

Any listed invariant that still fails after authorized repair, or any new unplanned pipeline defect → update trace + ledger, emit `ERROR_BLOCKED`, and wait for user approval.

---

## P1-03 — Validate the exact local execution environment

### Do

Validate without unnecessary reinstall:

1. Exactly 735 Skills.
2. Pinned SkillSpector:
   - executable path;
   - exact commit;
   - version;
   - `scan --help`;
   - dependency environment.

3. Pinned Cisco skill-scanner:
   - executable path;
   - exact commit;
   - version;
   - `scan --help`;
   - dependency environment.

4. Exact SS0/SS1/CS0/CS1/CS2/CS3 profile flags against real scanner help.

5. Ollama:
   - CLI;
   - localhost API;
   - `OLLAMA_NO_CLOUD=1`;
   - loopback-only service;
   - no cloud fallback.

6. Candidate models already present:
   - `qwen3:8b`;
   - `llama3.1:8b`;
   - full digest;
   - size;
   - quantization;
   - parameter count when reported.

7. Canonical environment adapter:
   - SkillSpector → localhost OpenAI-compatible Ollama;
   - Cisco LLM → `ollama/<model>`;
   - Cisco Meta → `ollama/<model>`;
   - O2 → localhost `/v1`.

8. Direct native Ollama and OpenAI-compatible health checks for both candidates using the real classification schema.

### Hard gate

Every required executable/profile/local endpoint is valid and no experimental LLM path can leave localhost.

### Mandatory error stop

Any environment/profile/commit/digest/localhost mismatch → update trace + ledger, emit `ERROR_BLOCKED`, and wait for user approval.

---

## P1-04 — Requalify and lock the local model correctly

The current `llama3.1:8b` lock is invalid and must not be reused.

### Do

Use only the existing **50-example development set**.

Evaluate:

- `qwen3:8b`
- `llama3.1:8b`

Run **3 complete trials per candidate** using identical prompt/context-building code.

The qualification context must contain enough evidence to make a real finding judgment, including at minimum:

- finding description;
- raw flagged evidence;
- relevant source snippet/context;
- file/path/line information;
- rule/context metadata;
- relevant source/sink information when available.

Do not qualify from scanner/rule/path/line metadata alone.

Measure:

- JSON/schema success;
- TP retention;
- FP suppression;
- precision;
- abstention;
- verdict consistency;
- API failure rate;
- median local runtime.

### Model-selection hard gate

Selection priority:

1. no catastrophic TP loss;
2. highest TP retention;
3. reliable structured output;
4. stable repeated verdicts;
5. precision;
6. runtime.

Do not lock an 8B model merely because the other candidate failed parsing.

If neither 8B model qualifies:

1. assess `qwen3:14b` feasibility using the recorded local hardware;
2. run it only if it can operate reliably;
3. otherwise stop at `CHECKPOINT_LOCAL_LLM_SETUP_REQUIRED`.

### Lock

Freeze:

- model;
- full Ollama digest;
- quantization;
- Ollama version;
- temperature;
- context policy;
- prompt hashes;
- environment-adapter version.

Any later change to these fields invalidates all downstream LLM work.

### Hard gate

Exactly one scientifically qualified local model is fully locked.

### Mandatory error stop

If no model meets the gate, a metric is inconsistent, context is insufficient, or a model/digest cannot be proven → update trace + ledger, emit `ERROR_BLOCKED` or the permitted local-model checkpoint, and wait for user approval.

---

## P1-05 — One-Skill semantic integration probes

Use one fixed Skill and prove each path before expensive execution.

### Do

Probe:

1. SS0
2. SS1
3. CS0
4. CS1
5. CS2
6. CS3
7. O2

Verify for every relevant path:

- exact profile;
- real Skill attempted;
- valid parser/schema;
- raw output preserved;
- selected model digest actually used where applicable;
- Cisco LLM truly executed;
- Cisco Meta truly executed;
- no UNKNOWN/fail-open accepted as success;
- O2 returns TP/FP/uncertain or explicit abstention;
- no cloud credential/endpoint;
- resume skips valid result.

Reuse already-valid non-LLM probes only if their dependency hashes still match after P1-02.

### Hard gate

All seven paths pass semantic validation.

### Mandatory error stop

Any probe failure/mismatch outside explicitly permitted retry behavior → update trace + ledger, emit `ERROR_BLOCKED`, and wait for user approval. Do not launch smoke tests.

---

## P1-06 — 10-Skill smoke and 50-Skill pilot gates

### Do

Use fixed reproducible Skill lists.

Run/reuse valid results for:

- SS0
- SS1
- CS0
- CS1
- CS2
- CS3
- O2 where defined by the experiment flow

First 10 Skills, then 50 Skills.

Verify:

- exact attempted counts;
- real per-Skill results;
- valid attribution;
- valid parsing/schema;
- no profile contamination;
- model digest consistency;
- explicit Meta success;
- no unexplained identity collision;
- local-only inference;
- resume performs zero duplicate valid work.

Accepted scanner-profile error rate:

```text
< 5%
```

excluding only documented infrastructure outages.

A documented failure inside the allowed threshold must be recorded but is not itself a plan mismatch.

### Hard gate

Both smoke and pilot gates pass for every required profile.

### Mandatory error stop

Any profile exceeds the gate, Meta fails/falls open, resume repeats valid work, or any unexpected mismatch appears → update trace + ledger, emit `ERROR_BLOCKED`, and wait for user approval.

---

## P1-07 — Complete the six full scanner profiles

### Speed rule

Reuse committed/full results only after integrity + dependency validation.

### Do

For all 735 Skills:

- SS0 — reuse only if valid;
- SS1 — run/complete with locked model;
- CS0 — run freshly unless a valid current post-repair full run already exists;
- CS1 — reuse only if valid;
- CS2 — run/complete with locked model;
- CS3 — run/complete with locked model + verified Meta.

Store one raw result per Skill per profile.

On timeout:

1. save timeout;
2. retry once at double timeout;
3. save final failure;
4. continue.

A failure is never equivalent to zero findings.

Use per-Skill resume so an interruption does not restart valid work.

### Hard gate

For every profile:

- requested = 735;
- all 735 Skills have explicit terminal state;
- completed/failed/timeouts/parser failures are fully accounted;
- no missing Skills;
- no invalid empty profile is treated as valid.

### Mandatory error stop

Any profile-level accounting/provenance/model mismatch or hard-gate failure → update trace + ledger, emit `ERROR_BLOCKED`, and wait for user approval before downstream normalization.

---

## P1-08 — Normalize identities and execute native matching

### Do

Normalize only semantically valid profile outputs.

For each finding preserve:

- unique finding instance identity;
- candidate key;
- duplicate group/occurrence/count;
- scanner/profile/analyzer/rule;
- category/severity;
- path/line range;
- raw evidence/metadata;
- reviewed taxonomy classes;
- scanner version/commit;
- model digest when applicable.

Verify:

- zero silent overwrite;
- zero unexplained ID collisions;
- zero scanner/profile contamination.

Run exact native comparisons:

- SS0 → SS1
- CS0 → CS1
- CS1 → CS2
- CS1 → CS3
- CS2 → CS3

Produce explicit:

- matched;
- suppressed;
- new;
- merged;
- split;
- ambiguous;
- unmatched;
- score;
- level.

Never match against blocked/absent/empty/parser-failed/fail-open profiles.

### Hard gate

All normalized profiles and five matching comparisons are provenance-valid, collision-safe, and exact.

### Mandatory error stop

Any identity collision, contamination, invalid source profile, unsafe ambiguity handling, or matching mismatch → update trace + ledger, emit `ERROR_BLOCKED`, and wait for user approval.

---

## P1-09 — Run O1, O2, and policy predictions with minimum necessary LLM work

### O1

Run separately:

- markdown context;
- dataflow;
- semantic context.

Preserve independent component votes.

### O2 — speed-optimized controlled pool

Use only the locked local model.

Do **not** run O2 over every baseline finding by default.

Run O2 on:

1. all valid native-delta/disagreement candidates needed to build the 40-delta strata;
2. a seeded, stratified baseline candidate reserve sufficient to fill 160 baseline units per scanner plus replacements.

Initial baseline reserve:

```text
192 SkillSpector baseline candidates
192 Cisco baseline candidates
```

If the final sample cannot be completed because of evidence/limits/duplicates, expand the affected scanner reserve in deterministic batches of **32** only as needed.

O2 must preserve:

- finding ID;
- TP/FP/uncertain;
- raw response;
- prompt hash;
- adequate evidence/context;
- model digest;
- cache key;
- parse/inference failure;
- abstention.

Never read gold labels.

### Policies

Generate real per-finding outputs for the evaluated candidate universe:

- O3
- O4
- H1
- H2
- H3

No empty placeholder directories.

### Hard gate

Every required candidate has an explicit valid prediction, failure, or abstention record, and all LLM inference is local/cached.

### Mandatory error stop

Any cloud path, missing prediction universe, invalid O2 context, model mismatch, placeholder output, or policy inconsistency → update trace + ledger, emit `ERROR_BLOCKED`, and wait for user approval.

---

## P1-10 — Complete post-label analysis code using synthetic fixtures only

Do not run real gold-label analysis yet.

### Do

Implement/test with synthetic fixtures:

1. Join:
   - manifest `review_id → finding_id`;
   - gold keyed by `review_id`;
   - predictions keyed by `finding_id`.

2. Experiment A required native variants.

3. Experiment B:
   - Native;
   - O1 components;
   - O2;
   - O3;
   - O4;
   - H1;
   - H2;
   - H3.

4. Metrics:
   - precision;
   - FP suppression rate;
   - TP retention;
   - false suppression rate;
   - coverage;
   - abstention;
   - F1;
   - MCC;
   - balanced accuracy;
   - Skill-level metrics;
   - pooled relative recall;
   - runtime;
   - local computational token usage;
   - error rate.

5. Statistics:
   - Skill-clustered bootstrap;
   - repository-clustered sensitivity bootstrap;
   - paired bootstrap;
   - McNemar;
   - Cochran's Q;
   - multiple-comparison correction;
   - effect sizes;
   - 95% CI;
   - 2-percentage-point TP-retention non-inferiority.

6. LLM stability analysis.

7. Real nonempty Markdown/JSON/JSONL/CSV report generators.

8. Future resume must accept exactly 400 labels without rerunning valid scanner/Ollama work.

### Speed rule

Use small synthetic fixtures only. Do not perform large bootstrap/report runs on real data before labels exist.

### Hard gate

Synthetic fixture tests prove the complete Part 2 analysis path can execute end-to-end.

### Mandatory error stop

Any missing metric/statistic/join/report output required above → update trace + ledger, emit `ERROR_BLOCKED`, and wait for user approval.

---

## P1-11 — Select exactly 400 review units

### Required composition

Exactly:

```text
SkillSpector: 160 baseline + 40 real delta = 200
Cisco:        160 baseline + 40 real delta = 200
TOTAL:                                    400
```

### Do

1. Select delta first.
2. Delta priority:
   - native-only;
   - baseline suppressed by valid native filtering;
   - materially changed by native analysis;
   - native/external disagreement;
   - hybrid disagreement;
   - difficult/uncertain evidence.

3. Every delta must have real valid native/external provenance.
4. Never replace missing delta with ordinary baseline.
5. Exclude:
   - development-set IDs;
   - delta/baseline overlap;
   - already selected IDs;
   - duplicate evidence instances.

6. Apply adaptive limits using the lowest tier that fills the stratum.
7. Seed:

```text
20260805
```

8. Record the tier used per scanner and stratum.

### Hard gate

Exactly 400 unique, provenance-valid units with exact 160/40 composition per scanner.

### Mandatory error stop

If any required stratum cannot be filled, any duplicate/overlap exists, or any delta lacks valid provenance → update trace + ledger, emit `ERROR_BLOCKED`, and wait for user approval. Do not weaken the quota automatically.

---

## P1-12 — Build blind, evidence-complete review packets

### Visible packet must include

- neutral risk family;
- neutral behavior description;
- Skill purpose;
- file/path/line range;
- flagged evidence;
- surrounding source context;
- complete relevant function/class;
- source-to-sink trace where applicable;
- relevant raw metadata;
- related files;
- cross-file source/sink excerpts where applicable;
- package-level inventory/threshold evidence where applicable.

### Visible packet must hide

- scanner name;
- rule ID;
- profile;
- native verdict;
- external verdict;
- sampling source;
- selected model;
- LLM confidence.

If evidence is insufficient, replace the candidate from the deterministic reserve.

Do not emit `[file not found]` or similarly incomplete evidence as an acceptable review unit.

### Hard gate

- 400 evidence-complete units;
- 0 blind-field leaks;
- 0 evidence-empty/insufficient units;
- all referenced evidence paths valid.

### Mandatory error stop

Any evidence/blindness/path failure that cannot be satisfied by the authorized deterministic replacement pool → update trace + ledger, emit `ERROR_BLOCKED`, and wait for user approval.

---

## P1-13 — Hard-freeze V1

Generate:

```text
data/evaluation/v1/test_set_400_v1_manifest.jsonl
data/evaluation/v1/test_set_400_v1_sampling_report.json
data/evaluation/v1/test_set_400_v1_sha256.txt
data/evaluation/v1/review_packets/
data/evaluation/v1/label_template_v1.jsonl
```

### Freeze assertions

All must pass:

- exactly 400 total;
- exactly 200 per scanner;
- exactly 160 baseline + 40 delta per scanner;
- 0 duplicate finding IDs;
- 0 baseline/delta overlap;
- 0 development-set overlap;
- 0 evidence-empty units;
- all evidence paths valid;
- all delta records have valid provenance;
- all packets are blind;
- manifest SHA matches the exact frozen manifest.

An issues list may **never** coexist with successful freeze completion.

### Hard gate

Every assertion passes with an empty issues list.

### Mandatory error stop

Any freeze issue → update trace + ledger, emit `ERROR_BLOCKED`, and wait for user approval. Do not create a labeling checkpoint.

---

## P1-14 — Final pre-label quality, resume, integrity, and checkpoint

### Do

Run from `vulnerability-scanner/`:

```powershell
python -m pytest tests/ -q
ruff check src tests
mypy src
```

Then:

1. run the main command with `--resume`;
2. run it a second time;
3. verify the second invocation performs:
   - zero duplicate valid scanner runs;
   - zero duplicate valid O2 calls;
   - cached O2 reuse;
   - unchanged normalization/matching reuse;
   - unchanged frozen hashes.

4. Perform one controlled upstream invalidation test.
5. Verify only correct downstream stages invalidate.
6. Restore the controlled fixture.
7. Reverify protected V0/baseline hashes.
8. Finalize `PART1_PRE_LABEL_EXECUTION_TRACE.md`.
9. Create the labeling checkpoint document/state.

### Hard gate

All tests, resume checks, invalidation checks, protected hashes, and frozen V1 hashes pass.

### Mandatory error stop

Any failing test/lint/type check, duplicate work, bad invalidation, or hash change → update trace + ledger, emit `ERROR_BLOCKED`, and wait for user approval.

### Successful Part 1 output

Print only:

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

Selected local model:
<model and full digest>

Part 1 trace:
<path>

Resume command:
<command>
```

Then **STOP COMPLETELY**.

Do not generate labels.
Do not run real Experiment A/B.
Do not run final statistics.
Do not continue into Part 2.

---

# MANUAL LABELING STOP — OUTSIDE CURSOR

The user will provide the 400 blind review units to ChatGPT and manually establish ground truth.

Cursor must do nothing until the user provides the completed file:

```text
data/evaluation/v1/test_set_400_v1_gold.jsonl
```

Expected: exactly 400 labeled review IDs.

Only after the user explicitly instructs Cursor to resume with the completed gold file may Part 2 begin.

---

# PART 2 — AFTER THE 400 GROUND-TRUTH LABELS ARE SUPPLIED

At the start of Part 2 create:

```text
vulnerability-scanner/docs/experiments/v1/PART2_POST_LABEL_EXECUTION_TRACE.md
```

Do not modify the frozen V1 sample.

---

## P2-01 — Validate the supplied ground-truth file

### Do

Validate:

- exactly 400 records;
- every `review_id` unique;
- every `review_id` exists in frozen manifest;
- no missing review IDs;
- no extra review IDs;
- frozen manifest hash unchanged;
- test-set SHA unchanged;
- only allowed gold values;
- `uncertain` preserved explicitly.

Do not inspect labels to tune prompts, policies, model configuration, or sampling.

### Hard gate

The supplied gold file maps exactly and exclusively to the frozen 400 review units.

### Mandatory error stop

Any count/ID/hash/schema mismatch → update Part 2 trace + ledger, emit `ERROR_BLOCKED`, and wait for user approval.

---

## P2-02 — Join gold labels to frozen predictions

### Do

Join only through:

```text
gold.review_id
→ frozen manifest.finding_id
→ prediction.finding_id
```

Validate one-to-one/defined multiplicity rules and zero missing prediction joins.

Preserve `uncertain` according to the frozen analysis policy.

### Hard gate

Every analyzable gold record joins deterministically to its frozen finding/predictions with no guessed identity.

### Mandatory error stop

Any missing/duplicate/ambiguous identity join → update trace + ledger, emit `ERROR_BLOCKED`, and wait for user approval.

---

## P2-03 — Run Experiment A

### Do

Run the fully preimplemented native architecture experiment using the frozen gold set.

Generate required:

- per-finding outputs;
- aggregate metrics;
- per-scanner metrics;
- Skill-level metrics;
- runtime/error data.

Do not rerun scanners or valid Ollama work.

### Hard gate

All required Experiment A variants produce complete nonempty outputs from the frozen data.

### Mandatory error stop

Any missing variant/input/metric or unexpected rerun requirement → update trace + ledger, emit `ERROR_BLOCKED`, and wait for user approval.

---

## P2-04 — Run Experiment B and LLM stability analysis

### Do

Evaluate:

- Native;
- O1 components;
- O2;
- O3;
- O4;
- H1;
- H2;
- H3.

Use the same frozen gold set and frozen predictions.

Run LLM stability analysis from the previously recorded repeated/local-model results.

Do not rerun valid expensive LLM work merely to regenerate cached results.

### Hard gate

All required Experiment B and stability outputs are complete and traceable to frozen inputs.

### Mandatory error stop

Any missing prediction family, incompatible frozen artifact, metric inconsistency, or unexpected expensive rerun → update trace + ledger, emit `ERROR_BLOCKED`, and wait for user approval.

---

## P2-05 — Run final statistical analysis

### Do

Run the preimplemented:

- Skill-clustered bootstrap;
- repository-clustered sensitivity bootstrap;
- paired bootstrap;
- McNemar tests;
- Cochran's Q;
- multiple-comparison correction;
- effect sizes;
- 95% confidence intervals;
- 2-percentage-point TP-retention non-inferiority analysis.

Handle `uncertain` exactly according to the frozen analysis policy.

### Hard gate

All required statistical outputs complete without placeholder or silent omission.

### Mandatory error stop

Any invalid statistical input, failed method, missing comparison, or inconsistent sample accounting → update trace + ledger, emit `ERROR_BLOCKED`, and wait for user approval.

---

## P2-06 — Generate final reports and verify integrity

### Do

Generate final nonempty:

- Markdown;
- JSON;
- JSONL;
- CSV

reports covering:

- scanner/profile counts;
- Experiment A;
- Experiment B;
- O1/O2/policies;
- hybrid comparisons;
- LLM stability;
- statistical results;
- effect sizes/CIs;
- runtime;
- local computational token usage;
- failures/abstentions;
- limitations.

Then verify:

- protected V0 unchanged;
- committed baselines unchanged;
- frozen V1 unchanged;
- selected model digest unchanged;
- no cloud inference used;
- no valid scanner/Ollama work rerun unnecessarily;
- every report input traces to the frozen manifest/gold set.

### Hard gate

All final reports exist, are nonempty, internally consistent, and integrity checks pass.

### Mandatory error stop

Any integrity/report/provenance mismatch → update trace + ledger, emit `ERROR_BLOCKED`, and wait for user approval.

---

## P2-07 — Final project completion report

### Do

Finalize:

```text
vulnerability-scanner/docs/experiments/v1/PART2_POST_LABEL_EXECUTION_TRACE.md
```

and the detailed task ledger.

Return one concise final execution report containing:

- Part 1 and Part 2 step status;
- protected-hash confirmation;
- exact 735-Skill validation;
- scanner executables/versions/commits;
- Ollama version/local-only evidence;
- selected model/full digest;
- smoke/pilot/full-run status;
- findings per profile;
- Cisco Meta results;
- matching summary;
- O1/O2/O3/O4/H1/H2/H3 coverage;
- frozen 400-sample composition;
- V1 SHA-256;
- gold-label validation;
- Experiment A results;
- Experiment B results;
- stability results;
- statistical results;
- final report paths;
- confirmation that no paid/cloud LLM was used;
- every remaining limitation/blocker.

### Hard gate

All Part 1 and Part 2 required steps are `PASSED`, all integrity checks pass, and no unresolved blocker remains.

### Mandatory error stop

If any required final assertion is false → do not declare the project complete. Update trace + ledger, emit `ERROR_BLOCKED`, and wait for user approval.

### Successful endpoint

Only after the hard gate passes, print:

```text
V1_EXPERIMENT_COMPLETE

Part 1 trace:
<path>

Part 2 trace:
<path>

Frozen test-set SHA-256:
<hash>

Final report directory:
<path>

Protected baseline verification:
PASSED

Cloud/paid LLM inference:
NONE
```

---

# 4. Absolute prohibitions

Cursor must never:

- generate the 400 gold labels;
- infer missing gold labels;
- change the frozen sample after labeling begins;
- change the locked model/prompt/context policy after freeze;
- treat `uncertain` as TP/FP without the frozen policy;
- convert scanner/LLM failure into zero findings or `keep`;
- treat ambiguous matching as suppression;
- invent native deltas to fill quota;
- continue past a failed hard gate;
- auto-fix an unplanned mismatch without user approval;
- use a cloud/paid LLM;
- rerun expensive valid work unnecessarily;
- create a false checkpoint;
- declare completion with unresolved issues.

---

# 5. Execution priority

Cursor must optimize for this order:

```text
CORRECTNESS OF HARD GATES
→ REUSE OF VALID WORK
→ MINIMUM NECESSARY LOCAL-LLM CALLS
→ RESUMABILITY
→ SPEED
```

The project should finish quickly, but no speed optimization may weaken the frozen 400-sample validity, ground-truth independence, or final research reproducibility.
