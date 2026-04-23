# Envoy Tech Lab — GitHub repository hub

**Entity:** HLK Tech Lab / Envoy Tech  
**Governance:** [PRECEDENCE.md](../../../compliance/PRECEDENCE.md), [v3.0/index.md](../../index.md)

---

## Purpose

Holistika tracks **many GitHub repositories** (platform products, internal tools, client-delivery codebases). This folder is the **canonical index** in the vault: it records *which* repos matter, *how* they are classified, and *who* owns the relationship—not the full file tree.

**GitHub remains SSOT** for source code and in-repo documentation. This vault holds:

- The **[REPOSITORIES_REGISTRY.md](REPOSITORIES_REGISTRY.md)** table (canonical).
- Optional **subfolders** (`platform/`, `internal/`, `client-delivery/`) for short README stubs or links—*not* a requirement to duplicate repo contents here.

---

## Folder taxonomy

| Subfolder | Use |
|-----------|-----|
| `platform/` | Product platforms (e.g. KiRBe, MADEIRA-related application repos). Aligns with existing vault doc roots [../KiRBe/](../KiRBe/) and [../MADEIRA/](../MADEIRA/). |
| `internal/` | Internal-only tools and libraries (not client-specific). |
| `client-delivery/` | Repositories created or primarily used for external client / engagement delivery. |

Existing top-level **KiRBe/**, **MADEIRA/**, and **Showcases/** under Envoy Tech Lab remain the **markdown documentation** homes unless a later migration moves them.

---

## Submodule vs pointer-only

| Approach | When to use |
|----------|----------------|
| **Pointer-only (default)** | Registry row + `github_url` + optional topic index `source` entries. Scales to many repos with minimal git noise. |
| **Git submodule** | Only when this monorepo must pin a specific commit for CI, review, or reproducible builds. Document the rationale in the registry `notes` column. |

Do not add submodules bulk-style without CTO / Tech Lead approval.

---

## Naming

- **repo_slug:** lowercase kebab-case, stable (rename only with a registry note and topic index update).
- **primary_owner_role:** must match `role_name` in [baseline_organisation.csv](../../../compliance/baseline_organisation.csv).

---

## API metadata columns

Registry rows may include **`api_spec_pointer`** and **`api_topic_id`** (see [REPOSITORIES_REGISTRY.md](REPOSITORIES_REGISTRY.md)). **Per-component** API fields (exposure, dependencies, runbooks) live in **[COMPONENT_SERVICE_MATRIX.csv](../../../compliance/COMPONENT_SERVICE_MATRIX.csv)** joined on **`repo_slug`**. API lifecycle procedures: [SOP-HLK_API_LIFECYCLE_MANAGEMENT_001.md](../../Admin/O5-1/Tech/System%20Owner/SOP-HLK_API_LIFECYCLE_MANAGEMENT_001.md).

## Related

- **Think Big** — commercial / engagement artifacts that are *not* repository roots: [../../Think Big/README.md](../../Think%20Big/README.md)
- **Topic bundles** — link registry rows from topic indexes; see [TOPIC_KNOWLEDGE_INDEX_TEMPLATE.md](../../Admin/O5-1/People/Compliance/TOPIC_KNOWLEDGE_INDEX_TEMPLATE.md)
- **Component matrix (CTO SSOT)** — [COMPONENT_SERVICE_MATRIX.csv](../../../compliance/COMPONENT_SERVICE_MATRIX.csv)
