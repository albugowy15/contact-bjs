"use client";

import { protectedFetch } from "@/lib/api";
import { useMutation } from "@tanstack/react-query";
import * as React from "react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { ContactForm, ContactFormSchema } from "./contact-form";

interface AddContactDialogProps {
  onSuccess: () => void;
}

const AddContactDialog = (props: AddContactDialogProps) => {
  const addContactMutation = useMutation({
    mutationFn: async (values: { fullname: string; phone_number: string }) => {
      return await protectedFetch("/contacts", {
        method: "POST",
        body: values,
      });
    },
    onSuccess() {
      toast.success("Contact added");
      props.onSuccess();
    },
    onError(error) {
      toast.error(error.message);
    },
  });

  function onSubmit(values: ContactFormSchema) {
    addContactMutation.mutate(values);
  }

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button>Add Contact</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Add contact</DialogTitle>
        </DialogHeader>
        <ContactForm
          variant="add"
          onSubmit={onSubmit}
          submitDiabled={addContactMutation.isPending}
        />
      </DialogContent>
    </Dialog>
  );
};

export { AddContactDialog };
