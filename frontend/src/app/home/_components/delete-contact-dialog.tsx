"use client";

import * as React from "react";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { Button } from "@/components/ui/button";
import { useMutation } from "@tanstack/react-query";
import { protectedFetch } from "@/lib/api";
import { toast } from "sonner";
import { Trash2 } from "lucide-react";

interface DeleteContactDialogProps {
  onSuccess: () => void;
  contactId: number;
}

const DeleteContactDialog = (props: DeleteContactDialogProps) => {
  const deleteContactMutation = useMutation({
    mutationFn: async (contactId: number) => {
      return await protectedFetch(`/contacts/${contactId}`, {
        method: "DELETE",
      });
    },
    onSuccess() {
      toast.success("Contact deleted!");
      props.onSuccess();
    },
    onError(error) {
      toast.error(error.message);
    },
  });
  return (
    <AlertDialog>
      <AlertDialogTrigger asChild>
        <Button variant="ghost" size="icon">
          <Trash2 className="h-4 w-4" />
        </Button>
      </AlertDialogTrigger>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
          <AlertDialogDescription>
            This action cannot be undone. This will permanently delete this
            contact.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>Cancel</AlertDialogCancel>
          <AlertDialogAction asChild>
            <Button
              variant="destructive"
              onClick={() => deleteContactMutation.mutate(props.contactId)}
            >
              Continue
            </Button>
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
};

export { DeleteContactDialog };
