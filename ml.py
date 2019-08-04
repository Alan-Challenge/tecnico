from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pymysql

# Si se modifica SCOPES debe borrar el archvio token.pickle de la carpeta principal
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    creds = None
    Word= "DevOps"
    #  token.pickle guarda el acceso del usuario y actualiza los tokens,
    # es creado automáticamente cuando el flujo de autorización se completa por primera vez.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # Si no hay credenciales válidas disponibles, el usuario deberá loguearse
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Guarda las crecenciales para la siguiente tanda
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Llamado a la API de Gmail
    mensajesJson = service.users().messages().list(userId='me', q=Word).execute()

    if mensajesJson:
        ServerName = "sql10.freemysqlhosting.net"
        Username = "sql10300498"
        Password = "bsAH7hylXa"
        DBName = "sql10300498"
		#Se conceta con la base de datos enviando las credenciales necesarias: Nombre del server, username, password, nombre de la base de datos
        db = pymysql.connect(ServerName,Username,Password,DBName)
        cursor = db.cursor()
		#Obtiene un Json con los mensajes con los mensajes que contienen el word (DevOps en este caso) y sus respectivos IDs
        mensajes = mensajesJson['messages']
        for mensaje in mensajes:
			#Por cada uno de esos mensajes debe solicitar, con el ID correspondiente, información sobre ese mensaje
            mensajesJson2 = service.users().messages().get(userId='me', id=mensaje['id']).execute()
            if mensajesJson2:
				#Guardo los datos de interés en base a su ubicación en la estructura Json que se devuelve
                key=str (mensajesJson2['id'])			
                fecha= str(mensajesJson2['payload']['headers'][1]['value']) #Dentro del subconjunto 'headers' la fecha se encuentra en la posición 1
                subject=str (mensajesJson2['payload']['headers'][3]['value']) #Dentro del subconjunto 'headers' el subject se encuentra en la posición 3
                de= str(mensajesJson2['payload']['headers'][4]['value']) #Dentro del subconjunto 'headers' el emisor se encuentra en la posición 4
				#Se usa 'INSERT IGNORE' para ignorar aquellas solicitudes que generen un error (como insertar registros con una PK ya exitente)
				#Esto es especialemente útil si se va a necesitar  hacer grandes cantidades de INSERTs
                sql = "INSERT IGNORE INTO mails_DevOps(id, DE, SUBJECT, FECHA) VALUES ('" + key+ "','"+de+"','"+subject+"','"+fecha+"')"
                try:
                    cursor.execute(sql)
                    db.commit()
                except:
                    db.rollback()
                    print ("Hubo un error con el registro:" + str (key))
        print ('La base de datos ha sido actualizada')
    else:
        print('No se encontraron mensajes.')      

if __name__ == '__main__':
    main()