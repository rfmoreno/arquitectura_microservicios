import os
import pymysql

def get_connection():
    return pymysql.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', ''),
        database=os.getenv('MYSQL_DB', 'productos_db'),
        cursorclass=pymysql.cursors.DictCursor
    )

def crear_tabla_si_no_existe():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                precio DECIMAL(10,2) NOT NULL,
                stock INT NOT NULL
            )
        """)
    conn.commit()
    conn.close()

def obtener_productos():
    crear_tabla_si_no_existe()
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, nombre, precio, stock FROM productos")
        results = cursor.fetchall()
    conn.close()
    return results

def crear_producto(nombre, precio, stock):
    crear_tabla_si_no_existe()
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)", (nombre, precio, stock))
    conn.commit()
    conn.close()

def eliminar_producto(producto_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
            conn.commit()
            return cursor.rowcount > 0
    finally:
        conn.close()
