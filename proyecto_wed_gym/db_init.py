import sqlite3

DB_NAME = "gym.db"

def crear_tablas_y_datos():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    # ======================================================
    # 1. rol_usuario
    # ======================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rol_usuario (
            id_Rol INTEGER PRIMARY KEY,
            Nombre_Rol TEXT NOT NULL,
            Descripcion TEXT
        )
    """)

    # ======================================================
    # 2. usuario
    # ======================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuario (
            id_Usuario INTEGER PRIMARY KEY,
            Nombre TEXT NOT NULL,
            Apellido TEXT NOT NULL,
            Email TEXT NOT NULL UNIQUE,
            Contraseña TEXT NOT NULL,
            Telefono TEXT,
            Fecha_Nacimiento DATE,
            id_Rol INTEGER,
            FOREIGN KEY (id_Rol) REFERENCES rol_usuario(id_Rol)
        )
    """)

    # ======================================================
    # 3. categoria
    # ======================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categoria (
            id_Categoria INTEGER PRIMARY KEY,
            Nombre TEXT NOT NULL,
            Descripcion TEXT
        )
    """)

    # ======================================================
    # 4. articulo
    # ======================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articulo (
            id_Articulo INTEGER PRIMARY KEY,
            Nombre TEXT NOT NULL,
            Descripcion TEXT,
            Precio REAL NOT NULL,
            Stock INTEGER DEFAULT 0,
            id_Categoria INTEGER
        )
    """)

    # ======================================================
    # 5. servicio
    # ======================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servicio (
            id_Servicio INTEGER PRIMARY KEY,
            Nombre TEXT NOT NULL,
            Descripcion TEXT,
            Precio REAL NOT NULL
        )
    """)

    # ======================================================
    # 6. entrenamientos
    # ======================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entrenamientos (
            id_Entrenamiento INTEGER PRIMARY KEY,
            Nombre TEXT NOT NULL,
            Descripcion TEXT,
            Duracion_Estimada INTEGER
        )
    """)

    # ======================================================
    # 7. nutricion
    # ======================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nutricion (
            id_Nutricion INTEGER PRIMARY KEY,
            Nombre TEXT NOT NULL,
            Descripcion TEXT,
            Tipo TEXT NOT NULL CHECK(Tipo IN ('Plan','Suplemento','Receta'))
        )
    """)

    # ======================================================
    # 8. membresia
    # ======================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS membresia (
            id_Membresia INTEGER PRIMARY KEY,
            Nombre TEXT NOT NULL,
            Precio REAL NOT NULL,
            Duracion INTEGER NOT NULL
        )
    """)

    # ======================================================
    # 9. ubicacion
    # ======================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ubicacion (
            id_Ubicacion INTEGER PRIMARY KEY,
            Direccion TEXT,
            Ciudad TEXT,
            Pais TEXT
        )
    """)

    # ======================================================
    # 10. sugerencias
    # ======================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sugerencias (
            id_Sugerencia INTEGER PRIMARY KEY,
            id_Usuario INTEGER,
            Correo TEXT NOT NULL,
            Asunto TEXT NOT NULL,
            Mensaje TEXT NOT NULL,
            Fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_Usuario) REFERENCES usuario(id_Usuario)
        )
    """)

    # ======================================================
    # 11. carga horas
    # ======================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS carga_horas_entrenamiento (
            id_Carga INTEGER PRIMARY KEY,
            id_Usuario INTEGER NOT NULL,
            Fecha DATE NOT NULL,
            Hora_Entrada TIME,
            Hora_Salida TIME,
            Horas_Entrenadas REAL,
            FOREIGN KEY (id_Usuario) REFERENCES usuario(id_Usuario)
        )
    """)


    # ======================================================
    # 12. historial pagos
    # ======================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historial_pago (
            id_Pago INTEGER PRIMARY KEY,
            id_Usuario INTEGER,
            id_Membresia INTEGER,
            Monto REAL NOT NULL,
            Metodo_Pago TEXT NOT NULL CHECK(Metodo_Pago IN ('Efectivo','Transferencia','Tarjeta de Crédito','Cheque')),
            Fecha_Pago DATETIME DEFAULT CURRENT_TIMESTAMP,
            Estado TEXT NOT NULL CHECK(Estado IN ('Pendiente','Completado','Cancelado')),
            FOREIGN KEY (id_Usuario) REFERENCES usuario(id_Usuario),
            FOREIGN KEY (id_Membresia) REFERENCES membresia(id_Membresia)
        )
    """)
    # ======================================================
    # 13. pedidos
    # ======================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedido (
            id_Pedido INTEGER PRIMARY KEY,
            id_Usuario INTEGER,
            Estado TEXT NOT NULL CHECK(Estado IN ('Pendiente','En Proceso','Completado','Cancelado')),
            Fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_Usuario) REFERENCES usuario(id_Usuario)
        )
    """)

    # ======================================================
    # 14. detalle pedido
    # ======================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalle_pedido (
            id_Detalle INTEGER PRIMARY KEY,
            id_Pedido INTEGER,
            id_Articulo INTEGER,
            Cantidad INTEGER NOT NULL,
            FOREIGN KEY (id_Pedido) REFERENCES pedido(id_Pedido),
            FOREIGN KEY (id_Articulo) REFERENCES articulo(id_Articulo)
        )
    """)

    # ======================================================
    # INSERTS
    # ======================================================

    # -------- Rol usuario --------
    cursor.executescript("""
        INSERT INTO rol_usuario VALUES
        (1, 'admin', 'Control total del sistema'),
        (2, 'usuario', 'Usuario del gimnasio');
    """)

    # -------- Usuarios --------
    cursor.executescript("""
        INSERT INTO usuario VALUES
        (1, 'Admin', 'Principal', 'admin@gym.com', 'admin123', '0991122334', '1990-07-08', 1),
        (2, 'Sergio', 'Sosa', 'sergio@gym.com', '1234', '0981000001', '2003-05-11', 2),
        (3, 'Aram', 'López', 'aram@gym.com', '1234', '0981444002', '2004-03-21', 2),
        (4, 'Valentina', 'Gómez', 'valentina@gym.com', '1234', '0975223344', '1999-10-14', 2),
        (5, 'Rodrigo', 'Rojas', 'rodrigo@gym.com', '1234', '0983777123', '1998-09-26', 2);
    """)

    # -------- Categorías --------
    cursor.executescript("""
        INSERT INTO categoria VALUES
        (1, 'Suplementos', 'Productos de nutrición'),
        (2, 'Ropa Deportiva', 'Indumentaria fitness'),
        (3, 'Accesorios', 'Accesorios para entrenamiento');
    """)

    # -------- Artículos --------
    cursor.executescript("""
        INSERT INTO articulo VALUES
        (1, 'Whey Protein', 'Suplemento de proteínas', 180000, 25, 1),
        (2, 'Creatina 300g', 'Monohidrato pura', 120000, 18, 1),
        (3, 'Camiseta Dry-Fit', 'Tela respirable', 65000, 40, 2),
        (4, 'Guantes de gimnasio', 'Cuero reforzado', 85000, 15, 3);
    """)

    # -------- Servicios --------
    cursor.executescript("""
        INSERT INTO servicio VALUES
        (1, 'Entrenamiento Personal', 'Sesión personalizada de 1 hora', 100000),
        (2, 'Fisioterapia', 'Sesión de recuperación física', 150000),
        (3, 'Evaluación Física', 'Control físico general', 70000);
    """)

    # -------- Entrenamientos --------
    cursor.executescript("""
        INSERT INTO entrenamientos VALUES
        (1, 'Full Body', 'Rutina completa del cuerpo', 60),
        (2, 'Piernas', 'Ejercicios para tren inferior', 45),
        (3, 'Cardio HIT', 'Entrenamiento de alta intensidad', 30);
    """)

    # -------- Nutricion --------
    cursor.executescript("""
        INSERT INTO nutricion VALUES
        (1, 'Plan Definición', 'Bajo en calorías', 'Plan'),
        (2, 'Creatina Monoh', 'Suplemento para fuerza', 'Suplemento'),
        (3, 'Avena Proteica', 'Receta para desayuno alto en proteína', 'Receta');
    """)

    # -------- Membresías --------
    cursor.executescript("""
        INSERT INTO membresia VALUES
        (1, 'Mensual', 160000, 30),
        (2, 'Trimestral', 420000, 90),
        (3, 'Semestral', 750000, 180),
        (4, 'Anual', 1500000, 365);
    """)

    # -------- Ubicación --------
    cursor.executescript("""
        INSERT INTO ubicacion VALUES
        (1, 'Calle 14 e/ España', 'Caacupé', 'Paraguay'),
        (2, 'Av. Brasil 550', 'Asunción', 'Paraguay'),
        (3, 'Ruta 2 Km 45', 'Itauguá', 'Paraguay');
    """)

    # -------- Sugerencias --------
    cursor.executescript("""
        INSERT INTO sugerencias (id_Sugerencia, id_Usuario, Correo, Asunto, Mensaje, Fecha) VALUES
        (1, 2, 'sergio@gmail.com', 'Mejoras en máquinas', 'Agregar más máquinas de pierna', CURRENT_TIMESTAMP),
        (2, 3, 'valentina@gmail.com', 'Horarios del gym', 'Horarios más amplios los sábados', CURRENT_TIMESTAMP);
    """)

    # -------- Carga horas --------
    cursor.executemany("""
        INSERT INTO carga_horas_entrenamiento 
        (id_Usuario, Fecha, Hora_Entrada, Hora_Salida, Horas_Entrenadas) 
        VALUES (?, ?, ?, ?, ?)
    """, [
        (2, '2025-12-01', '08:00', '10:00', 2.0),
        (3, '2025-12-01', '09:30', '10:15', 0.75),
        (2, '2025-12-02', '07:45', '09:15', 1.5),
        (4, '2025-12-02', '18:00', '19:30', 1.5),
        (3, '2025-12-03', '17:15', '18:00', 0.75)
    ])


    # -------- Historial pago --------
    cursor.executemany("""
        INSERT INTO historial_pago
        (id_Usuario, id_Membresia, Monto, Metodo_Pago, Estado)
        VALUES (?, ?, ?, ?, ?)
    """, [
        (2, 1, 160000, 'Efectivo', 'Completado'),
        (3, 2, 420000, 'Transferencia', 'Pendiente'),
        (2, 3, 1500000, 'Tarjeta de Crédito', 'Completado')
    ])

    # -------- Pedidos --------
    cursor.executemany("""
        INSERT INTO pedido
        (id_Usuario, Estado, Fecha)
        VALUES (?, ?, ?)
    """, [
        (2, 'Pendiente', '2025-12-01 10:30:00'),
        (3, 'En Proceso', '2025-12-02 15:45:00'),
        (2, 'Completado', '2025-12-03 09:20:00')
    ])

    # -------- Detalle pedidos --------
    cursor.executemany("""
        INSERT INTO detalle_pedido
        (id_Pedido, id_Articulo, Cantidad)
        VALUES (?, ?, ?)
    """, [
        (1, 1, 2),  # Pedido 1: 2 Whey Protein
        (1, 3, 1),  # Pedido 1: 1 Camiseta Dry-Fit
        (2, 2, 3),  # Pedido 2: 3 Creatina 300g
        (2, 4, 1),  # Pedido 2: 1 Guantes de gimnasio
        (3, 1, 1),  # Pedido 3: 1 Whey Protein
        (3, 2, 2)   # Pedido 3: 2 Creatina 300g
    ])

    conn.commit()
    conn.close()
    print("Base de datos creada con datos insertados correctamente.")

if __name__ == "__main__":
    crear_tablas_y_datos()
