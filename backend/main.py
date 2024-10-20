import json

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from datetime import timedelta
from schema.request import (
    CreateContactRequestSchema,
    LoginRequestSchema,
    RegisterRequestSchema,
    UpdateContactRequestSchema,
    validate_to_err_message,
)
from schema.model import Contact, User
import logging
import traceback

app = Flask(__name__)
app.config.from_prefixed_env()
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
CORS(app)
logging.basicConfig(level=logging.INFO)
db = SQLAlchemy(app)
jwt = JWTManager(app)


@app.errorhandler(HTTPException)
def handle_http_exception(error):
    app.logger.error(error)
    response = {"message": error.description}
    return jsonify(response), error.code


@app.errorhandler(Exception)
def handle_exception(error):
    app.logger.error(error)
    response = {
        "message": "An unexpected error occurred",
    }
    return jsonify(response), 500


@app.errorhandler(404)
def handle_404_error(error):
    app.logger.error(error)
    return jsonify({"message": "Resource not found"}), 404


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"message": "The token has expired."}), 401


@app.post("/v1/register")
def register():
    data = request.get_json()

    schema = RegisterRequestSchema()
    errors = schema.validate(data)
    if errors:
        validate_to_err_message(errors)
        return jsonify({"message": validate_to_err_message(errors)}), 400

    password = data.get("password")
    existing_user = db.session.scalars(
        select(User).filter_by(email=data["email"])
    ).first()
    if existing_user:
        return jsonify(
            {"message": "This email has beed registered. Use another email"}
        ), 400
    hashed_password = generate_password_hash(password)
    new_user = User(
        email=data["email"], fullname=data["email"], hashed_password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(
        {
            "message": "User registered successfully",
        }
    ), 201


@app.post("/v1/login")
def login():
    schema = LoginRequestSchema()
    data = request.get_json()
    errors = schema.validate(data)
    if errors:
        validate_to_err_message(errors)
        return jsonify({"message": validate_to_err_message(errors)}), 400

    email = data["email"]
    password = data["password"]

    user = db.session.scalars(select(User).filter_by(email=email)).first()
    if user and check_password_hash(user.hashed_password, password):
        access_token = create_access_token(
            identity={"id": user.id, "email": user.email}
        )
        return jsonify({"data": {"access_token": access_token}}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401


@app.get("/v1/contacts")
@jwt_required()
def get_all_contacts():
    current_user = get_jwt_identity()
    current_user_id = current_user["id"]
    user = db.session.scalars(select(User).filter_by(id=current_user_id)).first()
    if not user:
        return jsonify({"message": "User not found"}), 404
    contacts = db.session.scalars(
        select(Contact).filter_by(user_id=current_user_id)
    ).all()
    contact_list = []
    for contact in contacts:
        contact_list.append(
            {
                "id": contact.id,
                "fullname": contact.fullname,
                "phone_number": contact.phone_number,
            }
        )

    return jsonify({"data": contact_list}), 200


@app.post("/v1/contacts")
@jwt_required()
def create_contact():
    schema = CreateContactRequestSchema()
    data = request.get_json()
    errors = schema.validate(data)
    if errors:
        validate_to_err_message(errors)
        return jsonify({"message": validate_to_err_message(errors)}), 400

    current_user = get_jwt_identity()
    current_user_id = current_user["id"]
    user = db.session.scalars(select(User).filter_by(id=current_user_id)).first()
    if not user:
        return jsonify({"message": "User not found"}), 404
    new_contact = Contact(
        fullname=data["fullname"],
        phone_number=data["phone_number"],
        user_id=current_user["id"],
    )
    db.session.add(new_contact)
    db.session.commit()
    return jsonify(
        {
            "message": "Contact created successfully",
        }
    ), 201


@app.put("/v1/contacts/<int:contact_id>")
@jwt_required()
def update_contact(contact_id):
    schema = UpdateContactRequestSchema()
    data = request.get_json()
    errors = schema.validate(data)
    if errors:
        validate_to_err_message(errors)
        return jsonify({"message": validate_to_err_message(errors)}), 400

    current_user = get_jwt_identity()
    current_user_id = current_user["id"]

    contact = db.session.scalars(
        select(Contact).filter_by(id=contact_id, user_id=current_user_id)
    ).first()
    if not contact:
        return jsonify({"message": "Contact not found or you are not authorized"}), 404

    contact.fullname = data.get("fullname", contact.fullname)
    contact.phone_number = data.get("phone_number", contact.phone_number)
    db.session.commit()

    return jsonify({"message": "Contact updated"}), 200


@app.get("/v1/contacts/<int:contact_id>")
@jwt_required()
def get_contact(contact_id):
    current_user = get_jwt_identity()
    current_user_id = current_user["id"]
    user = db.session.scalars(select(User).filter_by(id=current_user_id)).first()
    if not user:
        return jsonify({"message": "User not found"}), 404
    contact = db.session.scalars(
        select(Contact).filter_by(id=contact_id, user_id=current_user_id)
    ).first()
    if not contact:
        return jsonify({"message": "Contact not found"}), 404
    return jsonify(
        {
            "data": {
                "id": contact.id,
                "fullname": contact.fullname,
                "phone_number": contact.phone_number,
            }
        }
    ), 200


@app.delete("/v1/contacts/<int:contact_id>")
@jwt_required()
def delete_contact(contact_id):
    current_user = get_jwt_identity()
    current_user_id = current_user["id"]
    user = db.session.scalars(select(User).filter_by(id=current_user_id)).first()
    if not user:
        return jsonify({"message": "User not found"}), 404
    contact = db.session.scalars(
        select(Contact).filter_by(id=contact_id, user_id=current_user_id)
    ).first()
    if not contact:
        return jsonify({"message": "Contact not found"}), 404
    db.session.delete(contact)
    db.session.commit()
    return jsonify({"message": "Contact deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)
