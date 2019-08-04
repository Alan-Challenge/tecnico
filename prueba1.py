from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

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
		#Obtiene un Json con los mensajes con los mensajes que contienen el word (DevOps en este caso) y sus respectivos IDs
        mensajes = mensajesJson['messages']
        for mensaje in mensajes:
			#Por cada uno de esos mensajes debe solicitar, con el ID correspondiente, información sobre ese mensaje
            mensajesJson2 = service.users().messages().get(userId='me', id=mensaje['id']).execute()
            if mensajesJson2:
				#Guardo los datos de interés en base a su ubicación en la estructura Json que se devuelve
                print (str (mensajesJson2['id']))			
                print (str(mensajesJson2['payload']['headers'][1]['value'])) #Dentro del subconjunto 'headers' la fecha se encuentra en la posición 1
                print (str(mensajesJson2['payload']['headers'][3]['value'])) #Dentro del subconjunto 'headers' el subject se encuentra en la posición 3
                print (str(mensajesJson2['payload']['headers'][4]['value'])) #Dentro del subconjunto 'headers' el emisor se encuentra en la posición 4
                print ('\n')
        print ('La base de datos ha sido actualizada')
    else:
        print('No se encontraron mensajes.')      

if __name__ == '__main__':
    main()