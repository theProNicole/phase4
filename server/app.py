# !/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask_restful import Resource
from flask import Flask, request, make_response

# Local imports
from config import app, db, api,  migrate
from flask_cors import CORS
# Add your model imports
from models import db, User, Exercise, Assignment, GymLocation, Trainer, Review
CORS(app)

class Users(Resource):
    def get(self):
        users=[e.to_dict() for e in User.query.all()]
        return make_response(users,200)
    
    #method below will run when new user is made
    def post(self):
        data=request.json
        try:
            new_user=User(name=data['name'],goal=data['goal'],membership_type=data['membership_type'])
        except ValueError as v_error:
            return make_response({'error':[str(v_error)]},400)
        except KeyError as k_error:
            return make_response({'error':[str(f'{k_error}''is missing')]},400)
        db.session.add(new_user)
        db.session.commit()
        return make_response(new_user.to_dict(),201)
api.add_resource(Users,'/users')

class Usersbyid(Resource):
    def get(self,id):
        user=User.query.get(id)
        if not user:
            return make_response({'error':'User not found'},404)
        return make_response(user.to_dict(rules=('name','membership_type','id','goal','-assignments.user','-assignments.exercise_id','-assignments.user_goal','-assignments.user_id')),200)
    def delete(self,id):
        user=User.query.get(id)
        if not user:
            return make_response({'error':'User cannot be deleted because user does not exist'})
        db.session.delete(user)
        db.session.commit()
        return make_response('',204)
api.add_resource(Usersbyid,'/users/<int:id>')

class Assignments(Resource):
    def get(self):
        assignments=[e.to_dict() for e in Assignment.query.all()]
        return make_response(assignments,200)
    def post(self):
        data=request.json
        try:
            new_assignment=Assignment(user_id=data['user_id'],exercise_id=data['exercise_id'],user_goal=data['user_goal'])
        except KeyError as k_error:
            return make_response({'error':[str(f'{k_error}''is missing')]},400)
        db.session.add(new_assignment)
        db.session.commit()
        return make_response(new_assignment.to_dict(),201)
api.add_resource(Assignments,'/assignments')

class Assignmentsbyid(Resource):
    def get(self,id):
        assignment=Assignment.query.get(id)
        if not assignment:
            return make_response({'error':'assignment not found'},404)
        return make_response(assignment.to_dict(rules=('-user_goal','-user_id')),200)
        
    def delete(self,id):
        assignment=Assignment.query.get(id)
        if not assignment:
            return make_response({'error':'cannot delete assignment as it does not exist'})
        db.session.delete(assignment)
        db.session.commit()
        return make_response('',204)
api.add_resource(Assignmentsbyid,'/assignments/<int:id>')

class Exercises(Resource):
    def get(self):
        exercises=[e.to_dict(rules=('exercise','-assignments')) for e in Exercise.query.all()]
        return make_response(exercises,200)
    def post(self):
        data=request.json
        try:
            new_exercise=Exercise(exercise_type=data['exercise_type'],exercise=data['exercise'])
        except KeyError as k_error:
            return make_response({'error':[str(f'{k_error}''is missing')]},400)
        db.session.add(new_exercise)
        db.session.commit()
        return make_response(new_exercise.to_dict(rules=('-assignments',)),201)
api.add_resource(Exercises,'/exercises')

class Exercisesbyid(Resource):
    def get(self,id):
        exercise=Exercise.query.get(id)
        if not exercise:
            return make_response({'error':'exercise not found'},404)
        return make_response(exercise.to_dict(rules=('-assignments',)),200)
    
    def delete(self,id):
        exercise=Exercise.query.get(id)
        if not exercise:
            return make_response({'error':'Cannot delete as exercise does not exist'},404)
        db.session.delete(exercise)
        db.session.commit()
        return make_response('',204)
api.add_resource(Exercisesbyid,'/exercises/<int:id>')

class GymLocations(Resource):

    def get(self):
        all_gym_locations=[location.to_dict(rules=('-machines','-trainers', '-reviews')) for location in GymLocation.query.all()]
        return make_response(all_gym_locations, 200)
api.add_resource(GymLocations,'/gym_locations')

class GymLocationById(Resource):

    def get(self, id):
        gym_Id=GymLocation.query.filter_by(id = id).first()
        if not gym_Id:
            return make_response({'error':'Gym location does not exist'}, 404)
        return make_response(gym_Id.to_dict(rules=('-machines.gym_location', '-trainers.gym_location', '-reviews')), 200)              
api.add_resource(GymLocationById, '/gym_locations/<int:id>')

class GymReviews(Resource):
    def get(self):
        review_Id=[reviews.to_dict(rules=( '-users', '-gym_locations', '-reveiws')) for reviews in Review.query.all()]
        return make_response(review_Id, 200)

    def post(self): 
        param = request.json
        try:
            new_review = Review(body=param['body'])
        except:
            return make_response({"error":"error"})
        db.session.add(new_review)
        db.session.commit()
        return make_response(new_review.to_dict(rules=('created_at', '-users', '-gym_locations', '-reveiws')), 201)
api.add_resource(GymReviews, '/reviews')

class ReviewById(Resource):

    def get(self, id):
        review_Id= Review.query.filter_by(id=id).first()
        if not review_Id:
            return make_response({'error':'review does not found'}, 404)
        return make_response(review_Id.to_dict( rules=('-users', '-gym_locations', '-reveiws',)), 200)
    
    def patch(self, id):
        review_Id = Review.query.filter_by(id=id).first()
        if not review_Id:
            return make_response({'error':'review does not found'}, 404)
        param = request.json
        for attr in param:
            setattr( review_Id, attr, param[attr] )
        db.session.commit()
        return make_response( review_Id.to_dict(rules=('updated_at','-users', '-gym_locations', '-reveiws')), 200)
    
    def delete(self, id):
        review_id = Review.query.filter_by( id=id ).first()
        if not review_id:
            return make_response( { 'error': 'review not found' }, 404 )
        db.session.delete( review_id )
        db.session.commit()
        return make_response( '', 204 )
        
api.add_resource(ReviewById, '/reviews/<int:id>')    

class Trainers(Resource):

    def get(self):
        all_trainers = [trainer.to_dict(rules=('-gym_location','-trainers')) for trainer in Trainer.query.all()]
        return make_response(all_trainers, 200)

api.add_resource(Trainers, '/trainers')

class TrainersById(Resource):
    def get_trainer_by_id(id):
        trainer = Trainer.query.get(id)
        if not trainer:
            return make_response({'error': 'Trainer does not exist'}, 404)
        return make_response(trainer.to_dict(rules=('-gym_location','-trainers')), 200)
api.add_resource(TrainersById, '/trainers/<int:id>')
# Views go here!

@app.route('/')
def index():
    return '<h1>Prohect Server</h1>'

if __name__ == '__main__':
    app.run(port=5555, debug=True)

