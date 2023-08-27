import mysql.connector


def connect_database():
    try:
        bank = mysql.connector.connect(
            host="localhost", user="root", passwd="senha12345", database="lojadoze"
        )
        return bank
    except mysql.connector.errors as err:
        print("Erro ao se conectar com o banco de dados: ", err)
        return None


def close_database(bank):
    if bank:
        bank.close()
