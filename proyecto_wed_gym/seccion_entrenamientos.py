import flet as ft

def seccion_entrenamientos(page: ft.Page):
    """
    Sección de entrenamientos con tarjetas en scroll horizontal centrado y modal de detalle.
    """

    # --- Ejercicios por categoría ---
    piernas = [
        {"nombre": "Sentadillas", "img": "https://mhunters.com/wp-content/uploads/2020/07/como-hacer-sentadillas-posiciones.jpg",
         "descripcion": "Ejercicio básico para fortalecer muslos y glúteos.",
         "objetivo": "Fortalecer cuádriceps, glúteos y core.",
         "beneficios": "Mejora la postura, el equilibrio y la fuerza funcional.",
         "consejos": "Mantén la espalda recta, los pies firmes y no dejes que las rodillas sobrepasen los pies.",
         "variaciones": "Sentadillas con salto, sumo, con barra o con mancuernas.",
         "tiempo": "4 series de 15 repeticiones", "duracion": "40 segundos por serie"},
        {"nombre": "Zancadas", "img": "https://www.sportlife.es/uploads/s1/75/62/88/9/5cc549e90de6941e683494e7-zancadas-para-pierna-o-para-gluteo.jpeg",
         "descripcion": "Trabaja piernas y estabilidad con movimientos controlados.",
         "objetivo": "Fortalecer muslos, glúteos y mejorar el equilibrio.",
         "beneficios": "Aumenta la estabilidad y coordinación del tren inferior.",
         "consejos": "Mantén la espalda recta y evita inclinarte hacia adelante.",
         "variaciones": "Zancadas laterales, caminando, o con mancuernas.",
         "tiempo": "3 series de 10 repeticiones por pierna", "duracion": "45 segundos por serie"},
    ]

    abdomen = [
        {"nombre": "Plancha", "img": "https://www.sportlife.es/uploads/s1/76/33/69/8/article-como-conseguir-plancha-abdominal-perfecta-clave-alineacion-590b47c50eeff.jpeg",
         "descripcion": "Fortalece el core y mejora la postura corporal.",
         "objetivo": "Reforzar abdomen, espalda y hombros.",
         "beneficios": "Aumenta la estabilidad y reduce el riesgo de lesiones.",
         "consejos": "Evita hundir la cadera y mantén la cabeza alineada con el cuerpo.",
         "variaciones": "Plancha lateral, con brazos extendidos o levantando una pierna.",
         "tiempo": "3 repeticiones", "duracion": "1 minuto por repetición"},
        {"nombre": "Crunch", "img": "https://hips.hearstapps.com/hmg-prod/images/crunch-1588842220.jpg",
         "descripcion": "Ejercicio clásico para los abdominales superiores.",
         "objetivo": "Fortalecer y tonificar el abdomen superior.",
         "beneficios": "Mejora la definición abdominal y la fuerza del core.",
         "consejos": "Evita jalar el cuello y controla la respiración.",
         "variaciones": "Crunch con giro, inverso o en pelota suiza.",
         "tiempo": "3 series de 15 repeticiones", "duracion": "30 segundos por serie"},
    ]

    brazos = [
        {"nombre": "Curl bíceps", "img": "https://hips.hearstapps.com/hmg-prod/images/bicep-curls-1655286150.jpg?resize=980:*",
         "descripcion": "Fortalece y desarrolla los músculos del bíceps.",
         "objetivo": "Aumentar fuerza y volumen en brazos.",
         "beneficios": "Mejora la capacidad de levantar peso y la apariencia muscular.",
         "consejos": "Evita balancear los brazos, mantén los codos fijos.",
         "variaciones": "Curl con barra, alternado o con cuerda.",
         "tiempo": "3 series de 12 repeticiones", "duracion": "35 segundos por serie"},
        {"nombre": "Flexiones", "img": "https://bulevip.com/blog/wp-content/uploads/2017/06/flexiones-t%C3%A9cnica.jpg",
         "descripcion": "Ejercicio compuesto que activa pecho, tríceps y hombros.",
         "objetivo": "Fortalecer el torso y mejorar la estabilidad general.",
         "beneficios": "Aumenta fuerza funcional y resistencia.",
         "consejos": "Mantén el cuerpo recto y evita bajar demasiado la cadera.",
         "variaciones": "Flexiones inclinadas, diamante o con mancuernas.",
         "tiempo": "3 series de 10 repeticiones", "duracion": "40 segundos por serie"},
    ]

    # --- Modal de detalle ---
    modal_detalle = ft.Stack(expand=True, controls=[])

    def cerrar_modal():
        modal_detalle.controls.clear()
        page.update()

    def ver_detalle(ejercicio):
        # Fondo negro con opacidad (70%)
        fondo = ft.Container(
            bgcolor="#B3000000",
            expand=True,
            on_click=lambda e: cerrar_modal()
        )

        tarjeta_modal = ft.Container(
            content=ft.Column([
                ft.Image(src=ejercicio["img"], width=400, height=300, fit=ft.ImageFit.CONTAIN),
                ft.Text(ejercicio["nombre"], size=28, weight="bold", color=ft.Colors.YELLOW, text_align="center"),
                ft.Text(f"Descripción: {ejercicio['descripcion']}", color=ft.Colors.WHITE, text_align="center"),
                ft.Text(f"Objetivo: {ejercicio['objetivo']}", color=ft.Colors.WHITE, text_align="center"),
                ft.Text(f"Beneficios: {ejercicio['beneficios']}", color=ft.Colors.WHITE, text_align="center"),
                ft.Text(f"Consejos: {ejercicio['consejos']}", color=ft.Colors.WHITE, text_align="center"),
                ft.Text(f"Variaciones: {ejercicio['variaciones']}", color=ft.Colors.WHITE, text_align="center"),
                ft.Text(f"Tiempo: {ejercicio['tiempo']}", color=ft.Colors.YELLOW, text_align="center"),
                ft.Text(f"Duración: {ejercicio['duracion']}", color=ft.Colors.YELLOW, text_align="center"),
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

    # --- Crear tarjeta de ejercicio ---
    def crear_tarjeta(ej):
        return ft.Container(
            content=ft.Column([
                ft.Image(src=ej["img"], width=200, height=150, fit=ft.ImageFit.CONTAIN),
                ft.Text(ej["nombre"], size=18, color=ft.Colors.YELLOW, weight="bold", text_align="center"),
                ft.ElevatedButton("Ver más", bgcolor=ft.Colors.YELLOW, color=ft.Colors.BLACK, width=100,
                                  on_click=lambda e, x=ej: ver_detalle(x))
            ], horizontal_alignment="center", spacing=5),
            bgcolor="#1E1E1E",
            border_radius=15,
            padding=10,
            width=220,
            shadow=ft.BoxShadow(blur_radius=5, color="#000000", offset=ft.Offset(2,2))
        )

    # --- Sección de categoría con scroll horizontal centrado ---
    def seccion_categoria_scroll(titulo, lista_ejercicios):
        fila = ft.Row(
            controls=[crear_tarjeta(ej) for ej in lista_ejercicios],
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
        seccion_categoria_scroll("PIERNAS", piernas),
        seccion_categoria_scroll("ABDOMEN", abdomen),
        seccion_categoria_scroll("BRAZOS", brazos)
    ], spacing=30, horizontal_alignment="center")

    # --- Stack principal para superponer modal ---
    stack_principal = ft.Stack(
        expand=True,
        controls=[contenido, modal_detalle]
    )

    return stack_principal
