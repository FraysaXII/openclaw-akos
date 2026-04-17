import type { OpenClawPluginApi } from "openclaw/plugin-sdk";

type PluginConfig = {
  apiUrl?: string;
  apiKeyEnv?: string;
  timeoutMs?: number;
};

type ToolParams = Record<string, unknown>;
type ToolResult = {
  content: Array<{ type: "text"; text: string }>;
};

type ToolSpec = {
  name: string;
  description: string;
  parameters: Record<string, unknown>;
  request: (params: ToolParams) => { path: string; query?: Record<string, string> };
};

const DEFAULT_API_URL = "http://127.0.0.1:8420";
const DEFAULT_TIMEOUT_MS = 10_000;

function readRequiredString(params: ToolParams, key: string): string {
  const value = params[key];
  if (typeof value !== "string" || !value.trim()) {
    throw new Error(`Parameter "${key}" is required.`);
  }
  return value.trim();
}

function readOptionalInt(params: ToolParams, key: string, fallback: number): number {
  const value = params[key];
  if (typeof value === "number" && Number.isFinite(value)) {
    return Math.trunc(value);
  }
  if (typeof value === "string" && value.trim()) {
    const parsed = Number.parseInt(value.trim(), 10);
    if (Number.isFinite(parsed)) {
      return parsed;
    }
  }
  return fallback;
}

function normalizeConfig(pluginConfig: PluginConfig | undefined) {
  const apiUrl = (pluginConfig?.apiUrl ?? DEFAULT_API_URL).trim().replace(/\/+$/, "");
  const apiKeyEnv = (pluginConfig?.apiKeyEnv ?? "AKOS_API_KEY").trim();
  const timeoutMs = pluginConfig?.timeoutMs ?? DEFAULT_TIMEOUT_MS;
  return { apiUrl, apiKeyEnv, timeoutMs };
}

function buildUrl(
  config: ReturnType<typeof normalizeConfig>,
  path: string,
  query?: Record<string, string>,
): string {
  const url = new URL(path, `${config.apiUrl}/`);
  for (const [key, value] of Object.entries(query ?? {})) {
    url.searchParams.set(key, value);
  }
  return url.toString();
}

function buildHeaders(config: ReturnType<typeof normalizeConfig>): Record<string, string> {
  const headers: Record<string, string> = { accept: "application/json" };
  const apiKey = config.apiKeyEnv ? process.env[config.apiKeyEnv]?.trim() : "";
  if (apiKey) {
    headers.authorization = ["Bearer", apiKey].join(" ");
  }
  return headers;
}

function toToolResult(payload: unknown): ToolResult {
  return {
    content: [
      {
        type: "text",
        text: typeof payload === "string" ? payload : JSON.stringify(payload, null, 2),
      },
    ],
  };
}

function extractErrorDetail(payload: unknown): string {
  if (payload && typeof payload === "object" && "detail" in payload) {
    const detail = payload.detail;
    if (typeof detail === "string" && detail.trim()) {
      return detail.trim();
    }
  }
  if (typeof payload === "string" && payload.trim()) {
    return payload.trim();
  }
  return "Unknown AKOS API error.";
}

async function requestAkosJson(
  pluginConfig: PluginConfig | undefined,
  request: ReturnType<ToolSpec["request"]>,
): Promise<unknown> {
  const config = normalizeConfig(pluginConfig);
  const url = buildUrl(config, request.path, request.query);
  const response = await fetch(url, {
    headers: buildHeaders(config),
    signal: AbortSignal.timeout(config.timeoutMs),
  });

  const raw = await response.text();
  let payload: unknown = raw;
  if (raw) {
    try {
      payload = JSON.parse(raw);
    } catch {
      payload = raw;
    }
  }

  if (!response.ok) {
    return {
      status: "error",
      source: "akos-api",
      http_status: response.status,
      error_detail: extractErrorDetail(payload),
    };
  }
  return payload;
}

function registerApiTool(api: OpenClawPluginApi, pluginConfig: PluginConfig | undefined, spec: ToolSpec): void {
  api.registerTool(
    {
      name: spec.name,
      description: spec.description,
      parameters: spec.parameters,
      async execute(_id: string, params: ToolParams): Promise<ToolResult> {
        try {
          const payload = await requestAkosJson(pluginConfig, spec.request(params));
          return toToolResult(payload);
        } catch (error) {
          const message = error instanceof Error ? error.message : String(error);
          return toToolResult({
            status: "error",
            source: "akos-runtime-tools",
            error_detail: message,
          });
        }
      },
    },
    { optional: true },
  );
}

const emptyParameters = {
  type: "object",
  additionalProperties: false,
  properties: {},
};

const toolSpecs: ToolSpec[] = [
  {
    name: "akos_route_request",
    description:
      "Classify a raw user message into an AKOS route (HLK lookup/search, finance research, GTM project, generic other, admin_escalate, execution_escalate). " +
      "Use when the operator goal is ambiguous or mixed. Do not use for simple direct HLK lookups when the ladder is already obvious. " +
      "Escalation routes win over embeddings when regex safety matches. Returns must_escalate and an operator_message suitable for Madeira.",
    parameters: {
      type: "object",
      additionalProperties: false,
      properties: {
        query: { type: "string", description: "The raw user request to classify." },
      },
      required: ["query"],
    },
    request: (params) => ({
      path: "/routing/classify",
      query: { q: readRequiredString(params, "query") },
    }),
  },
  {
    name: "hlk_role",
    description: "Resolve one HLK role from the canonical organisation registry using a canonical name or normalized title label.",
    parameters: {
      type: "object",
      additionalProperties: false,
      properties: {
        role_name: { type: "string", description: "Canonical role name or normalized title label, for example CTO or Chief Technology Officer." },
      },
      required: ["role_name"],
    },
    request: (params) => ({
      path: `/hlk/roles/${encodeURIComponent(readRequiredString(params, "role_name"))}`,
    }),
  },
  {
    name: "hlk_role_chain",
    description: "Traverse the reports-to chain for one HLK role using a canonical name or normalized title label.",
    parameters: {
      type: "object",
      additionalProperties: false,
      properties: {
        role_name: { type: "string", description: "Canonical role name or normalized title label." },
      },
      required: ["role_name"],
    },
    request: (params) => ({
      path: `/hlk/roles/${encodeURIComponent(readRequiredString(params, "role_name"))}/chain`,
    }),
  },
  {
    name: "hlk_area",
    description: "List roles that belong to one HLK area.",
    parameters: {
      type: "object",
      additionalProperties: false,
      properties: {
        area: { type: "string", description: "Area name from the HLK baseline." },
      },
      required: ["area"],
    },
    request: (params) => ({
      path: `/hlk/areas/${encodeURIComponent(readRequiredString(params, "area"))}`,
    }),
  },
  {
    name: "hlk_process",
    description: "Look up one HLK process item by canonical item ID with normalized matching for casing and punctuation.",
    parameters: {
      type: "object",
      additionalProperties: false,
      properties: {
        item_id: { type: "string", description: "Canonical HLK process item ID." },
      },
      required: ["item_id"],
    },
    request: (params) => ({
      path: `/hlk/processes/${encodeURIComponent(readRequiredString(params, "item_id"))}`,
    }),
  },
  {
    name: "hlk_process_tree",
    description: "Return direct children for one HLK process item name.",
    parameters: {
      type: "object",
      additionalProperties: false,
      properties: {
        item_name: { type: "string", description: "Canonical HLK process item name." },
      },
      required: ["item_name"],
    },
    request: (params) => ({
      path: `/hlk/processes/${encodeURIComponent(readRequiredString(params, "item_name"))}/tree`,
    }),
  },
  {
    name: "hlk_projects",
    description: "Return the HLK process/project summary.",
    parameters: emptyParameters,
    request: () => ({ path: "/hlk/processes" }),
  },
  {
    name: "hlk_gaps",
    description: "Identify HLK items with missing metadata or TBD ownership.",
    parameters: emptyParameters,
    request: () => ({ path: "/hlk/gaps" }),
  },
  {
    name: "hlk_search",
    description: "Ranked search across the HLK registry with best-match fields for clear canonical winners.",
    parameters: {
      type: "object",
      additionalProperties: false,
      properties: {
        query: { type: "string", description: "Search query." },
      },
      required: ["query"],
    },
    request: (params) => ({
      path: "/hlk/search",
      query: { q: readRequiredString(params, "query") },
    }),
  },
  {
    name: "hlk_graph_summary",
    description:
      "Return HLK CSV registry counts plus optional Neo4j label and relationship aggregates when the mirrored graph is configured.",
    parameters: emptyParameters,
    request: () => ({ path: "/hlk/graph/summary" }),
  },
  {
    name: "hlk_graph_process_neighbourhood",
    description:
      "Return a bounded neighbourhood subgraph around one HLK process item_id from the optional Neo4j mirror (depth and limit capped server-side).",
    parameters: {
      type: "object",
      additionalProperties: false,
      properties: {
        item_id: { type: "string", description: "Canonical HLK process item_id." },
        depth: { type: "integer", description: "Traversal depth (1-5), default 2." },
        limit: { type: "integer", description: "Max nodes to return, default 80." },
      },
      required: ["item_id"],
    },
    request: (params) => ({
      path: `/hlk/graph/process/${encodeURIComponent(readRequiredString(params, "item_id"))}/neighbourhood`,
      query: {
        depth: String(readOptionalInt(params, "depth", 2)),
        limit: String(readOptionalInt(params, "limit", 80)),
      },
    }),
  },
  {
    name: "hlk_graph_role_neighbourhood",
    description:
      "Return processes and reporting roles linked to one HLK role_name from the optional Neo4j mirror (bounded).",
    parameters: {
      type: "object",
      additionalProperties: false,
      properties: {
        role_name: { type: "string", description: "Canonical HLK role name." },
        depth: { type: "integer", description: "Traversal depth (1-4), default 2." },
        limit: { type: "integer", description: "Max nodes to return, default 80." },
      },
      required: ["role_name"],
    },
    request: (params) => ({
      path: `/hlk/graph/role/${encodeURIComponent(readRequiredString(params, "role_name"))}/neighbourhood`,
      query: {
        depth: String(readOptionalInt(params, "depth", 2)),
        limit: String(readOptionalInt(params, "limit", 80)),
      },
    }),
  },
  {
    name: "finance_quote",
    description: "Return a read-only finance quote bundle for one ticker symbol.",
    parameters: {
      type: "object",
      additionalProperties: false,
      properties: {
        ticker: { type: "string", description: "Ticker symbol, for example AAPL." },
      },
      required: ["ticker"],
    },
    request: (params) => ({
      path: `/finance/quote/${encodeURIComponent(readRequiredString(params, "ticker"))}`,
    }),
  },
  {
    name: "finance_search",
    description: "Resolve a company or partial ticker to matching finance symbols.",
    parameters: {
      type: "object",
      additionalProperties: false,
      properties: {
        query: { type: "string", description: "Company name or partial ticker." },
      },
      required: ["query"],
    },
    request: (params) => ({
      path: "/finance/search",
      query: { q: readRequiredString(params, "query") },
    }),
  },
  {
    name: "finance_sentiment",
    description: "Fetch read-only news sentiment for one or more ticker symbols.",
    parameters: {
      type: "object",
      additionalProperties: false,
      properties: {
        tickers: { type: "string", description: "Comma-separated ticker list." },
      },
      required: ["tickers"],
    },
    request: (params) => ({
      path: "/finance/sentiment",
      query: { tickers: readRequiredString(params, "tickers") },
    }),
  },
];

const akosRuntimeToolsPlugin = {
  id: "akos-runtime-tools",
  name: "AKOS Runtime Tools",
  description: "Expose AKOS HLK and finance lookups as OpenClaw agent tools.",
  register(api: OpenClawPluginApi) {
    const pluginConfig = (api.pluginConfig ?? {}) as PluginConfig;
    for (const spec of toolSpecs) {
      registerApiTool(api, pluginConfig, spec);
    }
  },
};

export default akosRuntimeToolsPlugin;
