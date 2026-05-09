---
phase: P5
phase_name: Public surfaces rewrite
initiative: I66
date: 2026-05-09
severity: HIGH
kind: security_inbox
status: operator_action_required_immediate
addressed_to: operator (CBO/O5-1)
governance: discovered during I66 P5 drift-gate validation; surfaced per akos-agent-checkpoint-discipline.mdc + akos-governance-remediation.mdc SoC/Security
---

# OPERATOR SECURITY INBOX — Leaked Google Cloud credentials in `boilerplate/`

> **Severity: HIGH.** A Google Cloud service-account credentials JSON file is committed in `boilerplate/app/`, with a real RSA private key exposed in source. This was discovered during I66 P5 brand-jargon drift-gate scanning (the validator caught `OAuth2` tokens in the file's URLs, which led to inspecting it). The agent has **not auto-remediated** — credential rotation requires operator action and out-of-AKOS-scope access (Google Cloud Console, Vercel env var settings, git history rewriting). This note surfaces the issue with maximum visibility for immediate operator action.

## What is exposed

**File**: `boilerplate/app/hlk-gtm-0001-365101c1624d.json`

**Status** (as of 2026-05-09):

- Committed in `boilerplate` repo on branch `i32-akos-mirror-seed` (and likely `main` and other branches; needs `git log` audit).
- Present in working tree.
- Contains:
  - `type: "service_account"`
  - `project_id: hlk-gtm-0001` (Google Tag Manager / GCP project)
  - `private_key_id: 365101c1624d7dda1e305dcd710a4192140f6605`
  - **`private_key`**: a real RSA-2048 private key in plain text (PEM-encoded).
  - `client_email: 626443357224-compute@developer.gserviceaccount.com`
  - URL fields confirming OAuth2 endpoints (which is what the validator caught).

**Implication**: anyone with access to the repository can authenticate as this service account and access whatever GCP resources it has IAM permissions on. If the repo is public on GitHub, this is **publicly exposed**.

## Immediate actions required (operator-driven)

### Step 1 — Revoke the credential (≤ 5 minutes)

1. Go to <https://console.cloud.google.com/iam-admin/serviceaccounts?project=hlk-gtm-0001>.
2. Find service account `626443357224-compute@developer.gserviceaccount.com` (or whichever account this `private_key_id` belongs to).
3. Under "Keys", find the key with ID `365101c1624d7dda1e305dcd710a4192140f6605`.
4. Click "Delete" to revoke it.

This makes the leaked key non-functional immediately. **Do this first**, before any other remediation.

### Step 2 — Audit access logs (≤ 30 minutes)

1. Go to <https://console.cloud.google.com/logs/query?project=hlk-gtm-0001>.
2. Filter for `protoPayload.authenticationInfo.principalEmail="626443357224-compute@developer.gserviceaccount.com"`.
3. Look for any access between when the key was committed (find via `git log --follow boilerplate/app/hlk-gtm-0001-*.json`) and when revoked in Step 1.
4. If unusual access patterns appear, escalate per Holistika incident-response (no SOP exists for this yet — flag as P3-followup for a SOP-SEC_INCIDENT_RESPONSE_001 SOP).

### Step 3 — Generate replacement credential (if still needed)

If the GCP project / service account is still in active use:

1. Generate a new key in the GCP console for the same service account.
2. Store the new key as a **Vercel environment variable** (encrypted at rest), not as a file.
3. Update boilerplate code that previously read the JSON to instead read the env var (typically `process.env.GCP_SA_KEY` decoded from base64 or stored as JSON string).

### Step 4 — Remove file from working tree + add to .gitignore

After replacement is in place:

1. `git rm boilerplate/app/hlk-gtm-0001-365101c1624d.json`.
2. Add to `boilerplate/.gitignore`:
   ```
   # Service-account credentials — never commit
   *.json
   !package.json
   !tsconfig.json
   !*.config.json
   !*.example.json
   # Or specifically:
   /app/hlk-gtm-*.json
   /credentials/
   ```

### Step 5 — Remove from git history (most-thorough remediation)

The credential remains in git history even after `git rm`. To fully remove:

**Option A** (BFG Repo-Cleaner — easier):

```bash
java -jar bfg.jar --delete-files hlk-gtm-0001-365101c1624d.json boilerplate-mirror.git
cd boilerplate-mirror.git && git reflog expire --expire=now --all && git gc --prune=now --aggressive
git push --force
```

**Option B** (`git filter-branch` — built-in but slower):

```bash
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch boilerplate/app/hlk-gtm-0001-365101c1624d.json" \
  --prune-empty --tag-name-filter cat -- --all
git push --force --all
```

**Note**: Force-pushing rewrites collaborator clones. Since boilerplate is a collaboration repo with PR history, this is disruptive. Operator decides whether the operational benefit (full removal from history) is worth the disruption (collaborators must re-clone). The minimum-viable mitigation is **Step 1 revocation** which makes the key non-functional regardless of whether it remains in history.

## Why agent did not auto-remediate

Per `akos-agent-checkpoint-discipline.mdc` and `akos-governance-remediation.mdc` §SoC/Security:

- **No SoC for credential remediation**: Google Cloud Console + Vercel env var management requires interactive operator authentication outside AKOS scope.
- **History-rewrite irreversible**: a force-push rewrites the boilerplate repo's history and disrupts collaborators. The agent does not autonomously make irreversible repository-wide changes.
- **Visibility before action**: making this leak as visible as possible (this inbox note + flagged in P5 increment 2 commit message) is more valuable than silently removing the file from working tree, which could mask the issue without fixing it.

## Cross-references

- I66 P5 increment 2 commit (`d7aa88ba` in boilerplate): mentions this issue in commit message footer.
- I66 P3 H1 pause record [`p3-pause-record-2026-05-08.md`](p3-pause-record-2026-05-08.md) §"Decided not to do" — flagged the file then; deferred remediation to operator.
- Future deliverable: `SOP-SEC_INCIDENT_RESPONSE_001.md` (does not exist; should be drafted in a future I-NN security-ops initiative).
- Risk register R-IH-66-XX: this incident may warrant a new risk register row for "credential-leak detection coverage".

## Sign-off needed from operator

Operator confirms before this inbox is marked resolved:

1. ☐ Step 1 — Credential revoked in GCP Console.
2. ☐ Step 2 — Access logs audited; no unusual access (or incident response triggered if found).
3. ☐ Step 3 — Replacement credential issued + stored in Vercel env var (or service-account decommissioned if no longer needed).
4. ☐ Step 4 — File removed from working tree + .gitignore updated.
5. ☐ Step 5 — Git history remediation decision made (force-push removal vs. accept-in-history with revoked key as non-blocking).
6. ☐ Future deliverable: SOP-SEC_INCIDENT_RESPONSE_001 chartered.

When all six items confirmed, this inbox file's `status:` frontmatter changes from `operator_action_required_immediate` to `resolved` and a brief resolution note is appended below.

## Resolution log (operator fills in as steps complete)

`[empty]`
