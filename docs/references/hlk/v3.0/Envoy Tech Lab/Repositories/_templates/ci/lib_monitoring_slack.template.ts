/**
 * AKOS template — Slack monitoring webhook for {{REPO_SLUG}}.
 * Rendered by `bless --with slack` into <repo>/lib/monitoring/slack.ts.
 *
 * No-ops when SLACK_OPS_WEBHOOK is unset so local dev stays quiet.
 * Verbatim of hlk-erp I62 production code.
 */

interface SlackBlock {
  type: string
  text?: { type: string; text: string }
  fields?: { type: string; text: string }[]
}

interface SlackPayload {
  text: string
  blocks?: SlackBlock[]
}

export async function notifyOps(payload: SlackPayload): Promise<void> {
  const url = process.env.SLACK_OPS_WEBHOOK
  if (!url) return
  try {
    await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(5_000),
    })
  } catch (err) {
    console.warn("[slack] notify failed", err instanceof Error ? err.message : err)
  }
}

export function block(text: string): SlackBlock {
  return { type: "section", text: { type: "mrkdwn", text } }
}
