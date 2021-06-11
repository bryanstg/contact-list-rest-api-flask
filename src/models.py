from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Crud(object):
    @classmethod
    def create(cls, **kwargs):
        """ Create and return an instance """
        return cls(**kwargs)

    @classmethod
    def get_all(cls):
        """ Get all the elements from the table """
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        """ Return a specific instance from the table """
        return cls.query.get(id)

    @classmethod
    def delete_by_id(cls, id):
        """ Delete an instance from db by id """
        to_delete = cls.get_by_id(id)
        db.session.delete(to_delete)
        db.session.commit()




#-------------------------------------CONTACT-----------------------------

class Contact(db.Model, Crud):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200), unique=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(150), nullable=True)
    phone = db.Column(db.String(150), nullable=True)
    memberships = db.relationship('Membership', backref='contact')

    @classmethod
    def put_by_id(cls, id, new_contact):
        """ Update all the info about a contact. Return the contact updated """
        #Contact to update info in the console
        print("Models: this is the contact to update:")
        print(new_contact)
        #Search by id the contact
        contact_to_update = cls.query.get(id)
        contact_dict = contact_to_update.serialize()
        print("models: contact to update")
        print(contact_to_update.serialize())
        #Assing the values of the contact
        contact_to_update.phone = new_contact["phone"]
        contact_to_update.email = new_contact["email"]
        contact_to_update.address = new_contact["address"]
        contact_to_update.full_name = new_contact["full_name"]
        contact_to_update.membership = contact_dict["memberships"]
        #Save the info to the db
        db.session.commit()
        #Check the console to compare before and after update
        contact_updated = cls.query.filter_by(id=id).first()
        print("models: contact updated")
        print(contact_updated.serialize())
        return contact_updated

    def save(self):
        """ Save and commit a new contact """
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        """ Return a dictionary of the instance """
        return {
            "id" : self.id,
            "full_name" : self.full_name,
            "email" : self.email,
            "address" : self.address,
            "phone" : self.phone,
            "groups" : [m.group.minialize() for m in self.memberships]
        }
    
    def minialize(self):
        """ Return a resume dictionary of the instance """
        return {
            "id": self.id,
            "full_name": self.full_name,
            "phone": self.phone,
        }


#---------------------------GROUP----------------------------------

class Group(db.Model, Crud):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    memberships = db.relationship('Membership', backref='group')

    @classmethod
    def put_by_id(cls, id, new_group):
        """ Update all the info about a group. Return the group updated """
        #Group to update info in the console
        print("Models: this is the group to update:")
        print(new_group)
        #Search the group by id
        group_to_update = cls.query.get(id)
        group_dict = group_to_update.serialize()
        print("models: contact to update")
        print(group_to_update.serialize())
        #Assing the values of the group
        group_to_update.name = new_group["name"]
  
        #Save the info to the db
        db.session.commit()
        #Check the console to compare before and after update
        group_updated = cls.query.filter_by(id=id).first()
        print("models: group updated")
        print(group_updated.serialize())
        return group_updated

    def minialize(self):
        """ Return a resume dictionary of the instance """
        return {
            "id": self.id,
            "name": self.name,
        }

    def serialize(self):
        """ Return a dictionary of the instance """
        return {
            "id" : self.id,
            "name" : self.name,
            "contacts" : [m.contact.minialize() for m in self.memberships]
        }
    
    def save(self):
        """ Save and commit a new contact """
        db.session.add(self)
        db.session.commit()


#------------------------------ MEMBERSHIP-------------------------------------

class Membership(db.Model, Crud):
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    
    
    @classmethod
    def put_by_id(cls, id, new_membership):
        """ Update all the info about a membership. Return the membership updated """
        #Membership to update info in the console
        print("Models: this is the membership to update:")
        print(new_membership)
        #Search the membership by id
        membership_to_update = cls.query.get(id)
        membership_dict = membership_to_update.serialize()
        print("models: membership to update")
        print(membership_to_update.serialize())
        #Assing the values of the membership
        membership_to_update.contact_id = membership_dict["contact_id"]
        membership_to_update.group_id = membership_dict["group_id"]
        #Save the info to the db
        db.session.commit()
        #Check the console to compare before and after update
        membership_updated = cls.query.filter_by(id=id).first()
        print("models: membership updated")
        print(membership_updated.serialize())
        return membership_updated

    def serialize(self):
        """ Return a dictionary of the instance """
        return {
            "id" : self.id,
            "contact_id" : self.contact_id,
            "group_id" : self.group_id
        }

    def save(self):
        """ Save and commit a new membership """
        db.session.add(self)
        db.session.commit()
