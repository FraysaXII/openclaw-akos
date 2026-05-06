// AKOS template — Sentry server (Node) config for {{REPO_SLUG}}.
// Rendered by `bless --with sentry` into <repo>/sentry.server.config.ts.

import * as Sentry from "@sentry/nextjs"

const dsn = process.env.SENTRY_DSN ?? process.env.NEXT_PUBLIC_SENTRY_DSN

if (dsn) {
  Sentry.init({
    dsn,
    environment: process.env.VERCEL_ENV ?? process.env.NODE_ENV,
    tracesSampleRate: 0.1,
    integrations: [],
    beforeSend(event) {
      if (event.request?.headers) {
        delete event.request.headers["authorization"]
        delete event.request.headers["cookie"]
        delete event.request.headers["x-supabase-auth"]
      }
      if (event.user) {
        event.user = { id: event.user.id ?? "anonymous" }
      }
      return event
    },
  })
}
