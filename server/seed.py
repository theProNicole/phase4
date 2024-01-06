#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app

from models import db, User, GymLocation, Exercise, Assignment, Review, Machines, Trainer


if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Deleting date...")
        User.query.delete()
        GymLocation.query.delete()
        Exercise.query.delete()
        Assignment.query.delete()
        Review.query.delete()
        Trainer.query.delete()
        Machines.query.delete()


        print("Starting seed...")
        # Seed code goes here!
        print('Making users')
        u1=User(name=fake.name(),membership_type='starter',goal='get big')
        u2=User(name=fake.name(),membership_type='starter',goal='get big')
        u3=User(name=fake.name(),membership_type='Pro',goal='get lean')
        u4=User(name=fake.name(),membership_type='Pro',goal='Tone up')
        users=[u1,u2,u3,u4]

        print('Making Gym Locations')

        g1=GymLocation(location=fake.address(),number_of_machines=12)
        g2=GymLocation(location=fake.address(),number_of_machines=12)
        g3=GymLocation(location=fake.address(),number_of_machines=12)
        g4=GymLocation(location=fake.address(),number_of_machines=12)
        gyms=[g1,g2,g3,g4]

        print('Making exercises')
        
        e1=Exercise(exercise_type="Cardio",exercise='Running')
        e2=Exercise(exercise_type="Cardio",exercise='Jump Rope')
        e3=Exercise(exercise_type="Strength",exercise='Weight lifting')
        e4=Exercise(exercise_type="Power",exercise='delayed lifts')

        exer=[e1,e2,e3,e4]

        print('making assignments')


        a1=Assignment(user_id=1,user_goal='get big',exercise_id=3)
        a2=Assignment(user_id=2,user_goal='get big',exercise_id=4)
        a3=Assignment(user_id=3,user_goal='get lean',exercise_id=2)
        a4=Assignment(user_id=4,user_goal='tone up',exercise_id=1)
        assignments=[a1,a2,a3,a4]

        print('making reviews')
        r1=Review(user_id=1,body='"Very nice gym!"', gym_location_id=1)#,created_at=fake.date(),gym_location_id= 3)
        r2=Review(user_id=2,body='"Staff is awesome!"', gym_location_id=2)#,created_at=fake.date(),gym_location_id= 4)
        r3=Review(user_id=3,body='"It\'s eh"',gym_location_id=3)#,created_at=fake.date(),gym_location_id= 2)
        r4=Review(user_id=4,body='"4 stars"', gym_location_id=4)#,created_at=fake.date(),gym_location_id= 1)
        reviews=[r1,r2,r3,r4]

        print('printing machines')
        m1=Machines(machine_name='Bench press, Tread Mills, Squat racks, Smith Machine, Dumb Bells', gym_locations_id=1 )
        m2=Machines(machine_name='Bench press, Tread Mills, Squat racks, Smith Machine, Dumb Bells', gym_locations_id=2 )
        m3=Machines(machine_name='Bench press, Tread Mills, Squat racks, Smith Machine, Dumb Bells', gym_locations_id=3 )
        m4=Machines(machine_name='Bench press, Tread Mills, Squat racks, Smith Machine, Dumb Bells', gym_locations_id=4 )
        machines=[m1, m2, m3, m4]

        print('printing trainers')
        t1=Trainer(name=fake.name(), gym_locations_id=1)
        t2=Trainer(name=fake.name(), gym_locations_id=1)
        t3=Trainer(name=fake.name(), gym_locations_id=1)
        t4=Trainer(name=fake.name(), gym_locations_id=2)
        t5=Trainer(name=fake.name(), gym_locations_id=2)
        t6=Trainer(name=fake.name(), gym_locations_id=3)
        t7=Trainer(name=fake.name(), gym_locations_id=3)
        t8=Trainer(name=fake.name(), gym_locations_id=4)
        t9=Trainer(name=fake.name(), gym_locations_id=4)
        t10=Trainer(name=fake.name(), gym_locations_id=4)
        trainer=[t1, t2, t3, t4, t5, t6, t7, t8, t9, t10]
        

        db.session.add_all(assignments)
        db.session.add_all(exer)
        db.session.add_all(gyms)
        db.session.add_all(users)
        db.session.add_all(reviews)
        db.session.add_all(machines)
        db.session.add_all(trainer)
        db.session.commit()


        print('seeding done!')

