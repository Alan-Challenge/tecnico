# tecnico
Challenge técnico - MercadoLibre - Alan
El archivo ml.py al ser ejecutado lleva al usuario a una interfaz de logueo de Gmail
Luego de efectivo el logueo, la aplicación verifica cuáles mails tiene la palabra "DevOps" en el body
Luego, de aquellos que cumplan esa condición se alamcenará en una base de datos hosteada externamente el subject, la fecha de emisión del correo y la dirección de quien lo envió
Los archivos prueba1.py y prueba2.py son aplicaciones de teste
Prueba1.py sólo verifica que se conecte la aplicación correctamente con la API de Gmail necesaria para obtener la información. La fracción el codigo que se conecta con la base de datos está asilada del resto.
Prueba2.py sólo verifica la conexión con la base de datos a partir de un archivo prueba.json de testeo. La facción del código que se usa los servicios de la API de Gmail está aislada del resto.
