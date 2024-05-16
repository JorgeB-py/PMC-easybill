import flet as ft
import os
import datetime

def __view__(page, nombre_empresa, direccion_carpeta):

    def open_dlg_modal(e):
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    def close_dlg(e):
        nombre_archivo.value = ""
        descripcion.value = ""
        fecha.value = ""
        valor_factura.value = ""
        dlg_modal.open = False
        page.update()

    def open_dlg_modal_2(e):
        page.dialog = dlg_modal_2
        dlg_modal_2.open = True
        page.update()

    def close_dlg_2(e):
        nombre_archivo.value = ""
        descripcion.value = ""
        fecha.value = ""
        valor_factura.value = ""
        dlg_modal_2.open = False
        page.update()

    nombre_archivo = ft.TextField(label="Nombre de archivo")
    descripcion = ft.TextField(label="Descripción")
    valor_factura = ft.TextField(label = "Valor a cobrar")
    fecha = ft.DatePicker(open = True)

    def agregar_archivo_no_facturadas(e):
        if nombre_archivo.value != "":
            ruta_archivo = os.path.join(direccion_carpeta + "/no_facturadas/" + nombre_archivo.value + ".txt")
            with open(ruta_archivo, "w") as archivo:
                archivo.write(f"nombre: {nombre_archivo.value}\nDescripción: {descripcion.value}\nValor de la factura: {valor_factura.value}\nSaldo en deuda: {valor_factura.value}\nFecha: {fecha.value}\n")
        dlg_modal.open = False
        nombre_archivo.value = ""
        descripcion.value = ""
        fecha.value = ""
        valor_factura.value = ""
        tabla1.update()
        page.update()

    def agregar_archivo_facturadas(e):
        if nombre_archivo.value != "":
            ruta_archivo = os.path.join(direccion_carpeta + "/facturadas/" + nombre_archivo.value + ".txt")
            with open(ruta_archivo, "w") as archivo:
                archivo.write(f"nombre: {nombre_archivo.value}\nDescripción: {descripcion.value}\nValor de la factura: {valor_factura.value}\nSaldo en deuda: 0\nFecha: {fecha.value}\n")
        dlg_modal_2.open = False
        nombre_archivo.value = ""
        descripcion.value = ""
        fecha.value = ""
        valor_factura.value = ""
        tabla2.update()
        page.update()

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Crear Factura"),
        actions=[
            nombre_archivo, descripcion, valor_factura, fecha,
            ft.ElevatedButton("Agregar", on_click=agregar_archivo_no_facturadas),
            ft.ElevatedButton("Cancelar", on_click=close_dlg)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    dlg_modal_2 = ft.AlertDialog(
        modal=True,
        title=ft.Text("Crear Factura"),
        actions=[
            nombre_archivo, descripcion, valor_factura, fecha,
            ft.ElevatedButton("Agregar", on_click=agregar_archivo_facturadas),
            ft.ElevatedButton("Cancelar", on_click=close_dlg_2)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

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
    archivos = os.listdir(direccion_carpeta + "/no_facturadas/")

    # Crear una lista de diccionarios con los nombres de los archivos y las fechas de modificación
    def get_data_no_facturadas(direccion_carpeta):
        archivos = os.listdir(direccion_carpeta + "/no_facturadas/")
        datos = [
            [
                archivo,
                datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(direccion_carpeta + "/no_facturadas/" + archivo)))
            ]
            for archivo in archivos
        ]
        return datos

    def get_data_facturadas(direccion_carpeta):
        archivos = os.listdir(direccion_carpeta + "/facturadas/")
        datos = [
            [
                archivo,
                datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(direccion_carpeta + "/facturadas/" + archivo)))
            ]
            for archivo in archivos
        ]
        return datos

    tabla1 = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text('Nombre')),
            ft.DataColumn(ft.Text('Fecha de modificación')),
        ],
        data=get_data_no_facturadas(direccion_carpeta),
    )

    tabla2 = ft.DataTable(
        show_checkbox_column=True,
        columns=[
            ft.DataColumn(ft.Text('Nombre')),
            ft.DataColumn(ft.Text('Fecha de modificación')),
        ],
        data=get_data_facturadas(direccion_carpeta),
    )
    titulo_tabla_1 = ft.Text(value="NO Facturadas",size=35,weight=ft.FontWeight.BOLD)
    titulo_tabla_2 = ft.Text(value="Facturadas",size=35,weight=ft.FontWeight.BOLD)

    # Crear la tabla
    # Crear los botones de flechas
    boton_izquierda = ft.IconButton(icon=ft.icons.ARROW_LEFT, on_click=lambda: print('Izquierda'))
    boton_derecha = ft.IconButton(icon=ft.icons.ARROW_RIGHT, on_click=lambda: print('Derecha'))

    # Crear botones de "Añadir elemento"
    boton_agregar_tabla_1 = ft.ElevatedButton(text="Crear Factura no facturada", on_click=open_dlg_modal)
    boton_agregar_tabla_2 = ft.ElevatedButton(text="Crear Factura facturada", on_click=open_dlg_modal_2)
    
    # Crear filas para las tablas y botones
    fila_boton_tabla_1 = ft.Column(controls=[titulo_tabla_1,tabla1,boton_agregar_tabla_1])

    fila_boton_tabla_2 = ft.Column(controls=[titulo_tabla_2,tabla2, boton_agregar_tabla_2])



    # Modificar la fila para incluir los botones
    fila = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            fila_boton_tabla_1,
            ft.Column(controls=[boton_izquierda, boton_derecha]),
            fila_boton_tabla_2 
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
        ],
        alignment= ft.alignment.center
    )

    return respuesta



    



    
    
    
