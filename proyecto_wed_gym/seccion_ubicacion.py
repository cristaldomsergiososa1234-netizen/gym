import flet as ft

def seccion_ubicacion(page: ft.Page):
    sucursales = [
        {
            "nombre": "PIRIBEBUY",
            "img": "https://mercadofitness.com/wp-content/uploads/2020/10/El-gimnasio-Pow-Training-Club-abrio-su-segunda-sede-en-San-Miguel.jpg",
            "desc": "Ubicado en el centro de Piribebuy, frente a la plaza principal.",
            "mapa": "https://www.google.com/maps/place/Piribebuy"
        },
        {
            "nombre": "CARAGUATAY",
            "img": "https://www.gimnasios.com.py/im/media/YTo0OntzOjI6ImlkIjtpOjE0NzgxNztzOjE6InciO2k6MzAwO3M6MToiaCI7aTozMDA7czoxOiJ0IjtzOjIzOiJwcm9maWxlLWNhcm91c2VsLXNsaWRlciI7fQ==",
            "desc": "Local moderno a una cuadra de la terminal de ómnibus.",
            "mapa": "https://www.google.com/maps/place/Caraguatay"
        },
        {
            "nombre": "ITACURUBÍ",
            "img": "https://rumboeconomico.net/wp-content/uploads/2021/03/Nota-8-imagen-principal.jpg",
            "desc": "Sucursal sobre la ruta principal, con fácil acceso desde el centro.",
            "mapa": "https://www.google.com/maps/place/Itacurubi"
        },
    ]

    tarjetas = []
    for s in sucursales:
        tarjeta = ft.Container(
            content=ft.Column([
                ft.Text(s["nombre"], size=24, weight="bold", color="#FFD700", text_align="center"),
                ft.Image(src=s["img"], width=300, height=180, fit=ft.ImageFit.COVER),
                ft.Text(s["desc"], color="white", size=16, text_align="center"),
                ft.ElevatedButton(
                    "Ubicar",
                    icon=ft.Icons.LOCATION_ON,
                    bgcolor="#FFD700",
                    color="black",
                    width=150,
                    on_click=lambda e, url=s["mapa"]: page.launch_url(url)  # 🔹 Abrir URL correctamente
                )
            ], spacing=10, horizontal_alignment="center"),
            bgcolor="#1A1A1A",
            padding=15,
            border_radius=15,
            width=320,
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(blur_radius=8, color="#000000", offset=ft.Offset(2,2))
        )
        tarjetas.append(tarjeta)

    return ft.Column([
        ft.Text("UBICACIONES", size=32, weight="bold", color="#FFD700", text_align="center"),
        ft.ResponsiveRow(
            controls=tarjetas,
            spacing=25,
            run_spacing=25,
            alignment="center"
        )
    ], spacing=30, horizontal_alignment="center")
