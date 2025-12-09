import flet as ft
import sqlite3
import main
import admin

DB_NAME = "gym.db"

# =========================
# Función para obtener usuario
# =========================
def obtener_usuario(login):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.id_Usuario, u.Nombre, u.Apellido, u.Email, u.Contraseña, r.Nombre_Rol, u.Telefono
            FROM usuario u
            LEFT JOIN rol_usuario r ON u.id_Rol = r.id_Rol
            WHERE u.Email = ? OR u.Nombre = ?
        """, (login, login))
        return cursor.fetchone()


# =========================
# Pantalla de login
# =========================
def login_page(page: ft.Page):
    page.title = "Login - Gym"
    page.bgcolor = "#121212"
    page.scroll = "adaptive"
    page.padding = 0
    page.clean()

    mensaje_error = ft.Text("", color=ft.Colors.RED)

    estilo_input = dict(
        width=300,
        text_style=ft.TextStyle(color=ft.Colors.WHITE),
        bgcolor="#1E1E1E",
        border_color=ft.Colors.GREY,
        focused_border_color=ft.Colors.YELLOW
    )

    usuario_input = ft.TextField(label="Usuario o Email", **estilo_input)
    contraseña_input = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, **estilo_input)

    def login_click(e):
        mensaje_error.value = ""
        page.update()

        login_val = usuario_input.value.strip()
        clave_val = contraseña_input.value.strip()
        user = obtener_usuario(login_val)

        if not user:
            mensaje_error.value = "Usuario no encontrado"
            page.update()
            return

        if clave_val != user[4]:
            mensaje_error.value = "Contraseña incorrecta"
            page.update()
            return

        usuario_dict = {
            "id_Usuario": user[0],
            "Nombre": user[1],
            "Apellido": user[2],
            "Email": user[3],
            "telefono": user[6] if user[6] else "No registrado",
            "horas_entrenamiento": "0h",
            "foto": "https://thumbs.dreamstime.com/b/silhouette-de-un-hombre-muscular-y-una-mujer-en-forma-emblema-gimnasio-silueta-musculoso-buena-con-pandillas-sembradas-prensa-400870742.jpg"
        }

        page.clean()
        if user[5] == "admin":
            admin.main(page, usuario_dict)
        else:
            main.main(page, usuario_dict)

    login_btn = ft.ElevatedButton("Iniciar sesión", width=300, bgcolor=ft.Colors.YELLOW_700, color=ft.Colors.BLACK, on_click=login_click)
    registrarse_btn = ft.ElevatedButton("Registrarse", width=300, bgcolor=ft.Colors.YELLOW_700, color=ft.Colors.BLACK, on_click=lambda e: mostrar_registro(page))

    cont_login = ft.Column(
        [
            ft.Text("💪 Gym", size=36, weight="bold", color=ft.Colors.YELLOW),
            ft.Text("Inicia sesión para continuar", size=18, color=ft.Colors.WHITE),
            usuario_input,
            contraseña_input,
            login_btn,
            registrarse_btn,
            mensaje_error
        ],
        alignment="center",
        horizontal_alignment="center",
        spacing=20
    )

    page.add(ft.Container(content=cont_login, alignment=ft.alignment.center, padding=ft.padding.only(top=120)))


# =========================
# Pantalla de registro (igual estilo que login)
# =========================
def mostrar_registro(page: ft.Page):
    page.clean()
    mensaje_error = ft.Text("", color=ft.Colors.RED)

    estilo_input = dict(
        width=300,
        text_style=ft.TextStyle(color=ft.Colors.WHITE),
        bgcolor="#1E1E1E",
        border_color=ft.Colors.GREY,
        focused_border_color=ft.Colors.YELLOW
    )

    nombre_input = ft.TextField(label="Nombre", **estilo_input)
    apellido_input = ft.TextField(label="Apellido", **estilo_input)
    email_input = ft.TextField(label="Email", **estilo_input)
    contraseña_input = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, **estilo_input)
    telefono_input = ft.TextField(label="Teléfono", **estilo_input)
    fecha_nac_input = ft.TextField(label="Fecha de Nacimiento (YYYY-MM-DD)", **estilo_input)

    def registrar_click(e):
        nombre = nombre_input.value.strip()
        apellido = apellido_input.value.strip()
        email = email_input.value.strip()
        contraseña = contraseña_input.value.strip()
        telefono = telefono_input.value.strip()
        fecha_nac = fecha_nac_input.value.strip()

        if not (nombre and apellido and email and contraseña):
            mensaje_error.value = "Completa todos los campos obligatorios"
            page.update()
            return

        try:
            with sqlite3.connect(DB_NAME) as conn:
                conn.execute("PRAGMA foreign_keys = ON;")
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO usuario (Nombre, Apellido, Email, Contraseña, Telefono, Fecha_Nacimiento, id_Rol)
                    VALUES (?, ?, ?, ?, ?, ?, 2)
                """, (nombre, apellido, email, contraseña, telefono, fecha_nac))
                conn.commit()

            # Loguear automáticamente
            user = obtener_usuario(email)
            if user:
                usuario_dict = {
                    "id_Usuario": user[0], 
                    "Nombre": user[1],
                    "Apellido": user[2],
                    "Email": user[3],
                    "telefono": user[6] if user[6] else "No registrado",
                    "horas_entrenamiento": "0h",
                    "foto": "https://upload.wikimedia.org/wikipedia/commons/3/3f/Placeholder_view_vector.svg"
                }
                page.clean()
                main.main(page, usuario_dict)

        except sqlite3.IntegrityError:
            mensaje_error.value = "El email ya está registrado"

        page.update()

    registrar_btn = ft.ElevatedButton("Registrarse", width=300, bgcolor=ft.Colors.GREEN, color=ft.Colors.BLACK, on_click=registrar_click)
    volver_btn = ft.ElevatedButton("Volver al login", width=300, bgcolor=ft.Colors.GREY, color=ft.Colors.BLACK, on_click=lambda e: login_page(page))

    cont_registro = ft.Column(
        [
            ft.Text("📋 Registro", size=36, weight="bold", color=ft.Colors.YELLOW),
            nombre_input,
            apellido_input,
            email_input,
            contraseña_input,
            telefono_input,
            fecha_nac_input,
            registrar_btn,
            volver_btn,
            mensaje_error
        ],
        alignment="center",
        horizontal_alignment="center",
        spacing=20
    )

    page.add(ft.Container(content=cont_registro, alignment=ft.alignment.center, padding=ft.padding.only(top=80)))


# =========================
# Ejecutar la app
# =========================
if __name__ == "__main__":
    ft.app(target=login_page)
