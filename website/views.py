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
import psycopg2
import re
import numpy as np



views = Blueprint('views', __name__)
"""
ALLOWED_EXTENSIONS = set(['csv'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS """

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



@views.route('/graph', methods=['GET', 'POST'])
@login_required
def graph():
     while True:     
        conn = psycopg2.connect(database="data_monitoring", user="postgres", password="albertina", host="localhost", port="5432")
        if conn != None:
            cur = conn.cursor()
            otrzymane = "SELECT json_info -> 'values' as keyvalues FROM measurements" 
            cur.execute(otrzymane)
            conn.commit()
            value = [] 
            converted_value = []
            for(values) in cur:
                value.append(values)

            query = 'SELECT measurements_date FROM measurements'
            cur.execute(query)
            conn.commit()
            x = [] 
            converted_value = []
            for(measurements_date) in cur:
                x.append(measurements_date)
            cur.close()
            conn.close()       

            data =[]
            data2 =[]
            for i in value: 
                    to_convert = re.findall(r'\d\d+', str(i)) ##jak zmieniac wartosci w tym nawiasie???
                  #  converted = float(to_convert[0])
                    converted = str(to_convert[0])
                    print('converted:', converted)        
                    data.append(converted)
                    print('data:', data)
  
            for ii in x: 
                   # print('i:',i)
                    to_convert2 = re.findall(r'\d+', str(ii)) ##jak zmieniac wartosci w tym nawiasie???
                  #  converted = float(to_convert[0])
                    year = str(to_convert2[0])
                    month = str(to_convert2[1])
                    day = str(to_convert2[2])
                    hour = str(to_convert2[3])
                    minute = str(to_convert2[4])
                    second = str(to_convert2[5])
                  #  print('year:', year)  
                  #  print('month:', month)  
                  #  print('day:', day)  
                   # print('hour:', hour) 
                  #  print('minute:', minute)  
                   # print('second:', second)   
                    y = (hour+':'+minute+':'+second)   
                    measure_day = (day+'-'+month+'-'+year)
                    print('y: ',y,'measure day: ', measure_day) 
                    data2.append(y) 
                    print('data2: ',data2) 

            labels = [row[0] for row in data2]
            values = [row[1] for row in data]

            
            return render_template("graph.html", labels = labels, values = values,  user=current_user)

"""
@views.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        
        measurement = request.files['measurement']
        if measurement and allowed_file(measurement.filename):
            value = pd.read_csv(measurement)
            new_measurements = Measurement(value=measurement, user_id=current_user.id)
            db.session.add(new_measurements)
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
            
    return render_template("upload.html", user=current_user)     """               

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
""""
@views.route('/delete-graph', methods=['POST'])
def delete_graph():  
    graph = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    graphId = graph['graphId']
    graph = Graph.query.get(graphId)
    if graph:
        if graph.user_id == current_user.id:
            db.session.delete(graph)
            db.session.commit()

    return jsonify({})"""
