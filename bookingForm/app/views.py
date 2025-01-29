from werkzeug.utils import redirect
from app import app, db
from app.models import MovieMakerBookingDB
from flask import json, render_template, request, session, url_for, jsonify, flash
#from fpdf import FPDF
import os


@app.route('/')
def index():
    return render_template('homepage.html')


@app.route('/add', methods=['POST'])
def add_customer():
    form = request.form

    customer = MovieMakerBookingDB(
        name=form['name'],
        email=form['email-address'],
        course=form['course'],

    )
    #comment = form['comment']

    db.session.add(customer)
    db.session.commit()
    return "Booking Made"
