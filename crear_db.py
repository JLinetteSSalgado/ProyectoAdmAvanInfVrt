import pymysql

# 1. Pega aquí el Endpoint cuando AWS termine (ej: tienda.cw5...us-east-1.rds.amazonaws.com)
AWS_DB_ENDPOINT = "tienda-db.cbgmg8ssyk5d.us-east-2.rds.amazonaws.com" 

# 2. Tu usuario y contraseña
AWS_DB_USER = "admin"
AWS_DB_PASS = "Tienda2025AWS"

try:
    # Conectamos al servidor SIN especificar base de datos
    connection = pymysql.connect(
        host=AWS_DB_ENDPOINT,
        user=AWS_DB_USER,
        password=AWS_DB_PASS
    )
    
    cursor = connection.cursor()
    
    # Creamos la base de datos manualmente
    cursor.execute("CREATE DATABASE IF NOT EXISTS tienda_online;")
    print("✅ ¡LISTO! Base de datos 'tienda_online' creada correctamente.")
    
    cursor.close()
    connection.close()

except Exception as e:
    print("❌ Error:", e)