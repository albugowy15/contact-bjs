"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { MainLayout } from "@/layout/main";
import { protectedFetch } from "@/lib/api";
import { useSession } from "@/lib/auth";
import { useQuery } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import * as React from "react";
import { AddContactDialog } from "./_components/add-contact-dialog";
import { EditContactDialog } from "./_components/edit-contact-dialog";
import { DeleteContactDialog } from "./_components/delete-contact-dialog";

export default function MainHomePage() {
  const router = useRouter();
  const session = useSession();
  if (!session.isAuthenticated) {
    router.replace("/login");
  }

  const contactQuery = useQuery({
    queryFn: async () => {
      return await protectedFetch<
        { fullname: string; id: number; phone_number: string }[]
      >("/contacts");
    },
    queryKey: ["list-contacts"],
    enabled: !!session.isAuthenticated,
  });

  const contacts = contactQuery.data?.data || [];

  return (
    <MainLayout>
      <div className="flex justify-end mb-4">
        <AddContactDialog onSuccess={() => contactQuery.refetch()} />
      </div>
      <Card>
        <CardHeader>
          <CardTitle>Contacts List</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Phone</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {contacts.map((contact) => (
                <TableRow key={contact.id}>
                  <TableCell>{contact.fullname}</TableCell>
                  <TableCell>{contact.phone_number}</TableCell>
                  <TableCell>
                    <EditContactDialog
                      defaultValues={{
                        fullname: contact.fullname,
                        phone_number: contact.phone_number,
                      }}
                      contactId={contact.id}
                      onSuccess={() => contactQuery.refetch()}
                    />
                    <DeleteContactDialog
                      contactId={contact.id}
                      onSuccess={() => contactQuery.refetch()}
                    />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </MainLayout>
  );
}
