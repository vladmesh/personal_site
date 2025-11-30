const DEFAULT_TIMEOUT_MS = 8000;
const DEFAULT_BASE_URL = "http://localhost:8000";

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

const apiBaseUrl =
  (import.meta.env.PUBLIC_API_BASE_URL as string | undefined)?.replace(/\/+$/, "") ||
  DEFAULT_BASE_URL;

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
  if (path.startsWith("http://") || path.startsWith("https://")) {
    return path;
  }
  if (!path.startsWith("/")) {
    return `${apiBaseUrl}/${path}`;
  }
  return `${apiBaseUrl}${path}`;
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
