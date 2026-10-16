# TALK11 Dual-AI automation — operator setup

Status: **proposed configuration / NOT ACTIVE** until this PR is merged and its GitHub Actions variables, secret and local Antigravity integration are configured and tested.

## What the GitHub workflows do

1. `dual-ai-gated-autofix.yml` responds only when repository owner `KGD-Lucifer` applies the `ai-fix` label to an **open** Issue, or manually dispatches an already labeled Issue. It also requires `ENABLE_DUAL_AI_AUTOFIX=true`.
2. The Codex action reads that Issue, proposes code changes on a dedicated `ai/codex-issue-<n>` branch, runs static smoke checks, then opens a **review-only PR**. It never merges into `main` automatically.
3. `dual-ai-pr-review.yml` runs a **static Codex cross-review** for same-repository PRs on approved events or manual dispatch when `ENABLE_DUAL_AI_REVIEW=true`. It checks out trusted `main`, **never checks out or executes PR code**, and posts review comments. Bot-created PRs are explicitly dispatched by the intake workflow.
4. Antigravity **local runtime review/fix is not configured by these workflows**. This requires local setup below. Do not claim automatic two-way correction or DUAL PASS until that integration is working.

## One-time GitHub configuration (owner)

- Merge this reviewed PR (not directly on main).
- In **Settings → Secrets and variables → Actions** create secret `OPENAI_API_KEY` (provider API billing is separate from ChatGPT subscription).
- In **Settings → Secrets and variables → Actions → Variables**, create:
  - `ENABLE_DUAL_AI_AUTOFIX=true`
  - `ENABLE_DUAL_AI_REVIEW=true`
  Both must remain unset/false until permission and cost review is complete.
- In **Settings → Actions → General**, give the workflow the necessary `GITHUB_TOKEN` permissions and enable **Allow GitHub Actions to create and approve pull requests** if available. The YAML requests specific token permissions; repository/org policy must allow them.
- Create an Issue label `ai-fix`. Review any Issue carefully before applying this trusted execution label.
- First test using a small harmless Issue with `ai-fix`; verify that a proposed PR and a review comment are created and **no automated merge occurs**.

## Antigravity integration to implement locally

Use the official Antigravity CLI headless interface (`agy -p "..."`) only after verifying the installed CLI and interactive authentication. Choose **one** secure local trigger:

- A Task Scheduler job on the Windows PC that polls GitHub with authenticated `gh` for PRs/issues needing local QA, keeps a deduplication cursor in local state, and calls `agy -p`.
- A narrowly scoped local webhook listener that verifies GitHub signatures, deduplicates delivery IDs, and queues bounded jobs. Never expose an unauthenticated local HTTP runner.

For each proposed PR, check out an **isolated worktree/branch** (do not alter the active editor worktree), verify trusted PR ownership and permissions, run model/video/audio/browser QA with local assets, and comment machine-readable PASS/FAIL results on PR/Issue. If FAIL, Antigravity may propose a **new follow-up PR/commit on its own branch**, but never push blindly to `main`. Limit AI response/fix rounds to 2 and request human review when unresolved.

**Security:** This repository is public; do not run untrusted PR code or public fork workflows on a persistent self-hosted GitHub runner. Prefer the Windows local polling mechanism with credentials held on the operator PC. Never post API keys, tokens or private sample videos in Issues, Actions logs or PR diffs. Never use `agy --dangerously-skip-permissions`; explicitly allow only necessary workspace, `git`, and project test commands in Antigravity settings.

## DUAL PASS evidence

- Codex: source-level review PASS on the specific commit SHA with affected lines/issues resolved.
- Antigravity: actual runtime PASS on that same SHA, including AI matting/video, alpha export, waveform from real audio, subtitle timing, preview/export ducking, regression and performance tests.
- Human approval and merge after both pass. Check previous `#1` review blockers; keep the main tool stable.

Useful docs:
- https://github.com/openai/codex-action
- https://www.antigravity.google/docs/cli/headless/
- https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions
