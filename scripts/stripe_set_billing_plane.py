#!/usr/bin/env python3
"""Set Stripe Customer or Subscription metadata `hlk_billing_plane` (test/live key in env).

Requires `STRIPE_SECRET_KEY` in the environment (same key stored in Supabase secrets for Edge).

Examples:

  py scripts/stripe_set_billing_plane.py --customer cus_XXX --plane holistika_ops --org-label "Staging"
  py scripts/stripe_set_billing_plane.py --subscription sub_XXX --plane kirbe
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

PLANES = ("holistika_ops", "holistika", "kirbe")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--customer", type=str, help="Stripe Customer id (cus_)")
    g.add_argument("--subscription", type=str, help="Stripe Subscription id (sub_)")
    parser.add_argument(
        "--plane",
        required=True,
        choices=PLANES,
        help="hlk_billing_plane value",
    )
    parser.add_argument(
        "--org-label",
        dest="org_label",
        default="",
        help="Optional Customer metadata org_label (customers only)",
    )
    args = parser.parse_args()

    key = os.environ.get("STRIPE_SECRET_KEY")
    if not key:
        print("error: set STRIPE_SECRET_KEY (do not commit keys)", file=sys.stderr)
        return 1

    fields: dict[str, str] = {"metadata[hlk_billing_plane]": args.plane}
    if args.customer and args.org_label:
        fields["metadata[org_label]"] = args.org_label

    body = urllib.parse.urlencode(fields).encode("utf-8")
    if args.customer:
        url = f"https://api.stripe.com/v1/customers/{args.customer}"
    else:
        url = f"https://api.stripe.com/v1/subscriptions/{args.subscription}"

    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        print("Stripe API error:", e.code, err, file=sys.stderr)
        return 1

    oid = data.get("id", "?")
    meta = data.get("metadata") or {}
    print("ok:", oid, "metadata:", meta)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
