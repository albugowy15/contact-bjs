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
import { Pencil } from "lucide-react";

interface EditContactDialogProps {
  contactId: number;
  defaultValues: ContactFormSchema;
  onSuccess: () => void;
}

const EditContactDialog = (props: EditContactDialogProps) => {
  const editContactMutation = useMutation({
    mutationFn: async (values: {
      id: number;
      fullname: string;
      phone_number: string;
    }) => {
      return await protectedFetch(`/contacts/${values.id}`, {
        method: "PUT",
        body: {
          fullname: values.fullname,
          phone_number: values.phone_number,
        },
      });
    },
    onSuccess() {
      toast.success("Contact updated");
      props.onSuccess();
    },
    onError(error) {
      toast.error(error.message);
    },
  });

  function onSubmit(values: ContactFormSchema) {
    editContactMutation.mutate({
      id: props.contactId,
      fullname: values.fullname,
      phone_number: values.phone_number,
    });
  }

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="ghost" size="icon">
          <Pencil className="h-4 w-4" />
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Edit contact</DialogTitle>
        </DialogHeader>
        <ContactForm
          variant="edit"
          onSubmit={onSubmit}
          defaultValues={props.defaultValues}
          submitDiabled={editContactMutation.isPending}
        />
      </DialogContent>
    </Dialog>
  );
};

export { EditContactDialog };
