from flask_restx import Namespace, Resource, fields
from ..Model.contacts import Contacts
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus


contact_namespace = Namespace("contact", description="a namespace for contact",
                              decorators=[jwt_required()], path='/contact')


contact_model = contact_namespace.model(
    "Contact",
    {
        "id": fields.Integer(readOnly=True),
        "name": fields.String(required=True, description="A name"),
        "phone_number": fields.String(required=True, description="A phone number"),
        "email": fields.String(required=True, description="An email"),
        "user_id": fields.Integer(required=True, description="A user id", readOnly=True),
    },
)


# create, get, update, delete a contact
@contact_namespace.route("/contact")
class Contact(Resource):
    @contact_namespace.expect(contact_model)
    @contact_namespace.response(
        HTTPStatus.CREATED, "Contact created successfully", contact_model
    )
    def post(self):
        """Create a contact"""
        data = contact_namespace.payload
        name = data.get("name").lower()
        phone_number = data.get("phone_number")
        email = data.get("email").lower()
        user_id = get_jwt_identity()

        contact = Contacts(
            name=name, 
            phone_number=phone_number,
            email=email,
            user_id=user_id)
        contact.save()
        return contact

    @contact_namespace.response(HTTPStatus.OK, "Contact retrieved successfully", contact_model)
    def get(self):
        """Get all contacts"""
        user_id = get_jwt_identity()
        contacts = Contacts.query.filter_by(user_id=user_id).all()
        return contacts
