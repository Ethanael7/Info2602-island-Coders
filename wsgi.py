import os, csv
import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup
from App.models import*

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users )

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
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
    print('database intialized')

@app.cli.command('show-exercises', help="shows a list of all exercises")
def show_exercises():
    exercises = Exercise.query.all()
    for exercise in exercises:
        print(f"id = {exercise.id}, name = {exercise.name}, category = {exercise.category}, body part = {exercise.body_part}, videoLink = {exercise.videoLink}")
    return

@app.cli.command('show-workouts', help="shows a list of all workouts fo a user")
@click.argument("username")
def show_workouts(username):
    user = User.query.filter_by(username=username).first()
    if user:
        for workout in user.workouts:
            for exercise in workout.exercises:
                print(f"id = {exercise.id}, name = {exercise.name}, category = {exercise.category}, body part = {exercise.body_part}, videoLink = {exercise.videoLink}")
    return
'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the command
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)