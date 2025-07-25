import os
import pymysql

def get_connection():
    return pymysql.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', ''),
        database=os.getenv('MYSQL_DB', 'pedidos_db'),
        cursorclass=pymysql.cursors.DictCursor
    )

def crear_tabla_si_no_existe():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pedidos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT NOT NULL,
                estado VARCHAR(50) NOT NULL,
                detalles TEXT,
                total DECIMAL(10,2),
                creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    conn.commit()
    conn.close()

def crear_pedido(usuario_id, estado, detalles, total):
    crear_tabla_si_no_existe()
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO pedidos (usuario_id, estado, detalles, total) 
            VALUES (%s, %s, %s, %s)
        """, (usuario_id, estado, detalles, total))
        pedido_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return pedido_id

def obtener_pedidos():
    crear_tabla_si_no_existe()
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM pedidos ORDER BY creado_en DESC")
        results = cursor.fetchall()
    conn.close()
    return results
