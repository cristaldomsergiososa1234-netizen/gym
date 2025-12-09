import sqlite3

DB_NAME = "gym.db"

# ===========================
# 🔌 Conexión
# ===========================
def conectar_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# ===========================
# 0️⃣ Rol de usuario
# ===========================
def agregar_rol(nombre_rol, descripcion=None):
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO rol_usuario (Nombre_Rol, Descripcion)
            VALUES (?, ?)
        """, (nombre_rol, descripcion))
        conn.commit()
        print(f"✅ Rol '{nombre_rol}' agregado correctamente.")
    except sqlite3.Error as e:
        print("❌ Error al agregar rol:", e)
    finally:
        cursor.close()
        conn.close()

# ===========================
# 1️⃣ Usuario
# ===========================
def agregar_usuario(nombre, apellido, email, contraseña, telefono=None, fecha_nac=None, id_rol=2):
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO usuario (Nombre, Apellido, Email, Contraseña, Telefono, Fecha_Nacimiento, id_Rol)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nombre, apellido, email, contraseña, telefono, fecha_nac, id_rol))
        conn.commit()
        print(f"✅ Usuario '{nombre} {apellido}' agregado correctamente.")
    except sqlite3.Error as e:
        print("❌ Error al agregar usuario:", e)
    finally:
        cursor.close()
        conn.close()

# ===========================
# 2️⃣ Categoría
# ===========================
def agregar_categoria(nombre, descripcion=None):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO categoria (Nombre, Descripcion)
        VALUES (?, ?)
    """, (nombre, descripcion))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Categoría '{nombre}' agregada correctamente.")

# ===========================
# 3️⃣ Artículo
# ===========================
def agregar_articulo(nombre, descripcion, precio, stock, id_categoria):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO articulo (Nombre, Descripcion, Precio, Stock, id_Categoria)
        VALUES (?, ?, ?, ?, ?)
    """, (nombre, descripcion, precio, stock, id_categoria))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Artículo '{nombre}' agregado correctamente.")

# ===========================
# 4️⃣ Servicio
# ===========================
def agregar_servicio(nombre, descripcion, precio):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO servicio (Nombre, Descripcion, Precio)
        VALUES (?, ?, ?)
    """, (nombre, descripcion, precio))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Servicio '{nombre}' agregado correctamente.")

# ===========================
# 5️⃣ Entrenamiento
# ===========================
def agregar_entrenamiento(nombre, descripcion, duracion):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO entrenamientos (Nombre, Descripcion, Duracion_Estimada)
        VALUES (?, ?, ?)
    """, (nombre, descripcion, duracion))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Entrenamiento '{nombre}' agregado correctamente.")

# ===========================
# 6️⃣ Nutrición
# ===========================
def agregar_nutricion(nombre, descripcion, tipo):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO nutricion (Nombre, Descripcion, Tipo)
        VALUES (?, ?, ?)
    """, (nombre, descripcion, tipo))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Plan de nutrición '{nombre}' agregado correctamente.")

# ===========================
# 7️⃣ Membresía
# ===========================
def agregar_membresia(nombre, precio, duracion):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO membresia (Nombre, Precio, Duracion)
        VALUES (?, ?, ?)
    """, (nombre, precio, duracion))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Membresía '{nombre}' agregada correctamente.")

# ===========================
# 8️⃣ Ubicación
# ===========================
def agregar_ubicacion(direccion, ciudad, pais):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ubicacion (Direccion, Ciudad, Pais)
        VALUES (?, ?, ?)
    """, (direccion, ciudad, pais))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Ubicación '{direccion}, {ciudad}' agregada correctamente.")

# ===========================
# 9️⃣ Sugerencia
# ===========================
def agregar_sugerencia(id_usuario, mensaje):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sugerencias (id_Usuario, Mensaje)
        VALUES (?, ?)
    """, (id_usuario, mensaje))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Sugerencia agregada por usuario ID {id_usuario}.")

# ===========================
# 🔟 Carga de horas de entrenamiento
# ===========================
def agregar_carga_horas(id_usuario, id_entrenamiento, fecha, horas):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO carga_horas_entrenamiento (id_Usuario, id_Entrenamiento, Fecha, Horas_Entrenadas)
        VALUES (?, ?, ?, ?)
    """, (id_usuario, id_entrenamiento, fecha, horas))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Carga de {horas} horas registrada para usuario {id_usuario}.")

# ===========================
# 1️⃣1️⃣ Historial de pago
# ===========================
def agregar_pago(id_usuario, id_membresia, monto, metodo_pago, estado):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO historial_pago (id_Usuario, id_Membresia, Monto, Metodo_Pago, Estado)
        VALUES (?, ?, ?, ?, ?)
    """, (id_usuario, id_membresia, monto, metodo_pago, estado))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Pago de {monto} registrado correctamente para usuario {id_usuario}.")

# ===========================
# 🧩 Datos iniciales
# ===========================
if __name__ == "__main__":
    # Roles
    agregar_rol("admin", "Administrador con todos los permisos")
    agregar_rol("usuario", "Usuario con permisos limitados")

    # Categorías
    agregar_categoria("Suplementos", "Proteínas, creatinas, vitaminas")
    agregar_categoria("Equipos", "Pesas, bandas, colchonetas")

    # Usuarios
    agregar_usuario("Admin", "Principal", "admin@manuelgym.com.py", "admin123", "0983871346", "1990-05-10", 1)
    agregar_usuario("Carlos", "Perez", "carlos.perez@gmail.com", "12345", "0971234567", "1990-05-10", 2)

    # Membresías
    agregar_membresia("Mensual", 150000, 30)
    agregar_membresia("Trimestral", 400000, 90)

    # Servicios
    agregar_servicio("Entrenamiento Personal", "Asistencia individual con entrenador", 200000)
    agregar_servicio("Masaje Deportivo", "Masajes post-entrenamiento", 100000)

    # Entrenamientos
    agregar_entrenamiento("Full Body", "Entrenamiento general de fuerza", 60)
    agregar_entrenamiento("Cardio Intenso", "Entrenamiento de resistencia", 45)

    # Nutrición
    agregar_nutricion("Plan Proteico", "Alta en proteínas", "Plan")
    agregar_nutricion("Suplemento Energético", "Ideal para antes del entrenamiento", "Suplemento")

    # Ubicación
    agregar_ubicacion("Av. Central 123", "Caacupé", "Paraguay")

    # Carga de horas
    agregar_carga_horas(2, 1, "2025-11-04", 2)

    # Pagos
    agregar_pago(2, 1, 150000, "Efectivo", "Completado")

    # Sugerencias
    agregar_sugerencia(2, "Podrían agregar más máquinas para piernas.")
