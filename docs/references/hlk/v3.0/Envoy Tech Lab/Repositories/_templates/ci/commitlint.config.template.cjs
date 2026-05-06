/**
 * AKOS template — commitlint (Conventional Commits) for {{REPO_SLUG}}.
 * Rendered by bless when stack=node.
 */
module.exports = {
  extends: ["@commitlint/config-conventional"],
  rules: {
    "type-enum": [
      2,
      "always",
      [
        "feat",
        "fix",
        "docs",
        "refactor",
        "test",
        "chore",
        "style",
        "perf",
        "build",
        "ci",
        "revert",
      ],
    ],
    "subject-case": [2, "never", ["upper-case", "pascal-case", "start-case"]],
    "header-max-length": [2, "always", 100],
    "body-max-line-length": [1, "always", 200],
  },
};
