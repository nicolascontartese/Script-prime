from sqlite3 import Time
import requests
import urllib3
import smtplib
from email.message import EmailMessage
import json
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
urllib3.disable_warnings()

def request():
    resultado5 =[]
    #jobname = ['Job_Compliance Audit Job_8_36_24_572_PM_8_24_2022','Job_Compliance Audit Job_8_36_24_572_PM_8_24_2022']
    jobname = ['Job_Compliance Audit Job_2_33_24_832_AM_8_25_2022']
    base_uri = 'https://10.3.4.202/webacs/api/v4/' #Direccion ip del servidor que apuntas a las APIS
    user = 'apiroot'                               # Usuario con credencials de NBI Read
    password = 'Bvs3965!'                          
    rest_path = 'op/compliance/check.json'         #Api a la que necesito hacer el request

# Hcaemos el request de la información a la api solicitada 
# El jobName es el nombre del audit job del que deseamos traer la información
    url = base_uri + rest_path
    for i in jobname:
        try:
            res = requests.get(url,{'jobName':i},auth=(user, password),verify=False)
          
        # print("#########")      
        # print(res)
        # print(type(res))
            if (res.status_code == 200):
                #validar_conect = 1
                #print("okay")
                res = res.text
#La api nos devuelve la informacion a la varibale res la cual convertimos de json a python
                resultado = json.loads(res)
                resultado2 = resultado['mgmtResponse']
                resultado3 = resultado2['complianceCheckResult']
                for variable in resultado3:
                    pass
                resultado4= dict(variable['devices'])
        
                resultado5.append(resultado4['devices'])
                for variable3 in resultado5:
                    pass
        
                return variable3
        except requests.exceptions.RequestException as e:        
            # La conexion fallo y avisamos del error
            validar_conect = 1
            return validar_conect
        
        


def generar_reporte(datos):
    cont = 0
    for variable2 in datos:   #Recorre los compos del diccionarios para imprimirlos como filas
        #Conseguimos la key reason para saber si cometion una violation o no
        key = variable2.get('reason')
        if key == "No violation":
            pass
        else:
        #Las que si son violation las contamos 
            cont = cont+1
            #print(variable2)
    return cont

def excel(variable4):
    
    with open('archivo.csv','w') as f:
        w = csv.DictWriter(f,variable4[0].keys())
        w.writeheader()
        
        for k in variable4:
            key = k.get('reason')
            if key != "No violation":
                w.writerow(k)
            else:                
                pass

def email_enviar(equipo_compliance):
    # Iniciamos los parámetros del script
    remitente = 'nicoserver6@gmail.com'
    destinatarios = ['nicolascontartese@gmail.com', 'nicolascontartese@gmail.com']
    asunto = 'Equipos fuera de compliance'
    cuerpo = f'Cantidad de equipos fuera de comliance:{equipo_compliance}'
    ruta_adjunto = 'archivo.csv'
    nombre_adjunto = 'archivo.csv'

    # Creamos el objeto mensaje
    mensaje = MIMEMultipart()
 
    # Establecemos los atributos del mensaje
    mensaje['From'] = remitente
    mensaje['To'] = ", ".join(destinatarios)
    mensaje['Subject'] = asunto
 
    # Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
    mensaje.attach(MIMEText(cuerpo, 'plain'))
 
    # Abrimos el archivo que vamos a adjuntar
    archivo_adjunto = open(ruta_adjunto, 'rb')
 
    # Creamos un objeto MIME base
    adjunto_MIME = MIMEBase('application', 'octet-stream')
    # Y le cargamos el archivo adjunto
    adjunto_MIME.set_payload((archivo_adjunto).read())
    # Codificamos el objeto en BASE64
    encoders.encode_base64(adjunto_MIME)
    # Agregamos una cabecera al objeto
    adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % nombre_adjunto)
    # Y finalmente lo agregamos al mensaje
    mensaje.attach(adjunto_MIME)
 
    # Creamos la conexión con el servidor
    sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)
 
    # Ciframos la conexión
    sesion_smtp.starttls()

    # Iniciamos sesión en el servidor
    sesion_smtp.login('nicoserver6@gmail.com','xqhqpouallekkqie')

    # Convertimos el objeto mensaje a texto
    texto = mensaje.as_string()

    # Enviamos el mensaje
    sesion_smtp.sendmail(remitente, destinatarios, texto)

    # Cerramos la conexión
    sesion_smtp.quit()

def email_fallo():
    # Iniciamos los parámetros del script
    remitente = 'nicoserver6@gmail.com'
    destinatarios = ['nicolascontartese@gmail.com', 'nicolascontartese@gmail.com']
    asunto = 'Equipos fuera de compliance'
    cuerpo = 'Fallo la conexión con el servidor y no fue posible obtener la información'

    # Creamos el objeto mensaje
    mensaje = MIMEMultipart()
 
    # Establecemos los atributos del mensaje
    mensaje['From'] = remitente
    mensaje['To'] = ", ".join(destinatarios)
    mensaje['Subject'] = asunto
 
    # Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
    mensaje.attach(MIMEText(cuerpo, 'plain'))
 
    # Creamos la conexión con el servidor
    sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)
 
    # Ciframos la conexión
    sesion_smtp.starttls()

    # Iniciamos sesión en el servidor
    sesion_smtp.login('nicoserver6@gmail.com','xqhqpouallekkqie')

    # Convertimos el objeto mensaje a texto
    texto = mensaje.as_string()

    # Enviamos el mensaje
    sesion_smtp.sendmail(remitente, destinatarios, texto)

    # Cerramos la conexión
    sesion_smtp.quit()


###############-MAIN-#####################
    
salida_datos = request()
if (salida_datos!= 1):
    excel(salida_datos)
    cont = generar_reporte(salida_datos)
    print("Cantidad de equipos fuera de compliance:",cont)
    email_enviar(cont)
else:
    ## Fallo la conexión
    email_fallo()
    print("error")


