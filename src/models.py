from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#-------------------------------------CONTACT-----------------------------

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200), unique=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(150), nullable=True)
    phone = db.Column(db.String(150), nullable=True)
    memberships = db.relationship('Membership', backref='contact')

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
        """ Return a specific contact """
        return cls.query.get(id)

    @classmethod
    def delete_by_id(cls, id):
        """ Delete a contact by id """
        to_delete = cls.get_by_id(id)
        db.session.delete(to_delete)
        db.session.commit()

    @classmethod
    def put_by_id(cls, id, new_contact):
        """ Update all the info about a contact. Return the contact updated """
        #Contact to update info in the console
        print("Models: this is the contact to update:")
        print(new_contact)
        #Search by id the contact
        contact_to_update = Contact.query.get(id)
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
        contact_updated = Contact.query.filter_by(id=id).first()
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
            "memberships" : [m.group.serialize() for m in self.memberships]
        }


#---------------------------GROUP----------------------------------

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    memberships = db.relationship('Membership', backref='group')

    @classmethod
    def get_all(cls):
        """ Return all the groups available """
        return cls.query.all()

    @classmethod
    def create(cls, **kwargs):
        """ Create a new instance with the kwars passed """
        return cls(**kwargs)

    def serialize(self):
        """ Return a dictionary of the instance """
        return {
            "id" : self.id,
            "name" : self.name,
            "memberships" : self.memberships
        }
    
    def save(self):
        """ Save and commit a new contact """
        db.session.add(self)
        db.session.commit()


#------------------------------ MEMBERSHIP-------------------------------------

class Membership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    def serialize(self):
        """ Return a dictionary of the instance """
        return {
            "id" : self.id,
            "contact_id" : self.id,
            "group_id" : self.id
        }



"""     id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        } """