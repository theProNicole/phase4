from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates

from config import db

# Models go here!
class User(db.Model,SerializerMixin):
    __tablename__='users'

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String)
    email=db.Column(db.VarChar)
    #membership type and goal can be selected by drop downs in the front end
    membership_type=db.Column(db.String)
    goal=db.Column(db.String)
    
    #add relationships
    reviews=db.relationship('Review', back_populates='users', cascade='all, delete-orphan')
    reviews_gymLo=association_proxy('gym_locations', 'reviews')
    #add relationships
    assignments=db.relationship('Assignment',back_populates='user',cascade='all, delete-orphan')
    exercise=association_proxy('assignments','exercise')
    #rules
    serialize_rules=('-assignments','-exercise','-reviews')
    #validations
    @validates('name')
    def validate_name(self,key,name):
        if len(name)>1:
            return name
        else:
            raise ValueError('Name must be more than 1 character')



class GymLocation(db.Model,SerializerMixin):
    __tablename__='gym locations'

    id=db.Column(db.Integer, primary_key=True)
    location=db.Column(db.String, nullable=False)
    number_of_machines=db.Column(db.Integer)
    #relationships a gym location has many reviews
    reviews=db.relationship('Review', back_populates='gym_locations', cascade='all, delete-orphan')
    reviews_user=association_proxy('user', 'reviews')

    machines=db.relationship('Machines', back_populates='gym_location')
    trainers=db.relationship('Trainer', back_populates='gym_location')


class Exercise(db.Model,SerializerMixin):
    __tablename__='exercises'

    id=db.Column(db.Integer,primary_key=True)
    exercise_type=db.Column(db.String) #example:cardio
    exercise=db.Column(db.String)#example:Pushups
    #add relationships

    assignments=db.relationship('Assignment',back_populates='exercise',cascade='all,delete-orphan')
    user=association_proxy('assignments','user')

#assigns exercises to user
class Assignment(db.Model,SerializerMixin):
    __tablename__='assignments'

    #assignmenmts will be created by a form using post
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    user_goal=db.Column(db.String)
    exercise_id=db.Column(db.Integer,db.ForeignKey('exercises.id'))
    #add relationships
    user=db.relationship('User',back_populates='assignments')
    exercise=db.relationship('Exercise',back_populates='assignments')
    serialize_rules=('-user.assignments', '-exercise.assignments')


class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id=db.Column(db.Integer, primary_key=True)
    body=db.Column(db.String)
    created_at=db.Column(db.DateTime, server_default=db.func.now())
    updated_at=db.Column(db.DateTime, onupdate=db.func.now(), nullable=True)

    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    gym_location_id=db.Column(db.Integer,db.ForeignKey('gym locations.id'))
    # relationships
    users=db.relationship('User', back_populates='reviews')
    gym_locations=db.relationship('GymLocation', back_populates='reviews')

    @validates('body')
    def val_Reviews(self, key, value):
        if len(value)>5:
            return value
        else: 
            raise ValueError('Value too short. Must be more than 5 characters.')
        
class Machines(db.Model, SerializerMixin):
    __tablename__= 'machines'
    id=db.Column(db.Integer, primary_key=True)
    machine_name=db.Column(db.String)

    gym_locations_id=db.Column(db.Integer, db.ForeignKey('gym locations.id'))

    #relationship A Gym location has many machines
    gym_location=db.relationship('GymLocation', back_populates='machines') 


class Trainer(db.Model, SerializerMixin):
    __tablename__= 'trainers'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)

    gym_locations_id=db.Column(db.Integer, db.ForeignKey('gym locations.id'))

    #relationship A Gym location has many trainers
    gym_location=db.relationship('GymLocation', back_populates='trainers') 

