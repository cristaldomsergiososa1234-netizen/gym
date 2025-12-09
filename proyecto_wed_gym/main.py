import flet as ft
import login
from seccion_usuario import seccion_usuario
from seccion_membresias_premium import seccion_membresias_premium
from seccion_articulos import seccion_articulos
from seccion_ubicacion import seccion_ubicacion
from seccion_entrenamientos import seccion_entrenamientos
from seccion_sugerencias import seccion_sugerencias
from seccion_nutricion import seccion_nutricion

def main(page: ft.Page, usuario):
    usuario_dict = usuario  # Diccionario del usuario logueado

    page.title = "Gym - Portal Deportivo"
    page.bgcolor = "#121212"
    page.scroll = "adaptive"
    page.padding = 0

    contenido = ft.Column(expand=True, spacing=30, horizontal_alignment="center")

    # --- Función para refrescar la sección principal ---
    def page_update(seccion):
        contenido.controls.clear()
        contenido.controls.append(seccion)
        page.update()

    # --- Cambiar sección del menú lateral ---
    def cambiar_seccion(index):
        if index == 0:
            page_update(seccion_usuario(page, usuario_dict))
        elif index == 1:
            page_update(seccion_articulos(page))
        elif index == 2:
            page_update(seccion_entrenamientos(page))
        elif index == 3:
            page_update(seccion_nutricion(page))
        elif index == 4:
            page_update(seccion_membresias_premium(page, usuario_dict["id_Usuario"]))
        elif index == 5:
            page_update(seccion_ubicacion(page))
        elif index == 6:
            page_update(seccion_sugerencias(page, usuario_dict["id_Usuario"]))

    # --- Menú lateral ---
    drawer = ft.NavigationDrawer(
        bgcolor="#1E1E1E",
        on_change=lambda e: cambiar_seccion(e.control.selected_index),
        controls=[
            ft.Container(
                content=ft.Text("🏋️‍♂️ ManuelGym", size=22, weight="bold", color=ft.Colors.YELLOW),
                padding=ft.padding.all(20)
            ),
            ft.Divider(thickness=1, color=ft.Colors.GREY),
            ft.NavigationDrawerDestination(icon=ft.Icons.PERSON, label="Usuario"),
            ft.NavigationDrawerDestination(icon=ft.Icons.FITNESS_CENTER, label="Artículos"),
            ft.NavigationDrawerDestination(icon=ft.Icons.HOME_WORK, label="Entrenamientos"),
            ft.NavigationDrawerDestination(icon=ft.Icons.SET_MEAL, label="Nutrición"),
            ft.NavigationDrawerDestination(icon=ft.Icons.CARD_MEMBERSHIP, label="Membresías"),
            ft.NavigationDrawerDestination(icon=ft.Icons.LOCATION_ON, label="Ubicación"),
            ft.NavigationDrawerDestination(icon=ft.Icons.FEEDBACK, label="Sugerencias"),
        ]
    )
    page.drawer = drawer

    # --- Funciones de AppBar ---
    def abrir_menu(e):
        page.drawer.open = True
        page.update()

    def cerrar_sesion(e):
        page.clean()
        page.appbar = None
        page.drawer = None
        login.login_page(page)
        page.update()

    # --- Barra superior ---
    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.MENU, on_click=abrir_menu),
        title=ft.Text("MANUELGYM", weight="bold", size=20, color=ft.Colors.WHITE),
        center_title=True,
        bgcolor="#FFD700",
        actions=[
            ft.ElevatedButton(
                "Cerrar sesión",
                bgcolor=ft.Colors.RED,
                color=ft.Colors.WHITE,
                on_click=cerrar_sesion
            )
        ]
    )

    # --- Inicializar primera sección ---
    cambiar_seccion(0)

    # --- Agregar contenido principal a la página ---
    page.add(contenido)


if __name__ == "__main__":
    ft.app(target=lambda page: login.login_page(page))
