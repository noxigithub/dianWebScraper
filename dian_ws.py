from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import time


def get_clients(clients):
    
    client_data={'NO DOCUMENTO' : [],
                'PRIMER NOMBRE': [], 
                'OTROS NOMBRES' : [], 
                'PRIMER APELLIDO' : [], 
                'SEGUNDO APELLIDO' : []
        }
    for id_client in clients:
        with sync_playwright() as p:
            
            browser= p.chromium.launch(headless=False, slow_mo=50)
            page= browser.new_page()
            url= 'https://muisca.dian.gov.co/WebRutMuisca/DefConsultaEstadoRUT.faces'
            page.goto(url)

            page.fill('input#vistaConsultaEstadoRUT\:formConsultaEstadoRUT\:numNit', str(id_client))
            page.locator('input#vistaConsultaEstadoRUT\:formConsultaEstadoRUT\:numNit').press('Enter')
            
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
                
        time.sleep(2)
    return(client_data)
    
    
if __name__ == "__main__":
    data= get_clients([1088318629, 12234985670294,  31413984, 12])
    clients_df= pd.DataFrame.from_dict(data)
    print(clients_df)
