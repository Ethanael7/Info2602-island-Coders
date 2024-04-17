from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies
from sqlalchemy.exc import IntegrityError


from .index import index_views 

from App.models import*

from App.controllers import (
    login,
    get_all_users,
    create_user
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')



'''
Page/Action Routes
'''    
@auth_views.route('/home', methods=['GET'])
@jwt_required()
def index_page():
    return render_template('index.html')

@auth_views.route('/browseExercises_page/', methods=['GET'])
@auth_views.route('/browseExercises_page/add/<int:exercise_id>', methods=['GET'])
@auth_views.route('/browseExercises_page/add/<int:exercise_id>/<int:workout_id>', methods=['GET'])
@auth_views.route('/browseExercises_page/remove/<int:workout_id>', methods=['GET'])
@auth_views.route('/browseExercises_page/newWorkout/<int:intNewWorkout>/<exercise_id>', methods=['GET'])
@jwt_required()
def browseExercises_page(workout_id=None, exercise_id=None, intNewWorkout=0):

    q = request.args.get('q', default='', type=str)

    Radio = request.args.get('Radio', default=0, type=int)

    exercises = Exercise.searchResults(q, Radio)

    if intNewWorkout == 1:
        new_workout = True
    else:
        new_workout = False
        
    return render_template('browseExercises.html', exercises=exercises, workout_id=workout_id, exercise_id=exercise_id, new_workout=new_workout, q=q, Radio=Radio)

@auth_views.route('/addExercise/<int:exercise_id>/<int:workout_id>', methods=['POST'])
@jwt_required()
def addExercise_action(exercise_id, workout_id):
    current_user.addExercise(workout_id, exercise_id)
    return redirect(url_for('auth_views.browseExercises_page'))

@auth_views.route('/removeExercise/<int:exercise_id>/<int:workout_id>', methods=['POST'])
@jwt_required()
def removeExercise_action(exercise_id, workout_id):
    current_user.removeExercise(workout_id, exercise_id)
    return redirect(url_for('auth_views.manageWorkouts_page'))

@auth_views.route('/removeWorkout/<int:workout_id>', methods=['POST'])
@jwt_required()
def removeWorkout_action(workout_id):
    current_user.removeWorkout(workout_id)
    return redirect(url_for('auth_views.browseExercises_page'))

@auth_views.route('/createWorkout/<int:exercise_id>', methods=['POST'])
@jwt_required()
def createWorkout_action(exercise_id):
    current_user.createWorkout(exercise_id)
    return redirect(url_for('auth_views.browseExercises_page'))

@auth_views.route('/manageWorkouts_page', methods=['GET'])
@auth_views.route('/remove/<int:exercise_id>/<int:workout_id>', methods=['GET'])
@jwt_required()
def manageWorkouts_page(exercise_id=None, workout_id=None):
    return render_template('manageWorkouts.html', exercise_id=exercise_id, workout_id=workout_id)

@auth_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_page():
    return render_template('message.html', title="Identify", message=f"You are logged in as {current_user.id} - {current_user.username}")
    

@auth_views.route('/login', methods=['POST'])
def login_action():
    response = None
    username = request.form['username']
    password = request.form['password']
    token = login(username, password)
    if token == None:
        flash('Bad username or password given'), 401
        response = redirect(url_for('index_views.login_page'))
        return response
    else:
        flash('Login Successful')
        response = redirect(url_for('auth_views.index_page'))
        set_access_cookies(response, token) 
        return response

    
    
@auth_views.route("/signup", methods=['POST'])
def signup_action():
  response = None
  try:
    username = request.form['username']
    password = request.form['password']
    user = create_user(username, password)
    response = redirect(url_for('index_views.login_page'))
    flash('Account created')
  except IntegrityError:
    flash('Username already exists')
    response = redirect(url_for('index_views.signup_page'))
  return response


@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = redirect(url_for('index_views.login_page')) 
    flash("Logged Out!")
    unset_jwt_cookies(response)
    return response

    

'''
API Routes
'''
@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
  data = request.json
  token = login(data['username'], data['password'])
  if not token:
    return jsonify(message='bad username or password given'), 401
  response = jsonify(access_token=token) 
  set_access_cookies(response, token)
  return response

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})

@auth_views.route('/api/logout', methods=['GET'])
def logout_api():
    response = jsonify(message="Logged Out!")
    unset_jwt_cookies(response)
    return response