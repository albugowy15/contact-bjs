"use client";

import * as React from "react";
import { useRouter } from "next/navigation";
import RegistrationForm from "./_components/registration-form";
import { useSession } from "@/lib/auth";
import { MainLayout } from "@/layout/main";

export default function RegistrationPage() {
  const router = useRouter();
  const session = useSession();
  if (session.isAuthenticated) {
    router.replace("/home");
  }
  return (
    <MainLayout>
      <div className="flex justify-center items-center min-h-screen">
        <RegistrationForm />
      </div>
    </MainLayout>
  );
}
