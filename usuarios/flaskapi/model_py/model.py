import os
import pymysql
import hashlib

def get_connection():
    return pymysql.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', ''),
        database=os.getenv('MYSQL_DB', 'usuarios_db'),
        cursorclass=pymysql.cursors.DictCursor
    )

def crear_tablas_y_perfiles():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
          CREATE TABLE IF NOT EXISTS perfiles (
            id_perfil INT PRIMARY KEY,
            perfil VARCHAR(50) NOT NULL
          );
        """)
        cursor.execute("""
          INSERT IGNORE INTO perfiles (id_perfil, perfil) VALUES
            (1, 'user'), (2, 'admin'), (3, 'client');
        """)
        cursor.execute("""
          CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre_completo VARCHAR(255) NOT NULL,
            login VARCHAR(255) NOT NULL UNIQUE,
            email VARCHAR(255) NOT NULL UNIQUE,
            hash_password VARCHAR(32) NOT NULL,
            id_perfil INT NOT NULL,
            FOREIGN KEY (id_perfil) REFERENCES perfiles(id_perfil)
          );
        """)
    conn.commit()
    conn.close()

def obtener_usuarios():
    crear_tablas_y_perfiles()
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
          SELECT usuarios.id, usuarios.nombre_completo, usuarios.login, usuarios.email, usuarios.id_perfil, perfiles.perfil
          FROM usuarios
          JOIN perfiles ON usuarios.id_perfil = perfiles.id_perfil
        """)
        results = cursor.fetchall()
    conn.close()
    return results

def obtener_usuario_por_id(usuario_id):
    crear_tablas_y_perfiles()
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT usuarios.id, usuarios.nombre_completo, usuarios.login, usuarios.email, usuarios.hash_password, usuarios.id_perfil, perfiles.perfil
            FROM usuarios
            JOIN perfiles ON usuarios.id_perfil = perfiles.id_perfil
            WHERE usuarios.id = %s
        """, (usuario_id,))
        usuario = cursor.fetchone()
    conn.close()
    return usuario


def crear_usuario(nombre_completo, login, email, password, id_perfil):
    crear_tablas_y_perfiles()
    hash_pwd = hashlib.md5(password.encode('utf-8')).hexdigest()
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO usuarios (nombre_completo, login, email, hash_password, id_perfil) 
            VALUES (%s, %s, %s, %s, %s)
            """,
            (nombre_completo, login, email, hash_pwd, id_perfil)
        )
    conn.commit()
    conn.close()

def modificar_usuario(usuario_id, nombre_completo, login, email, password, id_perfil):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            if password:
                hash_pwd = hashlib.md5(password.encode('utf-8')).hexdigest()
                cursor.execute("""
                    UPDATE usuarios 
                    SET nombre_completo=%s, login=%s, email=%s, hash_password=%s, id_perfil=%s
                    WHERE id=%s
                """, (nombre_completo, login, email, hash_pwd, id_perfil, usuario_id))
            else:
                cursor.execute("""
                    UPDATE usuarios 
                    SET nombre_completo=%s, login=%s, email=%s, id_perfil=%s
                    WHERE id=%s
                """, (nombre_completo, login, email, id_perfil, usuario_id))
        conn.commit()
    finally:
        conn.close()

def eliminar_usuario(usuario_id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
        conn.commit()
        return cursor.rowcount > 0
    conn.close()

def obtener_perfiles():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id_perfil, perfil FROM perfiles")
        results = cursor.fetchall()
    conn.close()
    return results
