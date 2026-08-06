# Vulnerable-Skills-Detector V1 — Recovery and Completion Plan for Cursor

## Audit verdict

The repository contains useful implementation work, but the latest V1 run is **not a valid labeling checkpoint**. It is a second invalid attempt caused by broken LLM integration and missing hard gates. Do not continue from the current `CHECKPOINT_LABELING_REQUIRED_V1` state.

### Valid or reusable work

Preserve and revalidate these items rather than rebuilding them unnecessarily:

- Protected baseline data and the original V0 archive. Current protected-hash verification passes, and the V0 manifest SHA-256 is still `190bbe5de478378aacd9db37f696b8c09fe93837f54f88a81aba0bba661f62cd`.
- The first invalid zero-Skill attempt archive and its audit document.
- Repository-root and UTF-8 utilities, subject to rerunning their tests.
- The Skill-manifest loader, subject to a fresh hard assertion that exactly 735 valid Skill directories load.
- Pinned scanner checkouts and virtual environments, after revalidating exact commits, executables, versions, `scan --help`, and dependency environments.
- Installed Ollama and downloaded `qwen3:8b` and `llama3.1:8b`, if they still exist locally and their full Ollama digests validate.
- Committed SS0 and CS1 baselines, but only after integrity and count validation.
- Existing deterministic evaluator, normalization, matching, sampling, packet, metrics, and statistics modules as starting points—not as completed stages.

### Invalid or incomplete work that must be redone

- The task ledger is stale and does not reflect the actual run.
- Model qualification used five synthetic prompts per trial, not the existing 50-example development set. The current model selection and lock are invalid.
- The stored model digest is truncated and the lock omits prompt/context hashes.
- `configs/scanner_profiles.yaml` still contains the invalid Cisco argument `--enable-llm`, while Python code defines a different profile source.
- The scanner runner bypasses the canonical Ollama adapter:
  - SkillSpector receives the wrong provider mapping.
  - Cisco receives `llama3.1:8b` instead of `ollama/llama3.1:8b`.
  - Cisco Meta is not consistently given the correct localhost base URL and dummy key.
- SkillSpector SS1 failed all 60 attempted runs.
- Cisco CS2 returned process success but its LLM analyzer failed because LiteLLM could not identify the provider.
- Cisco CS3 returned process success but Meta failed/fell open on all attempted runs.
- Failed per-Skill results were stored as completed, and smoke/pilot stages passed despite 100% failure.
- The orchestrator continued after hard-gate failures.
- Raw stdout/stderr are truncated, so important scanner exceptions were lost.
- Empty native outputs were normalized and matched as if every baseline finding were suppressed.
- O2 is a placeholder; O3/O4/H1/H2/H3 were not actually generated.
- Experiment B, LLM stability, statistics, and final reports remain placeholders or incomplete.
- The sampled V1 manifest contains 32 duplicate finding IDs and is based on invalid native deltas.
- Freeze recorded an issues list but still passed.
- The current labeling checkpoint is invalid and its required checkpoint document is absent.
- The test suite currently passes, but it does not test the failed semantics above.

---

# Ready-to-paste Cursor instruction

You are continuing the V1 experiment in `Vulnerable-Skills-Detector-1`.

Your goal is to repair the current implementation and execute the experiment to the first legitimate stopping point:

- `CHECKPOINT_LOCAL_LLM_SETUP_REQUIRED` only when local Ollama genuinely cannot be made operational; or
- `CHECKPOINT_LABELING_REQUIRED_V1` only after a valid, blind, evidence-complete, duplicate-free 400-unit V1 test set exists.

Do not generate gold labels. Do not use any paid, hosted, or cloud LLM. All experiment LLM traffic must go only to local Ollama on `127.0.0.1:11434`.

The original 38-task plan remains the source of truth for scientific requirements and acceptance criteria. This continuation plan tells you how to recover efficiently from the current invalid state without restarting valid work.

## Global execution rules

1. Work through the packages below strictly in order. Finish and validate one package before starting the next.
2. Update `vulnerability-scanner/docs/experiments/v1/TASK_EXECUTION_LEDGER.md` immediately before and after every package, while retaining mapping to original Tasks 1–38.
3. Never mark a stage or Skill complete because a subprocess merely returned exit code 0. Validate semantic success.
4. When a hard gate fails, fix it and rerun that package. Do not continue downstream.
5. Reuse only artifacts whose hashes, provenance, and semantic validity pass current code.
6. Do not overwrite protected baselines or the V0 archive.
7. Use UTF-8 explicitly for all text/JSON I/O and PowerShell-compatible commands.
8. Avoid broad refactors. Repair existing modules and add focused tests.
9. In this extracted repository, Git may show extensive CRLF-only churn. Do not stage or commit unrelated line-ending changes. Confirm each substantive diff.
10. Add a Windows keep-awake guard around the long experiment command, using `SetThreadExecutionState` through Python `ctypes`, and restore the previous state on exit. It must require no administrator privileges and do nothing on non-Windows systems.

## Package 1 — Recover and quarantine the second invalid attempt

1. Verify protected hashes before moving anything.
2. Preserve the existing first invalid archive.
3. Archive the current invalid second attempt under new, clearly named paths such as:
   - `data/evaluation/archive/invalid_v1_llm_adapter_and_gate_attempt_20260805/`
   - `results/experiments/archive/invalid_v1_llm_adapter_and_gate_attempt_20260805/`
4. Archive at least the current V1 manifest, sample report, SHA file, review packets, label template, current state, invalid scanner runs, empty native normalized outputs, matching, evaluator outputs, policies, metrics, and false checkpoint artifacts.
5. Write `docs/experiments/v1/INVALID_V1_LLM_ATTEMPT_AUDIT.md` documenting:
   - SS1: 60 failed attempts;
   - CS2: LiteLLM provider failure caused by missing `ollama/` prefix;
   - CS3: Meta fail-open/UNKNOWN failure;
   - failed results marked completed;
   - empty outputs normalized and matched;
   - false suppression deltas;
   - 32 duplicate finding IDs;
   - freeze and checkpoint incorrectly passed.
6. Create a fresh V1 state file. Do not reuse per-Skill completion records from the invalid attempt.
7. Keep valid protected baselines, scanner installations, model files, and independently valid preflight evidence outside the invalid archive.

**Gate:** protected hashes still pass; invalid V1 products no longer occupy active V1 paths; fresh state has no completed scanner/evaluation/sampling stages.

## Package 2 — Repair the execution foundation

Fix these modules before any new LLM run:

- `src/vuln_scanner/experiment/state.py`
- `src/vuln_scanner/experiment/orchestrator_v1.py`
- `src/vuln_scanner/experiment/scanner_exec.py`
- `src/vuln_scanner/experiment/ollama_adapter.py`
- `configs/scanner_profiles.yaml`

Required changes:

1. Support exactly: `pending`, `running`, `completed`, `partial`, `failed`, `blocked`, `invalidated`.
2. Define a real stage DAG. Every stage record must include upstream stage IDs, direct input hashes, relevant source/config/prompt hashes, scanner executable/commit/version, and local model identity/digest where applicable.
3. Include changes under experiment, filters, scanners, configs, authored taxonomy, prompts, and policies in invalidation hashes.
4. Store per-Skill state as success, failed, timeout, parser_failed, blocked, or abstained. Only semantic success is resumable as completed.
5. Verify the result file hash when deciding whether to skip a completed Skill.
6. A scanner stage can complete only when `requested > 0`, every requested Skill has an explicit terminal state, and `completed + failed == requested`.
7. Smoke/pilot error rate above 5% must raise a hard failure, not a warning.
8. A failed stage must stop the run loop. Downstream stages must not execute.
9. A blocked, absent, empty, parser-failed, or fail-open profile must not be normalized or matched.
10. Preserve complete stdout and stderr—not truncated strings—along with exit code, parsed JSON, parser status, duration, retry, analyzers, model name, and full digest.
11. Make one profile source authoritative. Prefer loading `configs/scanner_profiles.yaml` and validating it against each pinned scanner’s actual `scan --help`. Remove duplicate hard-coded definitions or generate them from the YAML.
12. Replace all actual scanner CLI uses of `--enable-llm` with Cisco’s `--use-llm`. Add a repository-wide test that parses scanner argument definitions and fails on `--enable-llm` as a scanner argument.
13. Delete the duplicate environment mapping in `scanner_exec.py`. Use one canonical adapter for all profiles:
    - SkillSpector: provider `openai`, model selected model, base `http://127.0.0.1:11434/v1`, dummy key `ollama-local`.
    - Cisco LLM: model `ollama/<selected-model>`, base `http://127.0.0.1:11434`, dummy key.
    - Cisco Meta: same `ollama/` model/base/dummy key.
    - O2: OpenAI-compatible localhost `/v1` endpoint and dummy key.
14. Hard-fail any non-localhost experiment LLM URL and any automatic cloud fallback.
15. Make required quality commands fail the stage on nonzero exit.
16. Implement `--resume`, `--force-stage`, and `--invalidate-downstream` against the real DAG.

**Focused tests before continuing:** state semantics; failed subprocess; semantic Cisco LLM failure; Meta UNKNOWN/fail-open; blocked normalization; output-hash resume; downstream invalidation; profile-source synchronization; localhost-only enforcement.

## Package 3 — Revalidate preflight, hardware, and local models

1. Rerun root discovery, UTF-8 tests, and the real manifest loader. Hard-assert exactly 735 valid Skill directories.
2. Revalidate pinned scanner commits, executables, versions, `scan --help`, and dependency environments without reinstalling valid environments.
3. Correct hardware detection. A failed `nvidia-smi` command is not a GPU name. Store `null` plus a detection note when no supported GPU is found.
4. Confirm Ollama CLI and API, `OLLAMA_NO_CLOUD=1`, and loopback-only binding. Record evidence, not only configuration claims.
5. Inventory both candidate models using full Ollama digests, size, quantization, parameters when reported, and pull status.
6. Repair health checks so each candidate is tested through both:
   - native Ollama API; and
   - OpenAI-compatible `/v1/chat/completions`.
7. Validate the exact classification schema, not merely JSON parseability.
8. Replace the current five-prompt synthetic qualification. Use the existing 50-example development set, both candidates, the same prompt/context builder, and three complete trials per candidate.
9. Compute every required development metric and select one model by the original priority order.
10. Create a new lock with full model digest, quantization, Ollama version, temperature, context policy, all prompt hashes, and adapter version. Invalidate all LLM/downstream work when any locked field changes.

**Gate:** one legitimately selected and fully locked local model. If neither 8B model passes and 14B is infeasible, stop only at `CHECKPOINT_LOCAL_LLM_SETUP_REQUIRED` with exact evidence and resume instructions.

## Package 4 — One-Skill integration probes

Before smoke tests, run one fixed Skill at a time and preserve full raw evidence:

1. SS0: confirm static SkillSpector success.
2. CS0 and CS1: confirm Cisco static/behavioral success.
3. SS1: capture the complete current exception, repair its environment/dependencies, and verify that the selected Ollama model was actually called.
4. CS2: verify no `LLM_ANALYSIS_FAILED`, no LiteLLM provider error, and that `ollama/<model>` was used.
5. CS3: verify Meta is explicitly executed; expected fields exist; there is no UNKNOWN fail-open, failure summary, or hidden fallback.
6. O2: verify localhost-only request, exact model digest, strict TP/FP/uncertain output, raw response, prompt hash, cache key, and abstention on malformed output.

**Gate:** all seven probes pass semantic validation. Do not start smoke tests before this gate.

## Package 5 — Smoke and pilot gates

1. Run 10 fixed Skills for all required scanner profiles and O2.
2. Verify exact attempted counts, per-Skill raw files, attribution, JSON/schema parsing, no profile contamination, consistent digest, Meta success, and zero repeated valid work on resume.
3. Run 50 fixed Skills for all required scanner profiles and O2.
4. Enforce the below-5% error threshold, excluding only documented infrastructure outages.
5. Record local runtime, locally reported token usage as computational usage, CPU/GPU utilization when available, and failures.
6. Validate committed SS0 and CS1 counts and run CS0 freshly. Never derive CS0 from CS1.

**Gate:** smoke and pilot pass for every profile. A single blocked/failed profile blocks the full run.

## Package 6 — Full six-profile execution

1. Reuse SS0 and CS1 only after integrity validation.
2. Run/complete all 735 Skills for SS1, CS0, CS2, and CS3 using the locked model.
3. Store one complete raw result per Skill per profile.
4. On timeout, save it, retry once at double timeout, then store final failure and continue.
5. A failure is never equivalent to zero findings.
6. Verify `--resume` performs zero duplicate valid scans and only retries eligible failures according to explicit policy.

**Gate:** each profile reports requested, completed, failed, timeout, parser-failed, blocked, and finding counts with all 735 Skills accounted for.

## Package 7 — Normalize, match, and evaluate

1. Normalize only real valid outputs, profile by profile, with zero cross-scanner contamination.
2. Populate all required finding identity, provenance, taxonomy, scanner, and model fields.
3. Preserve unique instance identity; prevent silent overwrites and unexplained collisions.
4. Implement guaranteed maximum-weight bipartite matching. Do not silently fall back to greedy matching; make the required solver a pinned project dependency or implement an equivalent exact algorithm.
5. Enforce native matching preconditions and produce all five required comparisons.
6. Run O1 components independently and preserve each vote.
7. Implement and run real O2 on controlled baseline candidate pools using only the locked local model; no placeholders and no gold-label access.
8. Generate actual per-finding O3, O4, H1, H2, and H3 predictions with complete policy metadata.

**Gate:** no empty placeholder directories; every expected candidate has an explicit prediction, failure, or abstention record; blocked profiles cannot create suppression claims.

## Package 8 — Finish post-labeling analysis code before sampling

Using synthetic fixtures only, fully implement and test:

1. Manifest join: `review_id -> finding_id`; gold labels keyed by review ID; predictions keyed by finding ID.
2. Experiment A and B variants required by the original plan.
3. All required metrics, including separate handling of gold `uncertain` and correct naming of pooled relative recall.
4. Skill- and repository-clustered bootstrap, paired bootstrap, McNemar, Cochran’s Q, correction, effect sizes, 95% intervals, and 2-point TP-retention non-inferiority.
5. LLM stability analysis.
6. Real Markdown, JSON, JSONL, and CSV report generators. No heading-only placeholder reports.
7. Future resume validation for exactly 400 labels without rerunning valid scanner/Ollama work.

**Gate:** synthetic fixture tests create complete nonempty outputs and verify the identity join.

## Package 9 — Sample, build packets, and freeze

1. Build exactly 200 SkillSpector and 200 Cisco units, each with 160 baseline and 40 valid native-delta/disagreement units.
2. Select delta first and require valid native provenance.
3. Exclude development IDs, delta/baseline overlap, already selected IDs, and duplicate evidence instances.
4. Apply adaptive tiers and seed `20260805`; record the tier per scanner and stratum.
5. Generate blind packets with all required context, traces, related files, metadata, and cross-file/package evidence.
6. Replace any evidence-incomplete candidate.
7. Freeze must raise and fail on any issue. An issues list may never coexist with completed status.
8. Hard assertions: exactly 400; 200 per scanner; 160/40 per scanner; zero duplicate instance IDs; zero stratum overlap; zero dev overlap; zero evidence-empty units; valid paths; valid native provenance; all packets blind.

**Gate:** all freeze assertions pass and the SHA file matches the exact frozen manifest.

## Package 10 — Final quality, resume, and checkpoint

1. Run from `vulnerability-scanner/`:
   - `python -m pytest tests/ -q`
   - `ruff check src tests`
   - `mypy src`
2. Run the main command twice with `--resume`; the second run must perform zero duplicate valid scanner or Ollama work and preserve hashes.
3. Change one controlled upstream fixture, verify exact downstream invalidation, and restore it.
4. Verify protected hashes again.
5. Create the complete checkpoint document and execution report required by original Tasks 36 and 38.
6. Print only the required `CHECKPOINT_LABELING_REQUIRED_V1` block and stop. Do not generate labels.

## Expected resume command

Run from `vulnerability-scanner/` in PowerShell after the selected model has been validly locked:

```powershell
$env:OLLAMA_NO_CLOUD="1"
$env:VSD_LLM_PROVIDER="ollama"
$env:VSD_LLM_MODEL="<selected-model-from-lock>"
$env:VSD_LLM_BASE_URL="http://127.0.0.1:11434"
$env:VSD_LLM_TEMPERATURE="0"
$env:VSD_LLM_MAX_CONCURRENCY="1"
$env:VSD_LLM_API_KEY="ollama-local"
python -m vuln_scanner experiment run --config configs/native_vs_external_v1.yaml --resume
```

Do not manually force the current false labeling checkpoint. Repair and invalidate from the earliest affected stage, then let the corrected DAG determine downstream reruns.

## Final response requirements

At the legitimate checkpoint, return:

- status of original Tasks 1–38;
- exact paths of both invalid-attempt archives;
- protected hash verification;
- 735-Skill validation;
- test/lint/type-check results;
- scanner commits, versions, and executables;
- Ollama local-only evidence;
- selected model and full digest;
- smoke, pilot, and full-run status/counts per profile;
- Meta success/failure counts;
- normalization, matching, O1/O2/policy coverage;
- sample composition and tiers;
- confirmation of zero duplicates and zero evidence-empty units;
- frozen V1 SHA-256 and review paths;
- exact resume command after labels;
- every remaining blocker.
