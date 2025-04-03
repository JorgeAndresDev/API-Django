import mysql.connector

def conexiondbw():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            passwd="1234",
            database="app_empresa_bd_wilson",
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
            raise_on_warnings=True
        )
        print("Conexión exitosa a la base de datos")
        return connection
    except mysql.connector.Error as error:
        print(f"No se pudo conectar a la BD: {error}")
        return None
