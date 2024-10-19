from marshmallow import Schema, fields
from marshmallow.validate import Length, Regexp
from marshmallow.exceptions import ValidationError
import re


def validate_password(password):
    if len(password) < 6 or len(password) > 32:
        raise ValidationError("Password must be at least 6 to 32 characters long.")
    if not re.search(r"[a-z]", password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if re.search(r"\s", password):
        raise ValidationError("Password must not contain spaces.")
    return True


class RegisterRequestSchema(Schema):
    fullname = fields.String(required=True, validate=Length(min=10, max=200))
    email = fields.Email(required=True, validate=Length(min=10, max=200))
    password = fields.String(required=True, validate=validate_password)


class LoginRequestSchema(Schema):
    email = fields.Email(required=True, validate=Length(min=10, max=200))
    password = fields.String(required=True, validate=validate_password)


class CreateContactRequestSchema(Schema):
    fullname = fields.String(required=True, validate=Length(min=10, max=200))
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
    fullname = fields.String(required=True, validate=Length(min=10, max=200))
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
