import flet as ft
import sqlite3

DB_NAME = "gym.db"

def seccion_sugerencias(page: ft.Page, id_usuario):
    # Obtener datos del usuario
    nombre_usuario = ""
    correo_usuario = ""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Nombre, Email FROM usuario WHERE id_Usuario = ?", (id_usuario,))
            resultado = cursor.fetchone()
            if resultado:
                nombre_usuario, correo_usuario = resultado
    except Exception as ex:
        print(f"Error al obtener datos del usuario: {ex}")

    # Campos del formulario
    nombre_input = ft.TextField(
        label="Nombre",
        value=nombre_usuario,
        bgcolor="#1A1A1A",
        color="white",
        border_color="#FFD700",
        width=300,
        disabled=True
    )
    correo_input = ft.TextField(
        label="Correo",
        value=correo_usuario,
        bgcolor="#1A1A1A",
        color="white",
        border_color="#FFD700",
        width=300,
        disabled=True
    )
    asunto_input = ft.TextField(
        label="Asunto",
        bgcolor="#1A1A1A",
        color="white",
        border_color="#FFD700",
        width=300
    )
    mensaje_input = ft.TextField(
        label="Mensaje",
        bgcolor="#1A1A1A",
        color="white",
        border_color="#FFD700",
        width=300,
        multiline=True,
        height=100
    )
    mensaje_estado = ft.Text("", color=ft.Colors.GREEN)

    def enviar_click(e):
        asunto = asunto_input.value.strip()
        mensaje = mensaje_input.value.strip()

        if not (asunto and mensaje):
            mensaje_estado.value = "Completa los campos obligatorios"
            mensaje_estado.color = ft.Colors.RED
            page.update()
            return

        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO sugerencias (id_Usuario, Correo, Asunto, Mensaje)
                    VALUES (?, ?, ?, ?)
                """, (id_usuario, correo_usuario, asunto, mensaje))
                conn.commit()
            mensaje_estado.value = "¡Sugerencia enviada correctamente!"
            mensaje_estado.color = ft.Colors.GREEN
            # Limpiar campos
            asunto_input.value = ""
            mensaje_input.value = ""
            page.update()
        except Exception as ex:
            mensaje_estado.value = f"Error al enviar: {ex}"
            mensaje_estado.color = ft.Colors.RED
            page.update()

    # Layout
    return ft.Column([
        # Título general
        ft.Container(
            content=ft.Text("SUGERENCIAS", size=32, weight="bold", color="#FFD700"),
            alignment=ft.alignment.center,
            padding=ft.padding.only(top=20, bottom=10)
        ),
        # Mensaje introductorio
        ft.Container(
            content=ft.Text(
                "¡Queremos tu opinión!\nDéjanos un mensaje para mejorar nuestros servicios.",
                size=18,
                color=ft.Colors.WHITE,
                text_align="center"
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.only(bottom=20)
        ),
        # Contenedor del formulario
        ft.Container(
            content=ft.Column([
                nombre_input,
                correo_input,
                asunto_input,
                mensaje_input,
                ft.ElevatedButton("Enviar", bgcolor="#FFD700", color="black", width=150, height=40, on_click=enviar_click),
                mensaje_estado
            ], spacing=15, horizontal_alignment="center"),
            padding=ft.padding.all(20),
            bgcolor="#1A1A1A",
            border_radius=15,
            alignment=ft.alignment.center
        )
    ], spacing=20, horizontal_alignment="center")
