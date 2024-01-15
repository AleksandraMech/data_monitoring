from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
#from script_process_csv import process_csv
from .models import Note #, Graph
from . import db
from .models import Measurement
import json
import os #operating system, library
import pandas as pd
import psycopg2
import re
import numpy as np


views = Blueprint('views', __name__)

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
    user_id=current_user.id
    user_name=current_user.first_name

    return render_template("home.html", user=current_user,  user_id=user_id, user_name=user_name)


@views.route('/graph', methods=['GET', 'POST'])
@login_required

def graph():
        user_id=current_user.id
        user_name = current_user.first_name
        while True:     
            conn = psycopg2.connect(database="data_monitoring", user="postgres", password="albertina", host="localhost", port="5432")
           # if conn != None and user_id == 24:
            if conn != None:
                cur = conn.cursor()
                #sprawdzenie czy id zgadza sie z id pomiaru
                id = "SELECT json_info -> 'patient_id' as keyvalues FROM measurements" 
                cur.execute(id)
                patient_id_nr = [] 
                for(nr) in cur:
                    patient_id_nr.append(nr)
                    patient_id_numbers =  "".join(nr)
                patient_id_number = patient_id_numbers
                if 1==1:
                    #if 1==1:
                    if str(user_id) == str(patient_id_number):
                        #pobranie danych odnośnie pomiarów z bazy danych
                        otrzymane = "SELECT json_info -> 'HR' as keyvalues FROM measurements" 
                        cur.execute(otrzymane)
                        conn.commit()
                        value = [] 
                        min = None
                        max = None
                        mean = None
                        sum = 0
                        numbers = 0
                        for(HR) in cur:
                          #  value.append(HR)
                            value.insert(0,HR)
                        for n in value: 
                            con3 = re.findall(r'\d\d+', str(n))
                            nn = int(con3[0])
                            sum += nn
                            numbers += 1 
                            if min == None or min > n:
                                min = n
                                con = re.findall(r'\d\d+', str(min))
                                min_hr = int(con[0])
                            if max == None or max < n:
                                max = n 
                                con2 = re.findall(r'\d\d+', str(max))
                                max_hr = str(con2[0])
                        mean = round(sum/numbers) # round zookrągla do pełnej liczby
                        devicefromtable = "SELECT json_info -> 'context' as keyvalues FROM measurements order by measurements_id desc limit 10 " 
                        cur.execute(devicefromtable)
                        devices = [] 
                        for(context) in cur:
                           # devices.append(context)
                            devices.insert(0,context)
                            measurement_devices =  "".join(context)
                        measurement_device = measurement_devices
                        print('measurement device: ', measurement_device)
        
                        #pobranie daty z bazy danych
                        query = "SELECT json_info -> 'measurement_time' as keyvalues FROM measurements order by measurements_id desc limit 10" 
                        cur.execute(query)
                        conn.commit()
                        x = [] 
                        for(measurement_time) in cur:
                           # x.append(measurement_time)
                            x.insert(0,measurement_time)
                        data =[]
                        data2 =[]
                        for i in value: 
                                to_convert = re.findall(r'\d\d+', str(i)) 
                                converted = str(to_convert[0])
                                print('converted:', converted)        
                               # data.append(converted)
                                data.insert(0,converted)
                                print('data:', data)
            
                        for ii in x: 
                                to_convert2 = re.findall(r'\d+', str(ii))
                                print('to convert',to_convert)
                                year = str(to_convert2[0])
                                month = str(to_convert2[1])
                                day = str(to_convert2[2])
                                hour = str(to_convert2[3])
                                minute = str(to_convert2[4])
                                second = str(to_convert2[5]) 
                                y = (hour+':'+minute+':'+second)   
                                measure_day = (day+'-'+month+'-'+year)
                                print('y: ',y,'measure day: ', measure_day) 
                                data2.append(y) 
                                print('data2: ',data2) 
                        labels = data2
                        values = data       
                        #   new_graph = Graph(data=graph, user_id=current_user.id)
                        #  db.session.add(new_graph)
                        #  db.session.commit()
                        # flash('Graph added!', category='succes')
                        cur.close()
                        conn.close()                
                        return render_template("graph.html", measurement_device=measurement_device, labels = labels, values = values,  user=current_user, measure_day=measure_day, min_hr=min_hr, max_hr=max_hr, mean=mean)
                    else:
                        return render_template('nographs.html', user_first_name=user_name, user=user_id)
                

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()


# Create Admin Page
@views.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    user_id=current_user.id
    user_name = current_user.first_name
    if user_id == 24: 
        while True:     
            conn = psycopg2.connect(database="data_monitoring", user="postgres", password="albertina", host="localhost", port="5432")
            if conn != None:
                cur = conn.cursor()

                patient_id = 'SELECT patient_id FROM patient'
                cur.execute(patient_id)
                #print(patient_id)
                patients_id = [] 
                for(patient_id) in cur:    
                    convert = re.findall(r'\d\d+', str(patient_id)) 
                    converted = str(convert[0])
                    patients_id.append(converted)   
                    
                names= 'SELECT name FROM patient'
                cur.execute(names)
                patient_names = [] 
                for(names) in cur:         
                    patient_name =  "".join(names)
                    patient_names.append(patient_name)
                print(' patient_names : ', patient_names) #lista
                        
                mails= 'SELECT mail FROM patient'
                cur.execute(mails)
                patient_mails = [] 
                for(mails) in cur:         
                    mail =  "".join(mails)
                    patient_mails.append(mail)
                print(' patient_mails : ', patient_mails) #lista
                headings = ['Patient id', 'Name', 'Mail']
                return render_template("admin.html",  patient_mails=patient_mails, patients_id=patients_id, headings=headings, patient_names=patient_names, user=current_user,  user_id=user_id,   patient_name=patient_name)
    else:
         return render_template('admin2.html', user_first_name=user_name, user=current_user)
    

@views.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    user_id=current_user.id
    user_name=current_user.first_name
    user_email=current_user.email
    return render_template("user.html", user=current_user,  user_id=user_id, user_name=user_name, user_email=user_email)