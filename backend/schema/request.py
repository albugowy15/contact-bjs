from marshmallow import Schema, fields
from marshmallow.validate import Length, Regexp
from marshmallow.exceptions import ValidationError
import re


def validate_to_err_message(errors):
    _, first_error_list = next(iter(errors.items()))
    first_error = first_error_list[0]
    return first_error


def validate_password(password):
    if len(password) < 6 or len(password) > 32:
        raise ValidationError("Password must be at least 6 to 32 characters long.")
    if not re.search(r"[a-z]", password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if re.search(r"\s", password):
        raise ValidationError("Password must not contain spaces.")
    return True


def validate_fullname(fullname):
    if not re.match(r"^[A-Za-z\s]+$", fullname):
        raise ValidationError("Fullname must contain only letters and spaces.")


class RegisterRequestSchema(Schema):
    fullname = fields.String(
        required=True,
        error_messages={"required": "Fullname is required."},
        validate=[
            Length(
                min=10,
                max=200,
                error="Fullname length must be between 10 and 200 characters.",
            ),
            validate_fullname,
        ],
    )
    email = fields.Email(
        required=True,
        validate=Length(
            min=10, max=200, error="Email length must be between 10 and 200 characters."
        ),
    )
    password = fields.String(
        required=True,
        error_messages={"required": "Password is required."},
        validate=validate_password,
    )


class LoginRequestSchema(Schema):
    email = fields.Email(
        required=True,
        error_messages={"required": "Email is required."},
        validate=Length(
            min=10, max=200, error="Email length must be between 10 and 200 characters."
        ),
    )
    password = fields.String(
        required=True,
        error_messages={"required": "Password is required."},
        validate=validate_password,
    )


class CreateContactRequestSchema(Schema):
    fullname = fields.String(
        required=True,
        error_messages={"required": "Fullname is required."},
        validate=[
            Length(
                min=10,
                max=200,
                error="Fullname length must be between 10 and 200 characters.",
            ),
            validate_fullname,
        ],
    )
    phone_number = fields.String(
        required=True,
        validate=[
            Regexp(
                r"^0\d+$",
                error="Phone number must start with zero, contain only numbers, and have no spaces.",
            ),
            Length(
                min=10,
                max=20,
                error="Phone number length must be between 10 and 20 digits.",
            ),
        ],
    )


class UpdateContactRequestSchema(Schema):
    fullname = fields.String(
        required=True,
        error_messages={"required": "Fullname is required."},
        validate=[
            Length(
                min=10,
                max=200,
                error="Fullname length must be between 10 and 200 characters.",
            ),
            validate_fullname,
        ],
    )
    phone_number = fields.String(
        required=True,
        validate=[
            Regexp(
                r"^0\d+$",
                error="Phone number must start with zero, contain only numbers, and have no spaces.",
            ),
            Length(
                min=10,
                max=20,
                error="Phone number length must be between 10 and 20 digits.",
            ),
        ],
    )
