from App.database import db
from .Exercise import*
from flask import flash

class Workout(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  exercises = db.relationship('Exercise', backref='workout', lazy=True, foreign_keys='Exercise.workout_id')

  def __init__(self, exercise_id):
    exercise = Exercise.query.filter_by(id=exercise_id).first()
    self.exercises.append(exercise)
  
  def add_exercise(self, exercise_id):
    alreadyAdded = next((exercise for exercise in self.exercises if exercise.id == exercise_id), None)
    if not alreadyAdded:
        exercise = Exercise.query.filter_by(id=exercise_id).first()
        self.exercises.append(exercise)
        db.session.commit()
        return
    flash("Exercise already added to this workout!")
    return 
  
  def remove_exercise(self, exercise_id):
    alreadyAdded = next((exercise for exercise in self.exercises if exercise.id == exercise_id), None)
    if alreadyAdded:
        self.exercises.remove(alreadyAdded)
        db.session.commit()
        return
    return 

  def get_json(self):
   return {
     'id': self.id,
     'name': self.name,
     'exercise_type': self.category,
     'Targeted_body_part': self.body_part,
   }