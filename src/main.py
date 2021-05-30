"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Contact, Group, Membership
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


#_-------------------------------CONTACT REQUEST--------------------------------

@app.route('/contact/all', methods=["GET"])
def get_contacts():
    """ Recibe all the contacts from the db and return them in json """
    contact_list = Contact.get_all()
    contact_list_dict = list(map(lambda elem: elem.serialize(), contact_list)) 
    return jsonify(contact_list_dict), 200

@app.route('/contact', methods=['POST'])
def create_contact():
    """ Recibe data to create a new contact """
    #request in json
    request_body = request.json
    #Add to db the request
    new_contact = Contact.create(
        full_name = request_body["full_name"], 
        email = request_body["email"],
        address = request_body["address"],
        phone = request_body["phone"]
    )
    #Save and commit new_contact
    #db.session.add(new_contact)
    #Commit contact
    #db.session.commit()

    #Save and commit new_contact
    new_contact.save()
    #Return a response
    return jsonify(
        {
            "contact" : new_contact.serialize(),
            "response" : "Your contact was added successfully"
        }
    ), 200


@app.route('/contact/<int:id>', methods=['GET', 'DELETE'])
def get_by_id (id):
    """ Obtain a specific contact through the id """
    if request.method == 'GET':
        #Find the contact
        contact_by_id = Contact.get_by_id(id)
        return jsonify(contact_by_id.serialize()), 200
    else: 
        contact_to_delete = Contact.get_by_id(id)
        Contact.delete_by_id(id)
        return f"The contact with id: {id} was eliminated successfully", 200

@app.route('/contact/<int:id>', methods=['PUT'])
def update_contact(id):
    """ Update a contact completely  """
    #Request to json
    request_body = request.json
    print("Este es el request:")
    print(request_body)
    #Find the contact to update
    contact_updated = Contact.put_by_id(id, request_body)
    return jsonify(
        {
            "response" : "The contact was updated successfully ",
            "contact" : contact_updated.serialize()
        }
    ), 200



#------------------------------GROUP REQUESTS-----------------------------------

@app.route('/group/all', methods=["GET"])
def get_groups():
    """ Recibe all the groups from the db and return them in json """
    group_list = Group.get_all()
    group_list_dict = list(map(lambda elem: elem.serialize(), group_list)) 
    return jsonify(group_list_dict), 200

@app.route('/group', methods=['POST'])
def create_group():
    """ Recibe data to create a new group """
    #request in json
    request_body = request.json
    #Add to db the request
    new_group = Group.create(
        name = request_body["name"]
    )

    #Save and commit new_contact
    new_group.save()
    #Return a response
    return jsonify(
        {
            "group" : new_group.serialize(),
            "response" : "Your group was added successfully"
        }
    ), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
