import flet as ft

def seccion_nutricion(page: ft.Page):
    """
    Sección de nutrición con tarjetas centradas en scroll horizontal y modal de detalle.
    """

    # === Datos ===
    planes_alimentacion = [
        {"nombre": "Plan de Definición", "img": "https://blog.planseguro.com.mx/wp-content/uploads/2023/03/en-que-consiste-un-plan-de-alimentacion.jpg",
         "descripcion": "Diseñado para reducir el porcentaje de grasa corporal sin perder masa muscular.",
         "objetivo": "Reducir grasa corporal manteniendo masa muscular.",
         "beneficios": "Mayor tono muscular, mejor digestión y más energía.",
         "consejos": "Comidas pequeñas cada 3 horas, controlar carbohidratos refinados."},
        {"nombre": "Plan de Volumen", "img": "https://images.tely.ai/telyai/planning-a-volume-diet-in-a-modern-kitchen-ghmjqjhv.webp",
         "descripcion": "Plan orientado al aumento de masa muscular mediante un superávit calórico controlado.",
         "objetivo": "Incrementar masa muscular y fuerza.",
         "beneficios": "Crecimiento muscular y aumento de fuerza.",
         "consejos": "Acompañar con entrenamiento de fuerza y descanso adecuado."},
        {"nombre": "Plan de Mantenimiento", "img": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEip4doo9Nr5hCsBZp19hYXxLQFtclFG5BU7crYdo0nbGsjzImeSY10HibUokYVeuuFGpRWuGpkPPGi0a_HqI43q2MD1MNLpOR1UQHgB5zdjV68_LzoHinN0Deo8dkV7IVPa2VZ7OByxg4I/s1600/Plan-nutricional-de-mantenimiento.jpg",
         "descripcion": "Ideal para mantener el peso corporal y nivel energético estable.",
         "objetivo": "Mantener peso y nivel energético.",
         "beneficios": "Estabilidad metabólica y bienestar general.",
         "consejos": "Seguir dieta equilibrada y variada."},
    ]

    recetas_saludables = [
        {"nombre": "Batido Energizante", "img": "https://hips.hearstapps.com/hmg-prod/images/gettyimages-1470339263-67a09e472ebea.jpg?crop=1xw:0.84375xh;0,0.164xh",
         "descripcion": "Batido natural con banana, avena, miel y leche vegetal.",
         "objetivo": "Aportar energía antes del entrenamiento.",
         "beneficios": "Recuperación rápida y energía inmediata.",
         "consejos": "Añadir mantequilla de maní para más proteínas."},
        {"nombre": "Ensalada Proteica", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT28zHM_zwRFV1e4Mgp06ehJFKmjtn0qi0XWg&s",
         "descripcion": "Pechuga de pollo, huevo duro, palta y vegetales frescos.",
         "objetivo": "Almuerzo post-entrenamiento alto en proteínas.",
         "beneficios": "Aporta proteínas de calidad y grasas saludables.",
         "consejos": "Añadir aceite de oliva y limón para sabor y digestión."},
    ]

    suplementos = [
        {"nombre": "Proteína Whey", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQadKYkBLPTl7M6AkL2qd2euMRTjwBmhbqSFA&s",
         "descripcion": "Suplemento para crecimiento y reparación muscular.",
         "objetivo": "Favorecer hipertrofia y recuperación post-entreno.",
         "beneficios": "Aporta aminoácidos esenciales de rápida absorción.",
         "consejos": "Consumir después del entrenamiento para mejor absorción."},
        {"nombre": "BCAA", "img": "https://tiendanaranja.com.py/media/catalog/product/7/1/71912.jpg?optimize=medium&bg-color=255,255,255&fit=bounds&height=700&width=700&canvas=700:700",
         "descripcion": "Aminoácidos de cadena ramificada.",
         "objetivo": "Reducir fatiga y catabolismo muscular.",
         "beneficios": "Mejora recuperación y rendimiento.",
         "consejos": "Tomar antes o durante el entrenamiento."},
    ]

    tips_nutricion = [
        {"nombre": "Hidrátate", "img": "https://fisio-clinics.com/sites/default/files/field/image/importancia_de_la_hidratacion_en_tu_salud.jpeg",
         "descripcion": "Beber al menos 2 litros de agua diarios.",
         "objetivo": "Mantener rendimiento físico y concentración.",
         "beneficios": "Mejor digestión y energía estable.",
         "consejos": "Evitar bebidas azucaradas y energéticas."},
        {"nombre": "Evita azúcares procesados", "img": "https://media.gq.com.mx/photos/6818e900fb92e46208e1f7de/master/w_1600%2Cc_limit/Ilustracio%25CC%2581n_Alimentos_Azucarados_a_Evitar%2520(1).jpg",
         "descripcion": "Reducir azúcares refinados en la dieta.",
         "objetivo": "Mantener niveles de glucosa y evitar grasa corporal.",
         "beneficios": "Más energía y mejor estado de ánimo.",
         "consejos": "Usar miel o stevia como endulzante natural."},
    ]

    # --- Modal de detalle ---
    modal_detalle = ft.Stack(expand=True, controls=[])

    def cerrar_modal():
        modal_detalle.controls.clear()
        page.update()

    def ver_detalle(item):
        # Fondo negro con opacidad
        fondo = ft.Container(
            bgcolor="#B3000000",  # 70% de opacidad
            expand=True,
            on_click=lambda e: cerrar_modal()
        )

        tarjeta_modal = ft.Container(
            content=ft.Column([
                ft.Image(src=item["img"], width=400, height=300, fit=ft.ImageFit.CONTAIN),
                ft.Text(item["nombre"], size=28, weight="bold", color=ft.Colors.YELLOW, text_align="center"),
                ft.Text(f"Descripción: {item['descripcion']}", color=ft.Colors.WHITE, text_align="center"),
                ft.Text(f"Objetivo: {item['objetivo']}", color=ft.Colors.WHITE, text_align="center"),
                ft.Text(f"Beneficios: {item['beneficios']}", color=ft.Colors.WHITE, text_align="center"),
                ft.Text(f"Consejos: {item['consejos']}", color=ft.Colors.WHITE, text_align="center"),
                ft.ElevatedButton("Cerrar", bgcolor=ft.Colors.YELLOW, color=ft.Colors.BLACK, width=120, on_click=lambda e: cerrar_modal())
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

    # --- Crear tarjeta ---
    def crear_tarjeta(item):
        return ft.Container(
            content=ft.Column([
                ft.Image(src=item["img"], width=200, height=150, fit=ft.ImageFit.CONTAIN),
                ft.Text(item["nombre"], size=18, color=ft.Colors.YELLOW, weight="bold", text_align="center"),
                ft.ElevatedButton("Ver más", bgcolor=ft.Colors.YELLOW, color=ft.Colors.BLACK, width=100,
                                  on_click=lambda e, i=item: ver_detalle(i))
            ], horizontal_alignment="center", spacing=5),
            bgcolor="#1E1E1E",
            border_radius=15,
            padding=10,
            width=220,
            shadow=ft.BoxShadow(blur_radius=5, color="#000000", offset=ft.Offset(2,2))
        )

    # --- Sección con scroll horizontal centrado ---
    def seccion_scroll(titulo, lista_items):
        fila = ft.Row(
            controls=[crear_tarjeta(i) for i in lista_items],
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
        seccion_scroll("PLANES DE ALIMENTACIÓN", planes_alimentacion),
        seccion_scroll("RECETAS SALUDABLES", recetas_saludables),
        seccion_scroll("SUPLEMENTOS", suplementos),
        seccion_scroll("TIPS DE NUTRICIÓN", tips_nutricion)
    ], spacing=30, horizontal_alignment="center")

    # --- Stack principal para superponer modal ---
    stack_principal = ft.Stack(
        expand=True,
        controls=[contenido, modal_detalle]
    )

    return stack_principal
