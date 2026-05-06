// AKOS template — verdict-flip webhook route for {{REPO_SLUG}}.
// Rendered by `bless --with slack` into <repo>/app/api/monitoring/verdict-flip/route.ts.
// Secret-gated via MONITORING_WEBHOOK_SECRET. Pairs with lib/monitoring/slack.ts.

import { NextResponse, type NextRequest } from "next/server"
import { z } from "zod"
import { notifyOps, block } from "@/lib/monitoring/slack"

const PayloadSchema = z.object({
  previous: z.string(),
  next: z.string(),
  cycle_id: z.string().optional(),
  reason: z.string().optional(),
})

export async function POST(request: NextRequest) {
  const secret = request.headers.get("x-mc-secret")
  if (!secret || secret !== process.env.MONITORING_WEBHOOK_SECRET) {
    return NextResponse.json({ error: "unauthorized" }, { status: 401 })
  }
  const body = await request.json().catch(() => null)
  const parsed = PayloadSchema.safeParse(body)
  if (!parsed.success) {
    return NextResponse.json({ error: "invalid_payload" }, { status: 400 })
  }
  const { previous, next, cycle_id, reason } = parsed.data
  await notifyOps({
    text: `{{REPO_SLUG}} verdict flipped ${previous} → ${next}`,
    blocks: [
      block(`*{{REPO_SLUG}} verdict flipped*\n${previous} → *${next}*`),
      block(`Cycle: \`${cycle_id ?? "—"}\`\nReason: ${reason ?? "—"}`),
    ],
  })
  return NextResponse.json({ ok: true })
}
