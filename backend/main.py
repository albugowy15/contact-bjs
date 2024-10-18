from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException
import json


app = Flask(__name__)
app.config.from_prefixed_env()
db = SQLAlchemy(app)

class Contact(db.Model):
    __tablename__ = "contacts"
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100))


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


@app.get("/v1/contacts")
def get_all_contacts():
    contacts = Contact.query.all()
    return jsonify(
        [
            {
                "id": c.id,
                "fullname": c.fullname,
                "phone_number": c.phone_number,
                "email": c.email,
            }
            for c in contacts
        ]
    )


@app.post("/v1/contacts")
def create_contact():
    data = request.json
    new_contact = Contact(
        fullname=data["fullname"],
        phone_number=data["phone_number"],
        email=data.get("email"),
    )
    db.session.add(new_contact)
    db.session.commit()
    return jsonify(
        {
            "id": new_contact.id,
            "fullname": new_contact.fullname,
            "phone_number": new_contact.phone_number,
            "email": new_contact.email,
        }
    ), 201


@app.put("/v1/contacts/<int:contact_id>")
def update_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    data = request.json
    contact.fullname = data.get("fullname", contact.fullname)
    contact.phone_number = data.get("phone_number", contact.phone_number)
    contact.email = data.get("email", contact.email)
    db.session.commit()
    return jsonify(
        {
            "id": contact.id,
            "fullname": contact.fullname,
            "phone_number": contact.phone_number,
            "email": contact.email,
        }
    )


@app.get("/v1/contacts/<int:contact_id>")
def get_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    return jsonify(
        {
            "id": contact.id,
            "fullname": contact.fullname,
            "phone_number": contact.phone_number,
            "email": contact.email,
        }
    )


@app.delete("/v1/contacts/<int:contact_id>")
def delete_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    db.session.delete(contact)
    db.session.commit()
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
