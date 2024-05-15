import flet as ft
import os
import datetime

def __view__(nombre_empresa, direccion_carpeta):
    navigation_bar = ft.Container(
            col=1,
            expand=False,
            height=120,
            content=ft.Column(
                controls=[
                    ft.Container(
                        expand=True,
                        content=ft.NavigationBar(
                            bgcolor='black',
                            selected_index=0,
                            destinations=[
                                ft.NavigationDestination(icon_content=ft.TextButton(text="USUARIO", icon=ft.icons.PERSON, style=ft.ButtonStyle(color='white', bgcolor='black'))),
                                ft.NavigationDestination(icon_content=ft.TextButton(text="NOTIFICACIONES", icon=ft.icons.NOTIFICATIONS_ACTIVE, style=ft.ButtonStyle(color='white', bgcolor='black')))
                            ]
                        )
                    ),
                ]
            )
        )
    archivos = os.listdir(direccion_carpeta)

    # Crear una lista de diccionarios con los nombres de los archivos y las fechas de modificación
    datos = [
        {
            'Nombre': archivo,
            'Fecha de modificación': datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(direccion_carpeta, archivo)))
        }
        for archivo in archivos
    ]
    tabla1 = ft.DataTable(
        data=datos,
        columns=[
            ft.DataColumn(ft.Text('Nombre')),
            ft.DataColumn(ft.Text('Fecha de modificación')),
        ]
    )

    tabla2 = ft.DataTable(
        data=datos,
        columns=[
            ft.DataColumn(ft.Text('Nombre')),
            ft.DataColumn(ft.Text('Fecha de modificación')),
        ]
    )

    # Crear la tabla
   # Crear los botones de flechas
    boton_izquierda = ft.IconButton(icon=ft.icons.ARROW_LEFT, on_click=lambda: print('Izquierda'))
    boton_derecha = ft.IconButton(icon=ft.icons.ARROW_RIGHT, on_click=lambda: print('Derecha'))

    # Organizar las tablas y los botones en una fila
    fila = ft.Row(
        controls=[
            tabla1,
            ft.Column(
                controls=[
                    boton_izquierda,
                    boton_derecha,
                ]
            ),
            tabla2,
        ]
    )

    table = ft.Container(
            border_radius=10,
            padding= 10,
            col = 8,
            expand=True,
            content= fila
            )

    respuesta=ft.Column(
        controls=[
            navigation_bar,
            fila
        ]
    )

    return respuesta