from fastapi.responses import JSONResponse
from conexion.conexionBD import conexiondb
from apps.usersSQL.schemas import UserCreateSchema, UserUpdateSchema

def get_all_users_service():     
    try:         
        connection = conexiondb()         
        if connection:             
            with connection.cursor(dictionary=True) as cursor:                 
                querySQL = """                     
                    SELECT
                        id,                    
                        name,                         
                        email,                         
                        password,                         
                        created_user                                            
                    FROM users                     
                    ORDER BY id ASC                 
                """                 
                cursor.execute(querySQL)                 
                empleadosBD = cursor.fetchall()                 
                return empleadosBD         
        else:             
            return None     
    except Exception as e:         
        print(f"Error en la función sql_lista_empleadosBD: {e}")         
        return None     
    finally:         
        if connection:             
            connection.close()
    
def create_user_service(user_data: UserCreateSchema):
    try:
        connection = conexiondb()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", 
               (user_data.name, user_data.email, user_data.password))
        connection.commit()
        cursor.close()
        connection.close()
        if 'connection' in locals():
            connection.close()
        return {'success':True, "message": "Usuario creado Correctamente"}
    except Exception as e:
        return {"error": str(e)}

    
def update_user_service(user: UserUpdateSchema):
    try:
        connection = conexiondb()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET name = %s, email = %s, password = %s WHERE id = %s",
                    (user.name, user.email, user.password, user.id)
                )
                connection.commit()
            return {"message": "Usuario actualizado Correctamente"}
        else:
            return {"error": "No se pudo establecer conexión con la base de datos"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'connection' in locals() and connection:
            connection.close()

def delete_user_service(userId: int):
    try:
        connection = conexiondb()   
        if connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE id = %s", (userId,))
                connection.commit()
            return {'success':True, "message": "Usuario eliminado Correctamente"}
        else:
            return {"error": "No se pudo establecer conexión con la base de datos"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'connection' in locals() and connection:
            connection.close()