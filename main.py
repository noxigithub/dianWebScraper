import os
from flask import Blueprint, flash, redirect, render_template, request, send_file, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from playwright.sync_api import sync_playwright
import pandas as pd
from app import db, UPLOAD_FOLDER
import time
#import numpy as np


ALLOWED_EXTENSIONS = {'xlsx'}
cedulas = []
main = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/aboutus')
def aboutus():
    return render_template('about-us.html')


@main.route('/apps')
def apps():
    return render_template('apps.html')


@main.route('/contact')
def contact():
    return render_template('contact.html')



@main.route("/uploadFile", methods=["GET"])
@login_required
def uploadFileForm():
    return render_template("uploadFile.html")

@main.route("/downloadFile")
@login_required
def downloadFile():
    path= os.path.join(UPLOAD_FOLDER,"Updated_file.xlsx" )
    return send_file(path, as_attachment=True)

"""
@main.route("/prueba")
@login_required
def prueba():
    df1 = pd.read_excel(os.path.join(UPLOAD_FOLDER,"Updated_file.xlsx" ))
    df2 = pd.read_excel(os.path.join(UPLOAD_FOLDER,"prueba.xlsx" ))

    df1.equals(df2)

    comparison_values = df1.values == df2.values

    print(comparison_values)

    rows, cols = np.where(comparison_values == False)
    for item in zip(rows,cols):
        df1.iloc[item[0], item[1]] = '{} --> {}'.format(df1.iloc[item[0], item[1]], df2.iloc[item[0], item[1]])

    df1.to_excel(os.path.join(UPLOAD_FOLDER,"differences.xlsx"), index = False, header = True)
    return render_template('index.html')


"""
@main.route("/uploadFile", methods=["POST"])
@login_required
def uploadFile():
     if request.method == "POST":
    # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
           # return redirect(url_for(UPLOAD_FOLDER, name=filename))
            dataset = pd.read_excel(os.path.join(UPLOAD_FOLDER, filename))
            cedulas = dataset["cedulas"]
            print(cedulas.values)
            #dataset.to_excel(filename)
            #dataset['Salary'] = dataset['Salary'] + dataset['Salary'] * (x/10
            filenameUpdated="Updated_file.xlsx"
            data= get_clients(cedulas.values)      
            clients_df= pd.DataFrame.from_dict(data)
            clients_df.to_excel(os.path.join(UPLOAD_FOLDER,filenameUpdated))
            return render_template("readData.html",tables=[clients_df.to_html(classes='data', table_id="table")], titles=clients_df.columns.values )
     #return render_template("readData.html", cedulas = clients_df)




def get_clients(clients):
     
    client_data={'NO DOCUMENTO' : [],
                'PRIMER NOMBRE': [], 
                'OTROS NOMBRES' : [], 
                'PRIMER APELLIDO' : [], 
                'SEGUNDO APELLIDO' : []
        }
    for id_client in clients:
        with sync_playwright() as p:
            
            browser= p.chromium.launch(headless=True, slow_mo=50)
            page= browser.new_page()
            url= 'https://muisca.dian.gov.co/WebRutMuisca/DefConsultaEstadoRUT.faces'
            page.goto(url)

            page.fill('input#vistaConsultaEstadoRUT\:formConsultaEstadoRUT\:numNit', str(id_client))
            page.locator('input#vistaConsultaEstadoRUT\:formConsultaEstadoRUT\:numNit').press('Enter')
            page.is_visible('#vistaConsultaEstadoRUT\:formConsultaEstadoRUT\:primerNombre')
            
            client_data['NO DOCUMENTO'].append(id_client)
            
            
            
            try:
                page.wait_for_selector('#vistaConsultaEstadoRUT\:formConsultaEstadoRUT\:primerNombre', timeout=50)
                name1= page.locator('#vistaConsultaEstadoRUT\:formConsultaEstadoRUT\:primerNombre').inner_text()
                name2= page.locator('#vistaConsultaEstadoRUT\:formConsultaEstadoRUT\:otrosNombres').inner_text()
                lastn1= page.locator('#vistaConsultaEstadoRUT\:formConsultaEstadoRUT\:primerApellido').inner_text()
                lastn2= page.locator('#vistaConsultaEstadoRUT\:formConsultaEstadoRUT\:segundoApellido').inner_text()
                
                client_data['PRIMER NOMBRE'].append(name1)
                client_data['OTROS NOMBRES'].append(name2)
                client_data['PRIMER APELLIDO'].append(lastn1)
                client_data['SEGUNDO APELLIDO'].append(lastn2)
                
            except:
                #page.wait_for_selector('#divMensaje')
                client_data['PRIMER NOMBRE'].append('NA')
                client_data['OTROS NOMBRES'].append('NA')
                client_data['PRIMER APELLIDO'].append('NA')
                client_data['SEGUNDO APELLIDO'].append('NA')
                print('Error en la transmición')
                
        time.sleep(0.2)
    return(client_data)