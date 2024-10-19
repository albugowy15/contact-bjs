"use client";

import * as React from "react";
import LoginForm from "./_components/login-form";
import { MainLayout } from "@/layout/main";
import { useSession } from "@/lib/auth";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();
  const session = useSession();
  if (session.isAuthenticated) {
    router.replace("/home");
  }
  return (
    <MainLayout>
      <div className="min-h-screen flex items-center justify-center">
        <LoginForm />
      </div>
    </MainLayout>
  );
}
