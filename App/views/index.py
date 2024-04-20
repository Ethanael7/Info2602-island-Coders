from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db
from App.controllers import initialize

index_views = Blueprint('index_views', __name__, template_folder='../templates') 

@index_views.route('/', methods=['GET'])
def login_page():
    return render_template('login.html')

@index_views.route('/signup-page', methods=['GET'])
def signup_page():
    return render_template('signup.html')

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})