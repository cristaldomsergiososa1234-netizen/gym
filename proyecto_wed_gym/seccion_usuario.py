import flet as ft
import sqlite3
from datetime import datetime

DB_NAME = "gym.db"

def seccion_usuario(page: ft.Page, usuario):
    # =========================
    # Consultar horas reales
    # =========================
    horas_entrenamiento = "0h"
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT SUM(Horas_Entrenadas)
                FROM carga_horas_entrenamiento
                WHERE id_Usuario = ?
            """, (usuario["id_Usuario"],))
            resultado = cursor.fetchone()
            if resultado and resultado[0]:
                horas_entrenamiento = f"{resultado[0]}h"
    except Exception as ex:
        print("Error al obtener horas de entrenamiento:", ex)

    # Inputs ocultos inicialmente para edición
    email_input = ft.TextField(value=usuario.get("Email",""), width=300, visible=False)
    telefono_input = ft.TextField(value=usuario.get("telefono",""), width=300, visible=False)

    # Contenedores de texto normales
    email_text = ft.Container(
        ft.Text(usuario.get("Email",""), color="black", size=18, weight="bold"),
        bgcolor="#FFD700", padding=10, border_radius=8, width=300, alignment=ft.alignment.center
    )
    telefono_text = ft.Container(
        ft.Text(usuario.get("telefono",""), color="black", size=18, weight="bold"),
        bgcolor="#FFD700", padding=10, border_radius=8, width=300, alignment=ft.alignment.center
    )
    horas_text = ft.Container(
        ft.Text(horas_entrenamiento, color="black", size=18, weight="bold"),
        bgcolor="#FFD700", padding=10, border_radius=8, width=300, alignment=ft.alignment.center
    )

    mensaje_estado = ft.Text("", color=ft.Colors.GREEN)

    # =========================
    # Botón editar/guardar
    # =========================
    def editar_click(e):
        if editar_btn.text == "Editar perfil":
            email_text.visible = False
            telefono_text.visible = False
            email_input.visible = True
            telefono_input.visible = True
            editar_btn.text = "Guardar"
        else:
            nuevo_email = email_input.value.strip()
            nuevo_telefono = telefono_input.value.strip()

            if not nuevo_email or not nuevo_telefono:
                mensaje_estado.value = "Completa todos los campos"
                mensaje_estado.color = ft.Colors.RED
                page.update()
                return

            # Actualizar textos visibles
            email_text.content.value = nuevo_email
            telefono_text.content.value = nuevo_telefono

            # Guardar cambios en DB
            try:
                with sqlite3.connect(DB_NAME) as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE usuario
                        SET Email = ?, Telefono = ?
                        WHERE id_Usuario = ?
                    """, (nuevo_email, nuevo_telefono, usuario["id_Usuario"]))
                    conn.commit()
                mensaje_estado.value = "Perfil actualizado correctamente"
                mensaje_estado.color = ft.Colors.GREEN
            except Exception as ex:
                mensaje_estado.value = f"Error al actualizar: {ex}"
                mensaje_estado.color = ft.Colors.RED

            email_text.visible = True
            telefono_text.visible = True
            email_input.visible = False
            telefono_input.visible = False
            editar_btn.text = "Editar perfil"

        page.update()

    editar_btn = ft.ElevatedButton("Editar perfil", bgcolor="#FFD700", color="black", width=150, on_click=editar_click)

    # =========================
    # Botón Entrada/Salida
    # =========================
    def entrada_salida_click(e):
        ahora = datetime.now()
        fecha_str = ahora.date().isoformat()
        hora_str = ahora.time().replace(microsecond=0).isoformat()

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            # Verificar si hay entrada sin salida
            cursor.execute("""
                SELECT id_Carga, Hora_Entrada, Fecha
                FROM carga_horas_entrenamiento
                WHERE id_Usuario = ? AND Hora_Salida IS NULL
                ORDER BY id_Carga DESC LIMIT 1
            """, (usuario["id_Usuario"],))
            registro = cursor.fetchone()

            if registro:
                # Registrar salida
                id_carga, hora_entrada_str, fecha_entrada_str = registro
                hora_entrada_dt = datetime.strptime(f"{fecha_entrada_str} {hora_entrada_str}", "%Y-%m-%d %H:%M:%S")
                horas = round((ahora - hora_entrada_dt).total_seconds() / 3600, 1)

                cursor.execute("""
                    UPDATE carga_horas_entrenamiento
                    SET Hora_Salida = ?, Horas_Entrenadas = ?
                    WHERE id_Carga = ?
                """, (hora_str, horas, id_carga))
                conn.commit()

                mensaje_estado.value = f"Salida registrada. Horas entrenadas: {horas}h"
                mensaje_estado.color = ft.Colors.GREEN
                btn_entrada_salida.text = "Registrar Entrada"

            else:
                # Registrar entrada
                cursor.execute("""
                    INSERT INTO carga_horas_entrenamiento (id_Usuario, Fecha, Hora_Entrada)
                    VALUES (?, ?, ?)
                """, (usuario["id_Usuario"], fecha_str, hora_str))
                conn.commit()
                mensaje_estado.value = f"Entrada registrada a las {hora_str}"
                mensaje_estado.color = ft.Colors.GREEN
                btn_entrada_salida.text = "Registrar Salida"

            # Actualizar la suma de horas
            cursor.execute("""
                SELECT SUM(Horas_Entrenadas)
                FROM carga_horas_entrenamiento
                WHERE id_Usuario = ?
            """, (usuario["id_Usuario"],))
            total = cursor.fetchone()[0]
            horas_text.content.value = f"{total if total else 0}h"

        page.update()

    btn_entrada_salida = ft.ElevatedButton(
        "Registrar Entrada", bgcolor="#FFD700", color="black", width=150, on_click=entrada_salida_click
    )

    # =========================
    # Construir columna del perfil
    # =========================
    perfil = ft.Column([
        ft.Text("PERFIL", size=32, weight="bold", color="#FFD700"),
        ft.Image(src=usuario.get("foto", "https://thumbs.dreamstime.com/b/silhouette-de-un-hombre-muscular-y-una-mujer-en-forma-emblema-gimnasio-silueta-musculoso-buena-con-pandillas-sembradas-prensa-400870742.jpg"),
                 width=120, height=120, border_radius=999, fit=ft.ImageFit.COVER),
        ft.Text(f"{usuario.get('Nombre','')} {usuario.get('Apellido','')}".upper(), size=24, weight="bold", color="#FFD700"),
        ft.Column([
            ft.Column([ft.Text("CORREO:", color="#FFD700", size=16, weight="bold"), email_text, email_input], spacing=5),
            ft.Column([ft.Text("TELÉFONO:", color="#FFD700", size=16, weight="bold"), telefono_text, telefono_input], spacing=5),
            ft.Column([ft.Text("H. ENTRENAMIENTO:", color="#FFD700", size=16, weight="bold"), horas_text], spacing=5)
        ], spacing=10, horizontal_alignment="center"),
        ft.Row([editar_btn, btn_entrada_salida], alignment="center", spacing=20),
        mensaje_estado
    ], horizontal_alignment="center", spacing=20)

    return perfil
