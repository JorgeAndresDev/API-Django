from fastapi.responses import JSONResponse
from apps.user.schemas import UserCreateSchema, UserUpdateSchema
from conexion.conexionBD import conexiondb

def get_all_users():
    try:
        cursor = conexiondb.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return JSONResponse(users)
    except Exception as e:
        return JSONResponse({"error": str(e)}), 500
    
def create_users(user_data: dict):
    try:
        cursor = conexiondb.cursor()
        cursor.execute("INSERT INTO users (name_surname, email_user, pass_user) VALUES (%s, %s, %s)", 
               (user_data["name_surname"], user_data["email_user"], user_data["pass_user"]))

        conexiondb.commit()
        return JSONResponse({"message": "Usuario creado Correctamente"}), 201
    except Exception as e:
        return JSONResponse({"error": str(e)}), 500

    
def update_users(user: UserUpdateSchema):
    try:
        cursor = conexiondb.cursor()
        cursor.execute("UPDATE users SET name_surname = %s, email_user = %s, pass_user = %s WHERE id = %s", (user.name_surname, user.email_user, user.pass_user, user.id))
        conexiondb.commit()
        return JSONResponse({"message": "Usuario actualizado Correctamente"}), 200
    except Exception as e:
        return JSONResponse({"error": str(e)}), 500

def delete_users(user_id: str):
    try:
        cursor = conexiondb.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conexiondb.commit()
        return JSONResponse({"message": "Usuario eliminado Correctamente"}), 200
    except Exception as e:
        return JSONResponse({"error": str(e)}), 500