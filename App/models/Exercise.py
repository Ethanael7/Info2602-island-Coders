from App.database import db

class Exercise(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False)
  category = db.Column(db.String(255), nullable=False)
  body_part = db.Column(db.String(255), nullable=False)
  workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'))
  videoLink = db.Column(db.String(1000), nullable=True)

  def searchResults(q, Radio):
    matching_results = None

    if q == '' and Radio == 0:
        matching_results = Exercise.query.all()

    if q != '' and Radio == 0:
        matching_results = Exercise.query.filter(db.or_(Exercise.body_part.ilike(f'%{q}%'), Exercise.name.ilike(f'%{q}%'), Exercise.category.ilike(f'%{q}%')))

    if q == '' and Radio == 1:
        matching_results = Exercise.query.filter_by(category="Weight_Training")

    if q != '' and Radio == 1:
        matching_results = Exercise.query.filter(db.or_(Exercise.body_part.ilike(f'%{q}%'), Exercise.name.ilike(f'%{q}%'), Exercise.category.ilike(f'%{q}%')), Exercise.category == "Weight_Training")

    if q == '' and Radio == 2:
        matching_results = Exercise.query.filter_by(category="Cardio")

    if q != '' and Radio == 2:
        matching_results = Exercise.query.filter(db.or_(Exercise.body_part.ilike(f'%{q}%'), Exercise.name.ilike(f'%{q}%'), Exercise.category.ilike(f'%{q}%')), Exercise.category == "Cardio")
    
    if q == '' and Radio == 3:
        matching_results = Exercise.query.filter_by(category="Calisthenics")
    
    if q != '' and Radio == 3:
        matching_results = Exercise.query.filter(db.or_(Exercise.body_part.ilike(f'%{q}%'), Exercise.name.ilike(f'%{q}%'), Exercise.category.ilike(f'%{q}%')), Exercise.category == "Calisthenics")
    
    if q == '' and Radio == 4:
        matching_results = Exercise.query.filter_by(body_part="Legs")
    
    if q != '' and Radio == 4:
        matching_results = Exercise.query.filter(db.or_(Exercise.body_part.ilike(f'%{q}%'), Exercise.name.ilike(f'%{q}%'), Exercise.category.ilike(f'%{q}%')), Exercise.body_part == "Legs")

    if q == '' and Radio == 5:
        matching_results = Exercise.query.filter_by(body_part="Back")
    
    if q != '' and Radio == 5:
        matching_results = Exercise.query.filter(db.or_(Exercise.body_part.ilike(f'%{q}%'), Exercise.name.ilike(f'%{q}%'), Exercise.category.ilike(f'%{q}%')), Exercise.body_part == "Back")

    if q == '' and Radio == 6:
        matching_results = Exercise.query.filter_by(body_part="Chest")
    
    if q != '' and Radio == 6:
        matching_results = Exercise.query.filter(db.or_(Exercise.body_part.ilike(f'%{q}%'), Exercise.name.ilike(f'%{q}%'), Exercise.category.ilike(f'%{q}%')), Exercise.body_part == "Chest")

    if q == '' and Radio == 7:
        matching_results = Exercise.query.filter_by(body_part="Shoulders")
    
    if q != '' and Radio == 7:
        matching_results = Exercise.query.filter(db.or_(Exercise.body_part.ilike(f'%{q}%'), Exercise.name.ilike(f'%{q}%'), Exercise.category.ilike(f'%{q}%')), Exercise.body_part == "Shoulders")

    if q == '' and Radio == 8:
        matching_results = Exercise.query.filter_by(body_part="Arms")
    
    if q != '' and Radio == 8:
        matching_results = Exercise.query.filter(db.or_(Exercise.body_part.ilike(f'%{q}%'), Exercise.name.ilike(f'%{q}%'), Exercise.category.ilike(f'%{q}%')), Exercise.body_part == "Arms")

    if q == '' and Radio == 9:
        matching_results = Exercise.query.filter_by(body_part="Abs")
    
    if q != '' and Radio == 9:
        matching_results = Exercise.query.filter(db.or_(Exercise.body_part.ilike(f'%{q}%'), Exercise.name.ilike(f'%{q}%'), Exercise.category.ilike(f'%{q}%')), Exercise.body_part == "Abs")

    return matching_results
  
  def get_json(self):
   return {
     'id': self.id,
     'name': self.name,
     'exercise_type': self.category,
     'Targeted_body_part': self.body_part,
   }