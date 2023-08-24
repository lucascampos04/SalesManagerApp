import mysql.connector

banco = mysql.connector.connect(
    host="localhost", user="root", passwd="senha12345", database="lojadoze"
)


cursor = banco.cursor()

banco.commit()
cursor.close()
banco.close()
