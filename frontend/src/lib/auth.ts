"use client";

import { publicFetch, BackendApiResponse } from "@/lib/api";
import { useMutation } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { create } from "zustand";
import { persist } from "zustand/middleware";

type AuthState = {
  accessToken: string;
  updateAccessToken: (accessToken: AuthState["accessToken"]) => void;
};

const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      accessToken: "",
      updateAccessToken(accessToken) {
        set(() => ({ accessToken: accessToken }));
      },
    }),
    {
      name: "auth",
    },
  ),
);

const useSession = () => {
  const router = useRouter();
  const accessToken = useAuthStore((state) => state.accessToken);
  const updateAccessToken = useAuthStore((state) => state.updateAccessToken);
  const isAuthenticated = accessToken != "";
  const signOut = () => {
    updateAccessToken("");
    router.push("/login");
  };
  return { accessToken, isAuthenticated, signOut };
};

type UseSignInOpts = {
  onError?: ((error: Error) => Promise<unknown> | unknown) | undefined;
  onSuccess?:
    | ((
        data: BackendApiResponse<{
          access_token: string;
        }>,
      ) => Promise<unknown> | unknown)
    | undefined;
};

const useSignIn = (opts?: UseSignInOpts) => {
  const updateAccessToken = useAuthStore((state) => state.updateAccessToken);
  const { data, error, isPending, isError, isSuccess, mutate, mutateAsync } =
    useMutation({
      mutationFn: async (values: { email: string; password: string }) => {
        return await publicFetch<{ access_token: string }>("/login", {
          method: "POST",
          body: values,
        });
      },
      onSuccess(data) {
        updateAccessToken(data.data?.access_token || "");
        if (opts?.onSuccess) {
          opts.onSuccess(data);
        }
      },
      onError(error) {
        if (opts?.onError) {
          opts.onError(error);
        }
      },
    });
  return {
    data,
    error,
    isError,
    isPending,
    isSuccess,
    signIn: mutate,
    signInAsync: mutateAsync,
  };
};

export { useAuthStore, useSession, useSignIn, type AuthState };
