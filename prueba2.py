from __future__ import print_function
import json
import pymysql

# Si se modifica SCOPES debe borrar el archvio token.pickle de la carpeta principal
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
	
		with open('prueba.json') as file:
			mensajesJson2 = json.load(file)
		if mensajesJson2:
			ServerName = "sql10.freemysqlhosting.net"
			Username = "sql10300498"
			Password = "bsAH7hylXa"
			DBName = "sql10300498"
			#Se conceta con la base de datos enviando las credenciales necesarias: Nombre del server, username, password, nombre de la base de datos
			db = pymysql.connect(ServerName,Username,Password,DBName)
			cursor = db.cursor()
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

if __name__ == '__main__':
    main()

