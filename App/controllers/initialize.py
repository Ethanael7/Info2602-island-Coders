from App.models import*
from .user import*
import os, csv

def initialize():
    db.drop_all()
    db.create_all()
    
    with open('App/static/exercises.csv', newline='', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            exercise = Exercise(id=row['id'], name=row['name'], category=row['exercise_type'], body_part=row['Targeted_body_part'], videoLink=row['Video_Link'])
            db.session.add(exercise)
    create_user('bob', 'bobpass')
    create_user('2', '2')
    user = User.query.filter_by(username='bob').first()
    user.createWorkout(1)
    workout = next((workout for workout in user.workouts if workout.id == 1), None)
    workout.add_exercise(2)
    workout.add_exercise(3)
    workout.add_exercise(4)
    workout.add_exercise(5)
    user.createWorkout(6)
    workout = next((workout for workout in user.workouts if workout.id == 2), None)
    workout.add_exercise(7)
    workout.add_exercise(8)
    workout.add_exercise(9)
    workout.add_exercise(10)
    user.createWorkout(11)
    workout = next((workout for workout in user.workouts if workout.id == 3), None)
    workout.add_exercise(12)
    workout.add_exercise(13)
    workout.add_exercise(14)
    workout.add_exercise(15)
    db.session.commit()