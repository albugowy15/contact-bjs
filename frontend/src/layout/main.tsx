"use client";

import { Button } from "@/components/ui/button";
import { useSession } from "@/lib/auth";
import Link from "next/link";
import * as React from "react";

export const MainLayout = ({ children }: { children: React.ReactNode }) => {
  const session = useSession();
  return (
    <div className="flex flex-col min-h-screen">
      <header className="sticky top-0 z-10 bg-background border-b">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold text-primary">
            MyApp
          </Link>
          <nav>
            <ul className="flex space-x-4">
              <li>
                <Button variant="ghost" asChild>
                  <Link href="/home">Home</Link>
                </Button>
              </li>
              {session.isAuthenticated ? (
                <li>
                  <Button onClick={session.signOut}>Logout</Button>
                </li>
              ) : (
                <>
                  <li>
                    <Button variant="ghost" asChild>
                      <Link href="/login">Login</Link>
                    </Button>
                  </li>
                  <li>
                    <Button variant="ghost" asChild>
                      <Link href="/register">Register</Link>
                    </Button>
                  </li>
                </>
              )}
            </ul>
          </nav>
        </div>
      </header>

      <main className="flex-grow container mx-auto px-4 py-8">{children}</main>

      <footer className="bg-background border-t">
        <div className="container mx-auto px-4 py-6 text-center text-muted-foreground">
          <p>&copy; 2024 Contact. Created by Mohamad Kholid Bughowi.</p>
        </div>
      </footer>
    </div>
  );
};
