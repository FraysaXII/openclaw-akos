// AKOS template — Sentry edge config for {{REPO_SLUG}}.
// Rendered by `bless --with sentry` into <repo>/sentry.edge.config.ts.

import * as Sentry from "@sentry/nextjs"

const dsn = process.env.SENTRY_DSN ?? process.env.NEXT_PUBLIC_SENTRY_DSN

if (dsn) {
  Sentry.init({
    dsn,
    environment: process.env.VERCEL_ENV ?? process.env.NODE_ENV,
    tracesSampleRate: 0.05,
  })
}
