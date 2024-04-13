from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

from .Exercise import*
from .Workout import*

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    workouts = db.relationship('Workout', backref='user', lazy=True, foreign_keys='Workout.user_id')


    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def removeWorkout(self, workout_id):
        alreadyAdded = next((workout for workout in self.workouts if workout.id == workout_id), None)
        if alreadyAdded:
            self.workouts.remove(alreadyAdded)
            db.session.commit()
            return
        return 

    def addPreBuiltWorkout(self, workout_id):
        preBuiltWorkout = Workout.query.filter_by(id=workout_id).first()
        if preBuiltWorkout:
            self.workouts.append(preBuiltWorkout)
            db.session.commit()
        return
    
    def createWorkout(self, exercise_id):
        newWorkout = Workout(exercise_id)
        db.session.add(newWorkout)
        self.workouts.append(newWorkout)
        db.session.commit()
        return
    
    def addExercise(self, workout_id, exercise_id):
        workout = next((workout for workout in self.workouts if workout.id == workout_id), None)
        if workout:
            workout.add_exercise(exercise_id)
            db.session.commit()
            return
        return

    def removeExercise(self, workout_id, exercise_id):
        workout = next((workout for workout in self.workouts if workout.id == workout_id), None)
        if workout:
            workout.remove_exercise(exercise_id)
            db.session.commit()
            return
        return

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

