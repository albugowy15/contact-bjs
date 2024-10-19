import json

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
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

app = Flask(__name__)
app.config.from_prefixed_env()
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "*"}})

class Contact(db.Model):
    __tablename__ = "contacts"
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    response = e.get_response()
    response.data = json.dumps(
        {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return response


@app.route("/v1/protected", methods=["GET"])
@jwt_required()  # This ensures the user has a valid JWT token
def protected():
    current_user = get_jwt_identity()  # Get the identity from the JWT token
    return jsonify(logged_in_as=current_user), 200


# Custom response for expired tokens
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"message": "The token has expired."}), 401


@app.post("/v1/register")
def register():
    data = request.json
    password = data["password"]
    existing_user = User.query.filter_by(email=data["email"]).first()
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
    data = request.json
    email = data["email"]
    password = data["password"]

    # Find the user in the database by username
    user = User.query.filter_by(email=email).first()

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
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    contacts = Contact.query.filter_by(user_id=current_user_id).all()
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
    current_user = get_jwt_identity()
    user = User.query.get(current_user["id"])
    if not user:
        return jsonify({"message": "User not found"}), 404
    data = request.json
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
    current_user = get_jwt_identity()
    user_id = current_user["id"]

    contact = Contact.query.filter_by(id=contact_id, user_id=user_id).first()
    if not contact:
        return jsonify({"message": "Contact not found or you are not authorized"}), 404

    data = request.json

    contact.fullname = data.get("fullname", contact.fullname)
    contact.phone_number = data.get("phone_number", contact.phone_number)
    db.session.commit()

    return jsonify(
        {
            "data": {
                "id": contact.id,
                "fullname": contact.fullname,
                "phone_number": contact.phone_number,
            }
        }
    ), 200


@app.get("/v1/contacts/<int:contact_id>")
@jwt_required()
def get_contact(contact_id):
    current_user = get_jwt_identity()
    user_id = current_user["id"]
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    contact = Contact.query.filter_by(id=contact_id, user_id=user_id).first()
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
    user_id = current_user["id"]
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    contact = Contact.query.filter_by(id=contact_id, user_id=user_id).first()
    if not contact:
        return jsonify({"message": "Contact not found"}), 404
    db.session.delete(contact)
    db.session.commit()
    return jsonify({"message": "Contact deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)
