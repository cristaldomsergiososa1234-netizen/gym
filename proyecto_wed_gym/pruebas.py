import flet as ft

def main(page: ft.Page):
    # Configurar la página
    page.title = "Deslizador horizontal de imágenes"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Lista de imágenes
    imagenes = [
        "https://upload.wikimedia.org/wikipedia/commons/3/3f/Placeholder_view_vector.svg",
        "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png",
        "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg",
        "https://upload.wikimedia.org/wikipedia/commons/b/b6/Image_created_with_a_mobile_phone.png",
        "https://upload.wikimedia.org/wikipedia/commons/6/6e/Example_image.png"
    ]

    # ListView horizontal
    slider = ft.ListView(
        scroll=ft.ScrollMode.HORIZONTAL,  # Scroll horizontal
        spacing=20,
        padding=20,
        controls=[ft.Image(src=img, width=300, height=200, fit=ft.ImageFit.COVER) for img in imagenes]
    )

    page.add(slider)

ft.app(target=main)
