import flet as ft

def seccion_articulos(page: ft.Page):
    """
    Sección de artículos adaptativa con scroll horizontal tipo carrusel
    y modal de detalle para cada artículo, con estilo unificado.
    """

    # --- Artículos por categoría ---
    equipamiento = [
        {"nombre": "Guantes de entrenamiento", "img": "https://upload.wikimedia.org/wikipedia/commons/3/3f/Placeholder_view_vector.svg",
         "descripcion": "Guantes cómodos para entrenamiento de fuerza y cardio."},
        {"nombre": "Remera de entrenamiento", "img": "https://upload.wikimedia.org/wikipedia/commons/3/3f/Placeholder_view_vector.svg",
         "descripcion": "Remeras cómodas, ideales para entrenamientos diarios."},
        {"nombre": "Medias de entrenamiento", "img": "https://upload.wikimedia.org/wikipedia/commons/3/3f/Placeholder_view_vector.svg",
         "descripcion": "Medias ligeras y transpirables para ejercicios de alto rendimiento."},
        {"nombre": "Pantalón deportivo", "img": "https://upload.wikimedia.org/wikipedia/commons/3/3f/Placeholder_view_vector.svg",
         "descripcion": "Pantalones cómodos para entrenamiento intenso."},
        {"nombre": "Zapatillas de running", "img": "https://upload.wikimedia.org/wikipedia/commons/3/3f/Placeholder_view_vector.svg",
         "descripcion": "Zapatillas ligeras y resistentes para correr."},
    ]

    consumo = [
        {"nombre": "Proteínas", "img": "https://upload.wikimedia.org/wikipedia/commons/3/3f/Placeholder_view_vector.svg",
         "descripcion": "Suplemento proteico para ganar masa muscular."},
        {"nombre": "Bebidas energéticas", "img": "https://upload.wikimedia.org/wikipedia/commons/3/3f/Placeholder_view_vector.svg",
         "descripcion": "Bebida para mantener la energía durante entrenamientos largos."},
        {"nombre": "Barras energéticas", "img": "https://upload.wikimedia.org/wikipedia/commons/3/3f/Placeholder_view_vector.svg",
         "descripcion": "Snack saludable rico en proteínas y carbohidratos."},
    ]

    fisioterapia = [
        {"nombre": "Fisioterapia", "img": "https://upload.wikimedia.org/wikipedia/commons/3/3f/Placeholder_view_vector.svg",
         "descripcion": "Servicios de recuperación muscular y masajes deportivos."},
    ]

    # --- Modal de detalle ---
    modal_detalle = ft.Stack(expand=True, controls=[])

    def cerrar_modal():
        modal_detalle.controls.clear()
        page.update()

    def ver_detalle(art):
        fondo = ft.Container(
            bgcolor=ft.Colors.BLACK.with_opacity(0.7),
            expand=True,
            on_click=lambda e: cerrar_modal()
        )

        tarjeta_modal = ft.Container(
            content=ft.Column([
                ft.Image(src=art["img"], width=400, height=300, fit=ft.ImageFit.CONTAIN),
                ft.Text(art["nombre"], size=28, weight="bold", color="#FFD700", text_align="center"),
                ft.Text(art.get("descripcion", "Sin descripción"), size=18, color=ft.Colors.WHITE, text_align="center"),
                ft.ElevatedButton("Cerrar", bgcolor="#FFD700", color=ft.Colors.BLACK, width=120,
                                  on_click=lambda e: cerrar_modal())
            ], horizontal_alignment="center", spacing=10),
            padding=20,
            bgcolor="#1E1E1E",
            border_radius=20,
            width=450,
            shadow=ft.BoxShadow(blur_radius=20, color="#000000", offset=ft.Offset(0,5))
        )

        modal_detalle.controls.clear()
        modal_detalle.controls.append(fondo)
        modal_detalle.controls.append(ft.Container(content=tarjeta_modal, alignment=ft.alignment.center, expand=True))
        page.update()

    # --- Crear tarjeta de artículo ---
    def crear_tarjeta(art):
        return ft.Container(
            content=ft.Column([
                ft.Image(src=art["img"], width=200, height=150, fit=ft.ImageFit.CONTAIN),
                ft.Text(art["nombre"], color="#FFD700", size=18, weight="bold", text_align="center"),
                ft.ElevatedButton("Ver más", bgcolor="#FFD700", color=ft.Colors.BLACK, width=100,
                                  on_click=lambda e, a=art: ver_detalle(a))
            ], horizontal_alignment="center", spacing=5),
            bgcolor="#1E1E1E",
            border_radius=15,
            padding=10,
            width=220,
            shadow=ft.BoxShadow(blur_radius=5, color="#000000", offset=ft.Offset(2,2))
        )

    # --- Sección con scroll horizontal centrado ---
    def seccion_scroll(titulo, lista_articulos):
        fila = ft.Row(
            controls=[crear_tarjeta(art) for art in lista_articulos],
            spacing=10,
            wrap=False,
            scroll="always",
            alignment=ft.MainAxisAlignment.CENTER
        )
        contenedor_scroll = ft.Container(
            content=fila,
            alignment=ft.alignment.center,
            width=600
        )
        return ft.Column([
            ft.Text(titulo, size=24, weight="bold", color="#FFD700", text_align="center"),
            contenedor_scroll
        ], spacing=10, horizontal_alignment="center")

    # --- Contenido principal ---
    contenido = ft.Column([
        seccion_scroll("EQUIPAMIENTO", equipamiento),
        seccion_scroll("CONSUMO", consumo),
        seccion_scroll("FISIOTERAPIA", fisioterapia)
    ], spacing=30, horizontal_alignment="center")

    # --- Stack principal para superponer modal ---
    stack_principal = ft.Stack(
        expand=True,
        controls=[contenido, modal_detalle]
    )

    return stack_principal
