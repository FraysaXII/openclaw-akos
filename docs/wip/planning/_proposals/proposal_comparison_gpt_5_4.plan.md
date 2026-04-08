# Proposal Comparison -- OpenCLAW-AKOS

This document compares the two proposals currently in `docs/wip`:

- `improvement_proposal_gpt_5_4.md`
- `improvement_proposal_aggressive_gpt_5_4.md`

---

## Executive Summary

### Proposal A: Operator-First

This is the **safer, more production-pragmatic** plan.

It prioritizes:

- repo-to-runtime parity
- role-safe capability enforcement
- dashboard-first usability
- lightweight memory and workflow improvements
- browser/live testing as release gates

This is the better choice if your main goal is:

> make the current system actually behave like the architecture says it should, then steadily improve UX and operations.

### Proposal B: Aggressive Autonomy-First

This is the **larger-upside, higher-complexity** plan.

It prioritizes:

- runtime convergence
- workflow-native execution
- task graphs and parallel execution lanes
- richer evidence retrieval
- dashboard as an operations cockpit
- release-grade eval infrastructure

This is the better choice if your main goal is:

> turn AKOS into a more competitive agent platform with stronger product differentiation.

---

## Side-by-Side Comparison

| Dimension | Proposal A -- Operator-First | Proposal B -- Aggressive Autonomy-First |
| :--- | :--- | :--- |
| Primary goal | Make the live product trustworthy and consistent | Build a more advanced agent platform and product moat |
| Best for | Stable production baseline | Bigger long-term differentiation |
| Core thesis | Fix runtime parity, safety, UX, and ops first | Build workflows, orchestration, retrieval, and eval as a platform |
| Complexity | Moderate | High |
| Delivery risk | Lower | Higher |
| Time to user-visible payoff | Fast | Medium |
| Time to strategic upside | Medium | High |
| Focus on dashboard UX | Strong | Very strong |
| Focus on runtime sync | Strong | Strong |
| Focus on workflows | Moderate | Very strong |
| Focus on parallel execution | Limited / careful | Explicit priority |
| Focus on retrieval/memory | Lightweight, pragmatic | More ambitious but still non-GraphRAG |
| Focus on release gates | Strong | Very strong |
| Operational burden | Lower | Higher |
| Documentation burden | Moderate | Higher |

---

## Decision Matrix (Scores 1–5)

Scores are 1 (low/weak) to 5 (high/strong). Higher is better unless the criterion is inverted.

| Criterion | Weight | A: Operator-First | B: Aggressive | Notes |
| :--- | :---: | :---: | :---: | :--- |
| **Time to value** | 1.2 | **5** | 3 | A delivers user-visible payoff faster |
| **Implementation risk** (5 = lowest risk) | 1.0 | **5** | 3 | A is safer to execute |
| **Product differentiation** | 1.0 | 3 | **5** | B creates stronger long-term moat |
| **Operator ergonomics** | 1.0 | 4 | **5** | B pushes harder on dashboard UX |
| **Long-term scalability** | 0.8 | 4 | **5** | B has more runway for platform growth |
| **Maintenance burden** (5 = lowest) | 1.0 | **5** | 3 | A is simpler to sustain |
| **Fit: "make it solid"** | 1.2 | **5** | 3 | A better for stable production baseline |
| **Fit: "make it standout"** | 1.0 | 3 | **5** | B better for platform differentiation |
| **Browser/live eval depth** | 0.8 | 4 | **5** | B formalizes eval culture more fully |
| **Workflow maturity** | 0.8 | 3 | **5** | B makes workflows a core product primitive |

### Weighted Totals

| Goal | A: Operator-First | B: Aggressive |
| :--- | :---: | :---: |
| **Prioritize stability and speed** | **22.0** | 13.2 |
| **Prioritize differentiation and scale** | 18.8 | **27.0** |

*Calculation: sum of (Score × Weight) for the subset of criteria per goal. The “stability” total emphasizes Time to value, Implementation risk, Maintenance burden, and Fit for “make it solid”. The “differentiation” total emphasizes Product differentiation, Operator ergonomics, Long-term scalability, Fit for “make it standout”, Browser/live eval depth, and Workflow maturity.*

### Quick Takeaway

- **A wins** if your primary driver is: ship faster, lower risk, easier to maintain.
- **B wins** if your primary driver is: stronger product identity, workflow-native UX, platform upside.

---

## By Decision Category

### 1. Runtime Parity

| Question | Proposal A | Proposal B |
| :--- | :--- | :--- |
| Does it fix repo-to-runtime drift? | Yes, as the first and biggest priority | Yes, also first priority |
| Does it force all 4 agents into the live runtime? | Yes | Yes |
| Does it clean up startup/workspace hydration issues? | Yes | Yes |

**Verdict:** both proposals agree strongly here. This is non-negotiable.

### 2. Role Safety

| Question | Proposal A | Proposal B |
| :--- | :--- | :--- |
| Enforce read-only Architect at the capability layer? | Yes | Yes |
| Add policy-backed role matrix? | Yes | Yes |
| Add auditability for capability drift? | Yes | Yes |

**Verdict:** also non-negotiable in both.

### 3. Dashboard UX

| Question | Proposal A | Proposal B |
| :--- | :--- | :--- |
| Health/readiness surface | Yes | Yes |
| Onboarding / first-run improvements | Yes | Yes |
| Checkpoint / progress UI | Moderate | Strong |
| Approval inbox | Nice-to-have | Stronger priority |
| Dashboard as true command center | Partial | Explicit goal |

**Verdict:** Proposal B pushes harder on product UX.

### 4. Workflows

| Question | Proposal A | Proposal B |
| :--- | :--- | :--- |
| Named workflows | Yes, but lighter | Yes, a central pillar |
| Slash commands / launchers | Suggested | Core product behavior |
| Task graphs | Not central | Core concept |
| Parallel workflow lanes | Deferred / cautious | Explicitly planned |

**Verdict:** if workflows are central to your vision, Proposal B wins.

### 5. Retrieval and Memory

| Question | Proposal A | Proposal B |
| :--- | :--- | :--- |
| Avoid GraphRAG | Yes | Yes |
| Memory packs | Yes | Yes |
| Context pinning | Yes | Yes |
| Source registry / citations | Moderate | Stronger emphasis |
| Evidence retrieval layer | Light | More ambitious |

**Verdict:** Proposal B is stronger for research-heavy and evidence-heavy use cases.

### 6. Testing and Evals

| Question | Proposal A | Proposal B |
| :--- | :--- | :--- |
| Offline regression lane | Yes | Yes |
| Browser/gateway smoke lane | Yes | Yes |
| Live provider/model lane | Yes | Yes |
| Workflow-level evals | Limited | Strong |
| Langfuse-scored release gates | Suggested | Stronger priority |

**Verdict:** Proposal B is more complete if you want a formal eval culture.

---

## Recommended Choice by Scenario

### Choose Proposal A if:

- you want the highest-confidence next step
- you care most about fixing what users will feel today
- you want lower implementation risk
- you want a stable baseline before expanding autonomy
- your main concern is runtime truth, safety, and operator usability

### Choose Proposal B if:

- you want to invest in a stronger long-term product identity
- you expect workflows and repeated trajectories to be central
- you want the dashboard to become an operations cockpit
- you are willing to accept more moving parts for larger upside
- you plan to keep iterating AKOS as a platform, not only a repo

---

## My Recommendation

If I were making the decision for real execution, I would recommend:

### Default recommendation: **Proposal A first**

Why:

- the live browser state shows that runtime parity and capability enforcement are still the highest-leverage gaps
- the dashboard currently exposes operational drift that should be fixed before deeper autonomy is layered on
- Proposal A addresses the exact pain you are already feeling as a user/operator

### Then selectively borrow from Proposal B

The best hybrid path is:

1. execute Proposal A phases 1-3 fully
2. then pull in from Proposal B:
   - workflow launcher UI
   - reusable workflow specs
   - source registry / citations
   - browser/live eval release gate
3. defer true parallel lanes until role safety and runtime sync are rock solid

This gives you:

- a safer short-term path
- a strong medium-term product path
- less risk of building impressive but unstable complexity

---

## Simplified Decision Rule

If you want the shortest rule possible:

- **Choose Proposal A** if the priority is: “make it solid”
- **Choose Proposal B** if the priority is: “make it standout”

---

## Worktree / File Location Note

These files were created in the currently active worktree:

- `docs/wip/improvement_proposal_gpt_5_4.md`
- `docs/wip/improvement_proposal_aggressive_gpt_5_4.md`
- `docs/wip/proposal_comparison_gpt_5_4.md`

If you ran other models in other Cursor worktrees, those worktrees are separate copies of the repo. Files created in one worktree do **not** automatically appear in the others.

---

## Signature

Comparison signature: `gpt_5_4`
