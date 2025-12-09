import flet as ft

def seccion_articulos(page: ft.Page):
    """
    Sección de artículos adaptativa con scroll horizontal tipo carrusel
    y modal de detalle para cada artículo, con estilo unificado.
    """

    # --- Artículos por categoría ---
    equipamiento = [
        {"nombre": "Guantes de entrenamiento", "img": "https://m.media-amazon.com/images/I/713VdnrukHL._AC_SL1500_.jpg",
         "descripcion": "Guantes cómodos para entrenamiento de fuerza y cardio."},
        {"nombre": "Remera de entrenamiento", "img": "https://pyunicentroprod.vtexassets.com/arquivos/ids/727391-800-auto?v=638580297434070000&width=800&height=auto&aspect=true",
         "descripcion": "Remeras cómodas, ideales para entrenamientos diarios."},
        {"nombre": "Medias de entrenamiento", "img": "https://www.saucony.com.py/cdn/shop/files/image_0_7d6ee366-4cbf-4012-b00e-52e1a6c17708.jpg?v=1762875789",
         "descripcion": "Medias ligeras y transpirables para ejercicios de alto rendimiento."},
        {"nombre": "Pantalón deportivo", "img": "https://www.wearfigs.com/i/contentful/5j6wpslh72e4/6UiONSB6HWQ9I0e1urao3o/3e75df902143a587796f147978d9d06b/Q3_2023_08_NAVY_TANSEN_M_DAVEY_21624.jpg?fm=webp&w=1100",
         "descripcion": "Pantalones cómodos para entrenamiento intenso."},
        {"nombre": "Zapatillas de running", "img": "https://decathlon.com.py/cdn/shop/files/pic_c297f34a-18e6-42ba-8abd-598cca113c02.jpg?v=1765179933&width=800",
         "descripcion": "Zapatillas ligeras y resistentes para correr."},
    ]

    consumo = [
        {"nombre": "Proteínas", "img": "https://tupi.com.py/imagen_articulo/MKP078463__600__600__PROTEINA--ENA-WHEY-PROTEIN-CHOCOLATE---2,05LB?t=c4b674b-0",
         "descripcion": "Suplemento proteico para ganar masa muscular."},
        {"nombre": "Bebidas energéticas", "img": "https://www.ruufe.com/cdn/shop/files/supermercados_la_vaquita_supervaquita_bebida_energizante_vive100_400ml_bebidas_liquidas.jpg?v=1724333991&width=1080",
         "descripcion": "Bebida para mantener la energía durante entrenamientos largos."},
        {"nombre": "Barras energéticas", "img": "https://i.ebayimg.com/images/g/StMAAeSw1KhoML-A/s-l1600.webp",
         "descripcion": "Snack saludable rico en proteínas y carbohidratos."},
    ]

    fisioterapia = [
        {"nombre": "Fisioterapia", "img": "https://clinicarozalen.com/wp-content/uploads/2023/10/fisioterapia-madrid.jpg",
         "descripcion": "Servicios de recuperación muscular y masajes deportivos."},
    ]

    # --- Modal de detalle ---
    modal_detalle = ft.Stack(expand=True, controls=[])

    def cerrar_modal():
        modal_detalle.controls.clear()
        page.update()

    def ver_detalle(art):
        # Fondo negro con opacidad
        fondo = ft.Container(
            bgcolor="#B3000000",  # negro con 70% opacidad
            expand=True,
            on_click=lambda e: cerrar_modal()
        )

        tarjeta_modal = ft.Container(
            content=ft.Column([
                ft.Image(src=art["img"], width=400, height=300, fit=ft.ImageFit.CONTAIN),
                ft.Text(art["nombre"], size=28, weight="bold", color=ft.Colors.YELLOW, text_align="center"),
                ft.Text(art.get("descripcion", "Sin descripción"), size=18, color=ft.Colors.WHITE, text_align="center"),
                ft.ElevatedButton("Cerrar", bgcolor=ft.Colors.YELLOW, color=ft.Colors.BLACK, width=120,
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
                ft.Text(art["nombre"], color=ft.Colors.YELLOW, size=18, weight="bold", text_align="center"),
                ft.ElevatedButton("Ver más", bgcolor=ft.Colors.YELLOW, color=ft.Colors.BLACK, width=100,
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
            ft.Text(titulo, size=24, weight="bold", color=ft.Colors.YELLOW, text_align="center"),
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
