import flet as ft
import sqlite3

DB_NAME = "gym.db"

def seccion_membresias_premium(page: ft.Page, id_usuario):
    """
    Sección de membresías premium con tarjetas centradas, scroll horizontal
    y selección de plan con retroalimentación visual y snack.
    """

    planes = [
        {"nombre": "Mensual", "precio": 160000, "precio_mensual": "160.000 Gs/mes",
         "beneficios": ["✓ Acceso ilimitado", "✓ 1 clase personal", "✓ Acceso a vestidores", "✓ Casillero gratis"],
         "color_fondo": "#1E1E1E", "icono": ft.Icons.CALENDAR_MONTH},
        {"nombre": "Trimestral", "precio": 420000, "precio_mensual": "140.000 Gs/mes",
         "beneficios": ["✓ Acceso ilimitado", "✓ 3 clases personales", "✓ 1 asesoría nutricional", "✓ Casillero gratis"],
         "color_fondo": "#2C2C2C", "icono": ft.Icons.CALENDAR_TODAY},
        {"nombre": "Semestral", "precio": 750000, "precio_mensual": "125.000 Gs/mes",
         "beneficios": ["✓ Acceso ilimitado", "✓ 6 clases personales", "✓ 2 asesorías nutricionales", "✓ Casillero premium"],
         "color_fondo": "#333333", "icono": ft.Icons.STAR},
        {"nombre": "Anual", "precio": 1500000, "precio_mensual": "125.000 Gs/mes",
         "beneficios": ["✓ Acceso ilimitado", "✓ 12 clases personales", "✓ Asesoría nutricional completa", "✓ Casillero VIP"],
         "color_fondo": "#444444", "icono": ft.Icons.WORKSPACE_PREMIUM},
    ]

    plan_seleccionado_text = ft.Text("", size=20, color=ft.Colors.GREEN)
    tarjetas = []

    # --- Consultar membresía seleccionada previamente ---
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT m.Nombre, h.id_Pago
                FROM historial_pago h
                JOIN membresia m ON h.id_Membresia = m.id_Membresia
                WHERE h.id_Usuario = ?
                ORDER BY h.Fecha_Pago DESC LIMIT 1
            """, (id_usuario,))
            result = cursor.fetchone()
            membresia_seleccionada = result[0] if result else None
            id_pago_seleccionado = result[1] if result else None
    except Exception as ex:
        print(f"Error al obtener membresía seleccionada: {ex}")
        membresia_seleccionada = None
        id_pago_seleccionado = None

    # --- Función para seleccionar plan ---
    def seleccionar_plan(e, plan_nombre):
        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id_Membresia, Precio FROM membresia WHERE Nombre = ?", (plan_nombre,))
                result = cursor.fetchone()
                if not result:
                    raise Exception("Membresía no encontrada")
                id_membresia, precio_db = result

                cursor.execute("""
                    INSERT INTO historial_pago (id_Usuario, id_Membresia, Monto, Metodo_Pago, Estado)
                    VALUES (?, ?, ?, ?, ?)
                """, (id_usuario, id_membresia, precio_db, "Efectivo", "Pendiente"))
                conn.commit()
                cursor.execute("SELECT last_insert_rowid()")
                id_pago = cursor.fetchone()[0]

            # Actualizar tarjetas visualmente
            for t in tarjetas:
                if t["nombre"] != plan_nombre:
                    t["container"].bgcolor = "#555555"
                    t["container"].content.controls[0].controls[1].color = "#AAAAAA"
                else:
                    t["container"].bgcolor = t["container"].original_color
            plan_seleccionado_text.value = f"Membresía {plan_nombre} seleccionada correctamente ({precio_db:,} Gs)"
            page.snack_bar = ft.SnackBar(ft.Text(f"Membresía {plan_nombre} guardada!"), open=True)
            page.update()
        except Exception as ex:
            plan_seleccionado_text.value = f"Error: {ex}"
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al seleccionar plan: {ex}"), open=True)
            page.update()

    # --- Crear tarjeta de plan ---
    def crear_tarjeta(plan):
        boton = ft.ElevatedButton(
            "Seleccionar Plan",
            bgcolor="#FFD700",
            color="black",
            width=200,
            on_click=lambda e, nombre=plan["nombre"]: seleccionar_plan(e, nombre)
        )

        tarjeta = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(plan["icono"], color="#FFD700", size=30),
                    ft.Text(plan["nombre"], size=24, weight="bold", color="#FFD700")
                ], alignment="center"),
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"{plan['precio']:,} Gs", size=32, weight="bold", color="white"),
                        ft.Text(f"({plan['precio_mensual']})", size=14, color="#CCCCCC", italic=True)
                    ], spacing=0, horizontal_alignment="center"),
                    margin=ft.margin.symmetric(vertical=15)
                ),
                ft.Divider(color="#FFD700", height=1),
                ft.Column([ft.Text(b, color="white", size=14) for b in plan["beneficios"]], spacing=10),
                boton
            ], spacing=10, horizontal_alignment="center"),
            bgcolor=plan["color_fondo"],
            padding=20,
            border_radius=15,
            width=250,
            height=500
        )

        tarjeta.original_color = plan["color_fondo"]

        # Si ya está seleccionada previamente
        if membresia_seleccionada:
            if plan["nombre"] != membresia_seleccionada:
                tarjeta.bgcolor = "#555555"
                tarjeta.content.controls[0].controls[1].color = "#AAAAAA"
                boton.visible = False
            else:
                boton.visible = False
                plan_seleccionado_text.value = f"Membresía seleccionada: {plan['nombre']}"

        tarjetas.append({"container": tarjeta, "nombre": plan["nombre"]})
        return tarjeta

    # --- Scroll horizontal centrado ---
    fila_tarjetas = ft.Row(
        controls=[crear_tarjeta(p) for p in planes],
        spacing=20,
        wrap=False,
        scroll="always",
        alignment=ft.MainAxisAlignment.CENTER
    )

    return ft.Column([
        ft.Text("MEMBRESÍAS PREMIUM", size=32, weight="bold", color="#FFD700", text_align="center"),
        ft.Text("Elige el plan que mejor se adapte a tus objetivos", size=16, color="#CCCCCC", text_align="center"),
        ft.Container(fila_tarjetas, alignment=ft.alignment.center),
        ft.Container(plan_seleccionado_text, alignment=ft.alignment.center, padding=10)
    ], spacing=20, horizontal_alignment="center")
