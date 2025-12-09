# main.py
import flet as ft
import sqlite3
from datetime import datetime, date
import login

DB_NAME = "gym.db"

# ============================
# IDS reales de cada tabla
# ============================
id_tablas = {
    "rol_usuario": "id_Rol",
    "usuario": "id_Usuario",
    "articulo": "id_Articulo",
    "servicio": "id_Servicio",
    "entrenamientos": "id_Entrenamiento",
    "nutricion": "id_Nutricion",
    "membresia": "id_Membresia",
    "ubicacion": "id_Ubicacion",
    "sugerencias": "id_Sugerencia",
    "carga_horas_entrenamiento": "id_Carga",
    "historial_pago": "id_Pago",
    "pedido": "id_Pedido",
    "detalle_pedido": "id_Detalle"
}

# Columnas por tabla
columnas_tablas = {
    "rol_usuario": ["Nombre_Rol", "Descripcion"],
    "usuario": ["Nombre", "Apellido", "Email", "Contraseña", "Telefono", "Fecha_Nacimiento", "id_Rol"],
    "articulo": ["Nombre", "Descripcion", "Precio", "Stock", "id_Categoria"],
    "servicio": ["Nombre", "Descripcion", "Precio"],
    "entrenamientos": ["Nombre", "Descripcion", "Duracion_Estimada"],
    "nutricion": ["Nombre", "Descripcion", "Tipo"],
    "membresia": ["Nombre", "Precio", "Duracion"],
    "ubicacion": ["Direccion", "Ciudad", "Pais"],
    "sugerencias": ["id_Usuario", "Correo", "Asunto", "Mensaje", "Fecha"],
    "carga_horas_entrenamiento": ["id_Usuario", "Fecha", "Hora_Entrada", "Hora_Salida", "Horas_Entrenadas"],
    "historial_pago": ["id_Usuario", "id_Membresia", "Monto", "Metodo_Pago", "Estado", "Fecha_Pago"],
    "pedido": ["id_Usuario", "Estado", "Fecha"],
    "detalle_pedido": ["id_Pedido", "id_Articulo", "Cantidad"]
}

# ============================
# Conexión DB
# ============================
def conectar_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def obtener_datos(tabla):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {tabla}")
    datos = cursor.fetchall()
    cursor.close()
    conn.close()
    return datos

# ============================
# PANEL PRINCIPAL
# ============================
def main(page: ft.Page, usuario=None):
    page.title = "Panel de Administración - Gym"
    page.bgcolor = "#0D0D0D"
    page.padding = 30
    page.scroll = "adaptive"

    current_tabla = "usuario"
    selected_row_index = None

    # === DataTable ===
    data_table = ft.DataTable(
        columns=[ft.DataColumn(ft.Text("Cargando...", color="white"))],
        rows=[],
        heading_row_color="#222222",
        border=ft.border.all(1, "#333333"),
        data_row_color={"hovered": "#1E1E1E"},
        expand=True,
        column_spacing=20,
        horizontal_lines=ft.border.BorderSide(0.5, "#444444"),
        vertical_lines=ft.border.BorderSide(0.5, "#444444")
    )

    form_fields = {}
    form_column = ft.Column(spacing=10, scroll="auto")

    # ============================
    # FUNCIONES CRUD
    # ============================
    def cargar_tabla(tabla):
        nonlocal current_tabla, selected_row_index
        current_tabla = tabla
        selected_row_index = None

        columnas = [id_tablas[tabla]] + columnas_tablas[tabla]

        data_table.columns.clear()
        data_table.columns.extend([
            ft.DataColumn(ft.Text(col, color="white", weight="bold"))
            for col in columnas
        ])

        datos = obtener_datos(tabla)
        data_table.rows.clear()

        for idx, fila in enumerate(datos):
            data_table.rows.append(
                ft.DataRow(
                    cells=[ft.DataCell(ft.Text(str(v), color="white")) for v in fila],
                    on_select_changed=lambda e, index=idx: seleccionar_fila(index)
                )
            )

        cargar_formulario(tabla)
        page.update()

    def seleccionar_fila(index):
        nonlocal selected_row_index
        selected_row_index = index
        fila = obtener_datos(current_tabla)[index][1:]  # Ignorar la ID
        for i, key in enumerate(columnas_tablas[current_tabla]):
            form_fields[key].value = str(fila[i])
        page.update()

    def agregar_registro(e):
        # Manejo automático de fechas y horas
        nueva_fila = []
        for key in columnas_tablas[current_tabla]:
            if key == "Fecha" or key == "Fecha_Pago" or key == "Fecha_Nacimiento":
                nueva_fila.append(date.today().isoformat())
            elif key == "Hora_Entrada" or key == "Hora_Salida":
                nueva_fila.append(datetime.now().time().replace(microsecond=0).isoformat())
            else:
                nueva_fila.append(form_fields[key].value)

        columnas_str = ", ".join(columnas_tablas[current_tabla])
        signos = ", ".join("?" for _ in columnas_tablas[current_tabla])

        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO {current_tabla} ({columnas_str}) VALUES ({signos})", nueva_fila)
        conn.commit()
        conn.close()

        cargar_tabla(current_tabla)
        limpiar_formulario()

    def modificar_registro(e):
        nonlocal selected_row_index
        if selected_row_index is not None:
            fila = obtener_datos(current_tabla)[selected_row_index]
            id_val = fila[0]

            nueva_fila = []
            for key in columnas_tablas[current_tabla]:
                if key in ["Fecha", "Fecha_Pago", "Fecha_Nacimiento", "Hora_Entrada", "Hora_Salida"]:
                    nueva_fila.append(fila[columnas_tablas[current_tabla].index(key)+1])  # No modificar fecha/hora
                else:
                    nueva_fila.append(form_fields[key].value)

            set_str = ", ".join(f"{col}=?" for col in columnas_tablas[current_tabla])

            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE {current_tabla} SET {set_str} WHERE {id_tablas[current_tabla]}=?",
                nueva_fila + [id_val]
            )
            conn.commit()
            conn.close()

            cargar_tabla(current_tabla)
            limpiar_formulario()

    def eliminar_registro(e):
        nonlocal selected_row_index
        if selected_row_index is not None:
            id_val = obtener_datos(current_tabla)[selected_row_index][0]

            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute(
                f"DELETE FROM {current_tabla} WHERE {id_tablas[current_tabla]}=?",
                (id_val,)
            )
            conn.commit()
            conn.close()

            cargar_tabla(current_tabla)
            limpiar_formulario()

    def limpiar_formulario():
        for key in form_fields:
            form_fields[key].value = ""
        page.update()

    def cargar_formulario(tabla):
        form_column.controls.clear()
        form_fields.clear()

        for col in columnas_tablas[tabla]:
            read_only = col in ["Fecha", "Hora_Entrada", "Hora_Salida", "Fecha_Pago", "Fecha_Nacimiento"]
            form_fields[col] = ft.TextField(
                label=col,
                width=250,
                read_only=read_only,
                bgcolor="#1E1E1E",
                color="white",
                border_radius=10,
                border_color="#FFD54F",
                focused_border_color="#FFC107",
                cursor_color="#FFD54F"
            )
            form_column.controls.append(form_fields[col])

        form_column.controls.append(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.ElevatedButton("Agregar", on_click=agregar_registro, bgcolor="#4CAF50", color="white"),
                            ft.ElevatedButton("Modificar", on_click=modificar_registro, bgcolor="#2196F3", color="white")
                        ],
                        alignment="center",
                        spacing=20
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton("Eliminar", on_click=eliminar_registro, bgcolor="#F44336", color="white"),
                            ft.ElevatedButton("Limpiar", on_click=lambda e: limpiar_formulario(), bgcolor="#757575", color="white")
                        ],
                        alignment="center",
                        spacing=20
                    )
                ],
                spacing=15
            )
        )

    # ============================
    # INTERFAZ
    # ============================
    def cerrar_sesion(e):
        page.clean()
        page.appbar = None
        page.drawer = None
        login.login_page(page)

    def cambiar_tabla(index):
        tablas = list(columnas_tablas.keys())
        if 0 <= index < len(tablas):
            cargar_tabla(tablas[index])
        page.drawer.open = False
        page.update()

    drawer = ft.NavigationDrawer(
        bgcolor="#1A1A1A",
        controls=[
            ft.Container(ft.Text("📋 Tablas disponibles", color="#FFD54F", size=18, weight="bold"), padding=10),
            *[ft.NavigationDrawerDestination(label=tabla.capitalize()) for tabla in columnas_tablas.keys()]
        ],
        on_change=lambda e: cambiar_tabla(e.control.selected_index)
    )

    page.appbar = ft.AppBar(
        title=ft.Text("Panel Administrativo - Gym", color="black", weight="bold"),
        bgcolor="#FFD54F",
        center_title=True,
        actions=[
            ft.ElevatedButton(
                "Cerrar sesión",
                bgcolor="black",
                color="white",
                on_click=cerrar_sesion
            )
        ]
    )

    layout = ft.Row(
        [
            ft.Container(data_table, expand=True, padding=10, border_radius=12, bgcolor="#1C1C1C"),
            ft.Container(form_column, width=300, padding=20, border_radius=12, bgcolor="#212121")
        ],
        spacing=20
    )

    page.drawer = drawer
    page.add(layout)
    cargar_tabla(current_tabla)

if __name__ == "__main__":
    ft.app(target=main)
