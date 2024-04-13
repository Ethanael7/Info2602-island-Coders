from App.database import db

class Exercise(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False)
  category = db.Column(db.String(255), nullable=False)
  body_part = db.Column(db.String(255), nullable=False)
  workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'))
  videoLink = db.Column(db.String(1000), nullable=True)
  
  def get_json(self):
   return {
     'id': self.id,
     'name': self.name,
     'exercise_type': self.category,
     'Targeted_body_part': self.body_part,
   }