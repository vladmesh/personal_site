import { PUBLIC_API_BASE_URL } from "astro:env/server";

const DEFAULT_TIMEOUT_MS = 8000;

export class ApiError extends Error {
  status: number;
  payload: unknown;

  constructor(message: string, status: number, payload: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.payload = payload;
  }
}

const apiBaseUrl = PUBLIC_API_BASE_URL.replace(/\/+$/, "");

type FetchOptions = RequestInit & { timeoutMs?: number };

export async function fetchApi<T>(path: string, options: FetchOptions = {}): Promise<T> {
  const { timeoutMs = DEFAULT_TIMEOUT_MS, headers, ...rest } = options;
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);

  const url = buildUrl(path);
  const response = await fetch(url, {
    ...rest,
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      ...headers,
    },
    signal: controller.signal,
  }).catch((error) => {
    clearTimeout(timeout);
    throw error;
  });

  clearTimeout(timeout);

  if (!response.ok) {
    const payload = await safeParseJson(response);
    throw new ApiError(`API request failed with status ${response.status}`, response.status, payload);
  }

  return (await safeParseJson(response)) as T;
}

function buildUrl(path: string): string {
  const base = apiBaseUrl;
  if (!base) {
    throw new Error("PUBLIC_API_BASE_URL is not set");
  }
  if (path.startsWith("http://") || path.startsWith("https://")) {
    return path;
  }
  if (!path.startsWith("/")) {
    return `${base}/${path}`;
  }
  return `${base}${path}`;
}

async function safeParseJson(response: Response): Promise<unknown> {
  try {
    return await response.json();
  } catch {
    try {
      return await response.text();
    } catch {
      return null;
    }
  }
}
