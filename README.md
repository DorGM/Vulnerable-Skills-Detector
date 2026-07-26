# Vulnerable-Skills-Detector

A tool for detecting vulnerable skills in AI agent systems.

## Part 1 — Skill discovery scanner

The discovery-and-acquisition pipeline lives in
[`skill-scanning-crawler/`](skill-scanning-crawler/README.md). It crawls GitHub,
ranks skill-publishing repos by stars, and downloads the top-50 repos' skills.

**The discovered skills are saved (and committed) under
[`skill-scanning-crawler/data/`](skill-scanning-crawler/data/):**

- `data/snapshots/<owner>/<repo>/<skill>/<sha8>/` — the skill files themselves
  (`SKILL.md` + auxiliary files), frozen at a pinned commit SHA.
- `data/manifests/skills.jsonl` — index of all 735 skills (path, SHA, content
  hash, file list, snapshot path).
- `data/reports/` — discovery/dataset summaries.

See the [crawler README](skill-scanning-crawler/README.md#output-layout) for the
full layout.

## Part 2 — Vulnerability scanning and cross-scanner gap analysis

Lives in [`vulnerability-scanner/`](vulnerability-scanner/README.md). It runs two published
skill scanners — [NVIDIA SkillSpector](https://github.com/NVIDIA/SkillSpector) and
[Cisco skill-scanner](https://github.com/cisco-ai-defense/skill-scanner) — over all 735
skills, measures where they agree, and identifies which threat classes neither covers.

The two scanners share no rule IDs, no categories, and no framework vocabulary, so comparing
them directly returns zero overlap and means nothing. Both are instead mapped onto neutral
reference taxonomies (OWASP LLM Top 10, OWASP Top 10 for Agentic Applications, MITRE ATLAS)
and compared through those.

| | |
|---|---|
| Corpus | 735 skills × 2 scanners, 0 errors |
| Findings | SkillSpector 2,309 security · Cisco 508 security + 615 advisory |
| Agreement — exact match / embeddings / **taxonomy** | 0 · 75 · **127** |
| Confirmed coverage gap | **4 of 20** mappable reference classes |

A wider denominator including scoped MITRE ATLAS techniques gives 47 of 76, but that figure is
reported as a sensitivity result rather than a finding: the technique subset behind it was
selected by keyword and has never been reviewed, so `analyze` declines to call it a confirmed
gap until it is.

- [`vulnerability-scanner/README.md`](vulnerability-scanner/README.md) — setup and commands
- [`docs/FINDINGS.md`](vulnerability-scanner/docs/FINDINGS.md) — 25 findings, indexed by status
- [`docs/HANDOFF.md`](vulnerability-scanner/docs/HANDOFF.md) — current state and what remains
- [`docs/ATLAS_SUBSET_REVIEW.md`](vulnerability-scanner/docs/ATLAS_SUBSET_REVIEW.md) — the open
  reviewer decision on that denominator

The reference scanners are installed from pinned commits by `scanners/setup.sh` and are
gitignored — third-party code is not vendored into this history.

## Specification

[`PROJECT_SPEC.md`](PROJECT_SPEC.md) holds the brief for both parts.
