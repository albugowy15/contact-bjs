"use client";

const BACKEND_API_URL = process.env.NEXT_PUBLIC_BACKEND_API_URL || "";
const BACKEND_API_VERSION =
  process.env.NEXT_PUBLIC_BACKEND_API_URL_VERSION || "v1";

interface FetchOption {
  method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  body?: unknown;
  headers?: Record<string, string>;
}

type BackendApiResponse<TData> = {
  data?: TData;
  message?: string;
};

interface AuthState {
  accessToken: string;
  foo: string;
}

interface StoredData {
  state: AuthState;
  version: number;
}

async function protectedFetch<TData>(path: string, options?: FetchOption) {
  console.log("got baseurl:", BACKEND_API_URL);
  const storedData = localStorage.getItem("auth");
  if (!storedData) {
    throw new Error("Auth not stored, please login");
  }
  const parsedData: StoredData = JSON.parse(storedData);
  const token = parsedData.state.accessToken;
  const fullUrl = `${BACKEND_API_URL}/${BACKEND_API_VERSION}/${path}`;
  const response = await fetch(fullUrl, {
    method: options?.method || "GET",
    body: options?.body ? JSON.stringify(options?.body) : undefined,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
      ...options?.headers,
    },
  });
  const responseBody: BackendApiResponse<TData> = await response.json();
  if (!response.ok) {
    if (responseBody.message) {
      throw new Error(responseBody.message);
    }
    throw new Error("fetch failed unknown error");
  }
  return responseBody;
}

async function publicFetch<TData>(path: string, options?: FetchOption) {
  console.log("got baseurl:", BACKEND_API_URL);
  const fullUrl = `${BACKEND_API_URL}/${BACKEND_API_VERSION}/${path}`;
  const response = await fetch(fullUrl, {
    method: options?.method || "GET",
    body: options?.body ? JSON.stringify(options?.body) : undefined,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });
  const responseBody: BackendApiResponse<TData> = await response.json();
  if (!response.ok) {
    if (responseBody.message) {
      throw new Error(responseBody.message);
    }
    throw new Error("fetch failed unknown error");
  }
  return responseBody;
}

export {
  protectedFetch,
  publicFetch,
  type FetchOption,
  type BackendApiResponse,
};
