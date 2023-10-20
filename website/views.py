from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
from script_process_csv import process_csv
from .models import Note
from . import db
from .models import Measurement
import json
import os #operating system, library
import pandas as pd

views = Blueprint('views', __name__)

ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='succes')
            
    return render_template("home.html", user=current_user)

@views.route('/', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        
        file = request.files['file']
        if file and allowed_file(file.filename):
            values = pd.read_csv(file)
            new_values = Measurement(values, user_id=current_user.id)
            db.session.add(new_values)
            db.session.commit()
            flash('Measurement added!', category='succes')
            #filename = secure_filename(file.filename)
            #new_filename = f'{filename.split(".")[0]}_{str(datetime.now())}.csv'
            #save_location = os.path.join('input', new_filename) #save_ location to tam gdzie zapisuje ten plik(do input directory), musiałam zrobić import os
         #   file.save(save_location) 
           # output_file = process_csv(save_location)
             #return send_from_directory('output', output_file)
           # return redirect(url_for('download'))
           # return 'uploaded'
            
    return render_template("upload.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
