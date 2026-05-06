// AKOS template — Sentry browser/client config for {{REPO_SLUG}}.
// Rendered by `bless --with sentry` into <repo>/sentry.client.config.ts.
// Lifted from hlk-erp I62 production configuration; PII scrubber drops sensitive headers
// and reduces the user object to id only.

import * as Sentry from "@sentry/nextjs"

const dsn = process.env.NEXT_PUBLIC_SENTRY_DSN

if (dsn) {
  Sentry.init({
    dsn,
    environment: process.env.NEXT_PUBLIC_VERCEL_ENV ?? process.env.NODE_ENV,
    tracesSampleRate: 0.1,
    replaysSessionSampleRate: 0,
    replaysOnErrorSampleRate: 1.0,
    integrations: [Sentry.browserTracingIntegration()],
    beforeSend: scrubPii,
    beforeBreadcrumb(breadcrumb) {
      if (breadcrumb.category === "console" && breadcrumb.level === "debug") return null
      return breadcrumb
    },
  })
}

function scrubPii(event: Sentry.ErrorEvent): Sentry.ErrorEvent | null {
  if (event.request?.headers) {
    delete event.request.headers["authorization"]
    delete event.request.headers["cookie"]
    delete event.request.headers["x-supabase-auth"]
  }
  if (event.user) {
    event.user = { id: event.user.id ?? "anonymous" }
  }
  return event
}
