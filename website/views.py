from flask import Blueprint, render_template, request, flash, session
from flask_login import login_required, current_user
from datetime import datetime
from .models import Note
from . import db
import json
import psycopg2
import re
from flask import Flask, redirect, url_for, render_template, session
from flask_wtf import FlaskForm
from wtforms.fields import DateField, TimeField
from wtforms.validators import DataRequired
from wtforms import validators, SubmitField
import datetime
import website.cfg as cfg


views = Blueprint('views', __name__)

class InfoForm(FlaskForm):
    date = DateField('Measurement date', format='%Y-%m-%d', default=datetime.datetime.now(), validators=(validators.DataRequired(),))
    enddate = DateField('End Date', format='%Y-%m-%d',  default=datetime.datetime.now(), validators=(validators.DataRequired(),))
    submit = SubmitField('Send')
    def validate_enddate(self, filed):
        if filed.data <= self.date.data:
             flash('Finish date must more or equal start date.', category='error')            
class InfoFormTime(FlaskForm):
    time = TimeField('Measurement time', format='%H.%M')
    endtime = TimeField('Measurement time', format='%H.%M')
    submit = SubmitField('Submit')
   
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

@views.route('/history', methods=['GET','POST'])
@login_required
def date():
    user_id=current_user.id
    user_name = current_user.first_name
    while True:   
            conn = psycopg2.connect(database=cfg.database, user=cfg.postgres_user, password=cfg.postgres_password, host=cfg.host, port=cfg.port)
            if conn != None:
                cur = conn.cursor()
                #sprawdzenie czy id zgadza sie z id pomiaru
                id = "SELECT json_info -> 'patient_id' as keyvalues FROM measurements where cast(json_info ->> 'patient_id' as INTEGER) = ( \'"+str(user_id)+"\') " 
                cur.execute(id)
                row = cur.fetchone()
                if row is None:
                     return render_template('nographs.html', user_first_name=user_name, user=current_user)
                else:
                    patient_id_nr = [] 
                    for(nr) in cur:
                        patient_id_nr.append(nr)
                        patient_id_numbers =  "".join(nr)
                    patient_id_number = patient_id_numbers
                    #dodanie formularzy odczytujących datę podaną przez użytkownika w zakładce history
                    form = InfoForm()
                    session['date'] = datetime.datetime.now()
                    session['enddate'] = datetime.datetime.now()
                    if form.validate_on_submit():
                        session['date'] = form.date.data
                        session['enddate'] = form.enddate.data
                    else:
                        date = datetime.datetime.now()
                        enddate = datetime.datetime.now()   
                    date = session['date']
                    enddate = session['enddate']
                    form2 = InfoFormTime()
                    if form2.validate_on_submit():
                            session['time'] = form2.time.data
                            session['endtime'] = form2.endtime.data
                    else:
                        time = '(00:00:00)'
                        enddate = '(00:00:00)'

                    if  session['date']  == datetime.datetime.now() :
                        return render_template('emptyhistory.html', form=form, form2=form2, user=current_user)
                    else:
                        dzien =  "SELECT json_info -> 'measurement_time' as keyvalues FROM measurements WHERE json_info ->> 'measurement_time' > ( \'"+str(date)+"\')  AND json_info ->> 'measurement_time' < ( \'"+str(enddate)+"\') AND cast(json_info ->> 'patient_id' as INTEGER) = ( \'"+str(user_id)+"\') order by measurements_id desc limit 1" 
                        cur.execute(dzien)
                        conn.commit()
                        for(dzien) in cur:
                            if str(user_id) == str(patient_id_number):
                                #pobranie danych odnośnie pomiarów z bazy danych
                                otrzymane3 = "SELECT json_info -> 'HR' as keyvalues FROM measurements WHERE json_info ->> 'measurement_time' > ( \'"+str(date)+"\')  AND json_info ->> 'measurement_time' < ( \'"+str(enddate)+"\') AND cast(json_info ->> 'patient_id' as INTEGER) = ( \'"+str(user_id)+"\') order by measurements_id desc --limit 20" 
                                #dodać warunek że jeżeli nie ma takiej daty to con.rollback
                                cur.execute(otrzymane3)
                                conn.commit()
                                value = [] 
                                min = None
                                max = None
                                mean = None
                                sum = 0
                                numbers = 0
                                for(HR) in cur:
                                # value.append(HR)
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
                                #pobranie daty z bazy danych
                                query = "SELECT json_info -> 'measurement_time' as keyvalues FROM measurements WHERE json_info ->> 'measurement_time' > ( \'"+str(date)+"\') AND json_info ->> 'measurement_time' < ( \'"+str(enddate)+"\') AND cast(json_info ->> 'patient_id' as INTEGER) = ( \'"+str(user_id)+"\')  order by measurements_id desc --limit 20" 
                                cur.execute(query)
                                conn.commit()
                                x = [] 
                                for(measurement_time) in cur:
                                    x.insert(0,measurement_time) # aby czas był dobrze sortowany
                                data =[]
                                data2 =[]
                                data4 = []
                                data5 = []
                                for i in value: 
                                        to_convert = re.findall(r'\d\d+', str(i)) 
                                        converted = str(to_convert[0])     
                                        data.append(converted)
                                for ii in x: 
                                        to_convert2 = re.findall(r'\d+', str(ii))
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
                                        data4.append(measure_day)
                                        dzienigodzina = (measure_day+' '+y)
                                        data5.append(dzienigodzina)
                                labels2 = data5
                                values2 = data      
                                cur.close()
                                conn.close()    
                                return render_template('history.html', form=form, form2=form2, labels2 = labels2, values2 = values2,  user_id= user_id, user=current_user, measure_day=measure_day, min_hr=min_hr, max_hr=max_hr, mean=mean)
                        else: 
                            flash('W podanym zakresie dat nie ma żadnych pomiarów. Wybierz inne daty.', category='error')
                            return render_template('emptyhistory.html', form=form, form2=form2, user=current_user)
                                    

@views.route('/graph', methods=['GET', 'POST'])
@login_required
def graph():
        user_id=current_user.id
        user_name = current_user.first_name
       
        while True:     
            conn = psycopg2.connect(database=cfg.database, user=cfg.postgres_user, password=cfg.postgres_password, host=cfg.host, port=cfg.port)
            if conn != None:
                cur = conn.cursor()
                #sprawdzenie czy id zgadza sie z id pomiaru, abyy stworzyć warunek, że gdy nie ma w bazie danych pomiarów do takiego id, to przekieruje do strony z informacja ze nie ma danych dla tego uyzytkownika
                id = "SELECT json_info -> 'patient_id' as keyvalues FROM measurements where cast(json_info ->> 'patient_id' as INTEGER) = ( \'"+str(user_id)+"\') " 
                cur.execute(id)
                row = cur.fetchone()
                if row is None:
                     return render_template('nographs.html', user_first_name=user_name, user=current_user)
                else:     
                    patient_id_nr = [] 
                    for(nr) in cur:
                        patient_id_nr.append(nr)
                        patient_id_numbers =  "".join(nr)
                    patient_id_number = patient_id_numbers
                    print("patient_id_number", patient_id_number)
                    if str(user_id) == str(patient_id_number):
                        #pobranie danych odnośnie pomiarów z bazy danych
                        otrzymane = "SELECT json_info -> 'HR' as keyvalues FROM measurements  where cast(json_info ->> 'patient_id' as INTEGER) = ( \'"+str(user_id)+"\') order by measurements_id desc limit 20" 
                        cur.execute(otrzymane)
                        conn.commit()
                        #obliczanie wartości szczytowych i średniej
                        value = [] 
                        min = None
                        max = None
                        mean = None
                        sum = 0
                        numbers = 0
                        for(HR) in cur:
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
                        #pobieranie z bazy z jakiego urządzenia był przesyłany pomiar
                        devicefromtable = "SELECT json_info -> 'context' as keyvalues FROM measurements where cast(json_info ->> 'patient_id' as INTEGER) = ( \'"+str(user_id)+"\') order by measurements_id desc limit 20" 
                        cur.execute(devicefromtable)
                        devices = [] 
                        for(context) in cur:
                            # devices.append(context)
                            devices.insert(0,context)
                            measurement_devices =  "".join(context)
                        measurement_device = measurement_devices
                        print('measurement device: ', measurement_device)
            
                        #pobranie daty z bazy danych
                        query = "SELECT json_info -> 'measurement_time' as keyvalues FROM measurements where cast(json_info ->> 'patient_id' as INTEGER) = ( \'"+str(user_id)+"\') order by measurements_id desc limit 20" 
                        cur.execute(query)
                        conn.commit()
                        x = [] 
                        for(measurement_time) in cur:
                            x.insert(0,measurement_time) # aby czas był dobrze sortowany
                        data =[]
                        data2 =[]
                        data4 = []
                        for i in value: 
                                to_convert = re.findall(r'\d\d+', str(i)) 
                                converted = str(to_convert[0])     
                                data.append(converted)
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
                                data4.append(measure_day)
                        labels = data2
                        values = data       
                        cur.close()
                        conn.close()                
                        return render_template("graph.html", measurement_device=measurement_device, labels = labels, values = values,  user=current_user, measure_day=measure_day, min_hr=min_hr, max_hr=max_hr, mean=mean)
                    else:
                        return render_template('nographs.html', user_first_name=user_name, user=current_user)
                

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()


@views.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    user_id=current_user.id
    user_name = current_user.first_name
    if user_id == 24: 
        while True:     
            conn = psycopg2.connect(database=cfg.database, user=cfg.postgres_user, password=cfg.postgres_password, host=cfg.host, port=cfg.port)
            if conn != None:
                cur = conn.cursor()
                patient_id = 'SELECT identyfikator FROM patient'
                cur.execute(patient_id)
                patients_id = [] 
                for(patient_id) in cur:    
                    #convert = re.findall(r'\d\d+', str(patient_id)) 
                    #converted = str(convert[])
                    patients_id.append(patient_id)   
                    
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