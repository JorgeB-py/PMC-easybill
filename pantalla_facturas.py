import flet as ft
import os
import datetime
from pathlib import Path
import shutil
import platform
import subprocess
import csv

def __view__(page, nombre_empresa, direccion_carpeta):

    def open_dlg_modal(e):
        page.dialog = dlg_modal
        dlg_modal.open = True
        fecha.open = True
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
        fecha.open = True
        page.update()

    def close_dlg_2(e):
        nombre_archivo.value = ""
        descripcion.value = ""
        fecha.value = ""
        valor_factura.value = ""
        dlg_modal_2.open = False
        page.update()

    def open_dlg_fecha(e, files, direccion):
        page.dialog = dlg_fecha
        dlg_fecha.open = True
        fecha_carga.open = True
        global archivos_a_cargar
        archivos_a_cargar = files
        global carpeta_destino
        carpeta_destino = direccion
        page.update()

    def close_dlg_fecha(e):
        fecha_carga.value = ""
        dlg_fecha.open = False
        page.update()

    nombre_archivo = ft.TextField(label="Nombre de archivo")
    descripcion = ft.TextField(label="Descripción")
    valor_factura = ft.TextField(label="Valor a cobrar")
    fecha = ft.DatePicker()

    fecha_carga = ft.DatePicker()

    def agregar_archivo_no_facturadas(e):
        if nombre_archivo.value != "":
            ruta_archivo = os.path.join(direccion_carpeta + "/no_facturadas/" + nombre_archivo.value + ".txt")
            with open(ruta_archivo, "w") as archivo:
                archivo.write(f"nombre: {nombre_archivo.value}\nDescripción: {descripcion.value}\nValor de la factura: {valor_factura.value}\nSaldo en deuda: {valor_factura.value}\nFecha: {fecha.value}\n")
            with open(os.path.join(direccion_carpeta, "registro.csv"), mode="a", newline='') as file:
                writer = csv.writer(file)
                writer.writerow([(nombre_archivo.value + ".txt"), fecha.value, "False"])
        cargar_tabla_1(nombre_archivo.value + ".txt", fecha.value)
        dlg_modal.open = False
        nombre_archivo.value = ""
        descripcion.value = ""
        fecha.value = ""
        valor_factura.value = ""
        page.update()

    def agregar_archivo_facturadas(e):
        if nombre_archivo.value != "":
            ruta_archivo = os.path.join(direccion_carpeta + "/facturadas/" + nombre_archivo.value + ".txt")
            with open(ruta_archivo, "w") as archivo:
                archivo.write(f"nombre: {nombre_archivo.value}\nDescripción: {descripcion.value}\nValor de la factura: {valor_factura.value}\nSaldo en deuda: 0\nFecha: {fecha.value}\n")
            with open(os.path.join(direccion_carpeta, "registro.csv"), mode="a", newline='') as file:
                writer = csv.writer(file)
                writer.writerow([(nombre_archivo.value + ".txt"), fecha.value, "True"])
        cargar_tabla_2(nombre_archivo.value + ".txt", fecha.value)
        dlg_modal_2.open = False
        nombre_archivo.value = ""
        descripcion.value = ""
        fecha.value = ""
        valor_factura.value = ""
        page.update()

    def agregar_archivos_cargados(e):
        global archivos_a_cargar
        global carpeta_destino
        if carpeta_destino == "/no_facturadas":
            facturado = "False"
        else:
            facturado = "True"
        if fecha_carga.value != "":
            for file in archivos_a_cargar:
                nombre_archivo = Path(file.path).stem
                ruta_archivo = os.path.join(direccion_carpeta + carpeta_destino + "/" + nombre_archivo + ".txt")
                shutil.move(file.path, ruta_archivo)
                with open(os.path.join(direccion_carpeta, "registro" + ".csv"), mode="a", newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([nombre_archivo, fecha_carga.value, facturado])
            cargar_tablas()
            page.update()
        close_dlg_fecha(e)

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

    dlg_fecha = ft.AlertDialog(
        modal=True,
        title=ft.Text("Cargar Archivos"),
        actions=[
            fecha_carga,
            ft.ElevatedButton("Agregar", on_click=agregar_archivos_cargados),
            ft.ElevatedButton("Cancelar", on_click=close_dlg_fecha)
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
    datos1 = [
        [
            archivo,
            datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(direccion_carpeta + "/no_facturadas/" + archivo)))
        ]
        for archivo in archivos
    ]

    archivos2 = os.listdir(direccion_carpeta + "/facturadas/")
    datos2 = [
        [
            archivo,
            datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(direccion_carpeta + "/facturadas/" + archivo)))
        ]
        for archivo in archivos2
    ]

    search_field = ft.TextField(label="Buscar por nombre de factura", on_change=lambda e: filtrar_tablas())
    date_field_text = ft.Text("Filtrar por fecha: ")

    def on_date_change(e):
        if date_filter.value:
            date_button.text = date_filter.value
        else:
            date_button.text = "Pick date"
        filtrar_tablas()
        page.update()

    date_filter = ft.DatePicker(on_change=on_date_change)
    page.overlay.append(date_filter)

    date_button = ft.ElevatedButton(
        "Pick date",
        icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda _: date_filter.pick_date(),
    )

    def clear_date_filter(e):
        date_filter.value = None
        date_button.text = "Pick date"
        filtrar_tablas()
        page.update()

    clear_date_button = ft.ElevatedButton(
        "Clear date",
        icon=ft.icons.CLEAR,
        on_click=clear_date_filter,
    )

    def filtrar_tablas():
        search_query = search_field.value.lower()
        selected_date = date_filter.value
        tabla1.rows.clear()
        tabla2.rows.clear()
        
        with open(Path(direccion_carpeta) / "registro.csv", mode="r") as archivo:
            reader = csv.reader(archivo)
            for fila in reader:
                if fila[0] != "nombre_factura":
                    facturado = fila[2] == 'True'
                    nombre_factura = fila[0]
                    fecha_factura = fila[1]

                    # Filtrar por nombre
                    if search_query and search_query not in nombre_factura.lower():
                        continue
                    
                    # Filtrar por fecha
                    if selected_date and selected_date != datetime.datetime.strptime(fecha_factura, "%Y-%m-%d %H:%M:%S"):
                        continue

                    if not facturado:
                        cargar_tabla_1(nombre_factura, fecha_factura)
                    else:
                        cargar_tabla_2(nombre_factura, fecha_factura)
        
        page.update()

    global selected_rows
    selected_rows = []

    def get_index(e):
        global selected_rows
        row = e.control
        name = row.cells[0].content.text

        if row.selected:
            row.selected = False
            row.style = None
            selected_rows = [r for r in selected_rows if r[0] != name]
        else:
            row.selected = True
            row.style = ft.TextStyle(bgcolor="yellow")
            selected_rows.append([name, row])

        page.update()

    tabla1 = ft.DataTable(
        show_checkbox_column=True,
        sort_ascending=True,
        expand=False,
        data_row_max_height=float("inf"),
        width= 450,
        columns=[
            ft.DataColumn(
                ft.Text("Factura"),
                on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
            ),
            ft.DataColumn(
                ft.Text("Fecha de vencimiento"),
                on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
            ),
        ]
    )

    def abrir_archivo(nombre, tipo):
        if tipo == "no_facturadas":
            file_path = Path(direccion_carpeta) / "no_facturadas" / nombre
        else:
            file_path = Path(direccion_carpeta) / "facturadas" / nombre

        if os.path.exists(file_path):
            try:
                if platform.system() == 'Windows':
                    os.startfile(file_path)  # Para Windows
                elif platform.system() == 'Darwin':  # macOS
                    subprocess.run(['open', file_path])
                else:  # Linux
                    subprocess.run(['xdg-open', file_path])
            except Exception as e:
                print(f"No se pudo abrir el archivo: {e}")
        else:
            print(f"El archivo {file_path} no existe.")

    def calcular_dias_restantes(fecha_mod):
        if isinstance(fecha_mod, str):
            fecha_obj = datetime.datetime.strptime(fecha_mod, "%Y-%m-%d %H:%M:%S")
        else:
            fecha_obj = fecha_mod
        fecha_actual = datetime.datetime.now()
        diferencia = fecha_obj - fecha_actual
        return abs(diferencia.days)

    def determinar_color_fila(dias_restantes):
        if dias_restantes >= 180:
            return "blue"
        elif dias_restantes >= 30:
            return "green"
        elif dias_restantes >= 7:
            return "yellow"
        elif dias_restantes >= 1:
            return "red"
        else:
            return "red"

    def cargar_tabla_1(nombre, fecha_mod):
        dias_restantes = calcular_dias_restantes(fecha_mod)
        color_fila = determinar_color_fila(dias_restantes)

        tabla1.rows.append(
            ft.DataRow(
                on_select_changed=get_index,
                cells=[
                    ft.DataCell(ft.TextButton(
                        text=nombre, 
                        on_click=lambda e: abrir_archivo(nombre, "no_facturadas"),
                    )),
                    ft.DataCell(ft.Text(fecha_mod,))  # Permitir que el texto se ajuste
                ],
                color=color_fila,
            )
        )
        try:
            tabla1.update()
        except Exception as e:
            print(f"Error al actualizar las tablas: {e}")

    tabla2 = ft.DataTable(
        sort_ascending=True,
        show_checkbox_column=True,
        data_row_max_height=float("inf"),
        expand=False,
        width= 450,
        columns=[
            ft.DataColumn(
                ft.Text("Factura"),
                on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
            ),
            ft.DataColumn(
                ft.Text("Fecha de vencimiento"),
                on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
            ),
        ]
    )

    def cargar_tabla_2(nombre, fecha_mod):
        tabla2.rows.append(
            ft.DataRow(
                on_select_changed=get_index,
                cells=[
                    ft.DataCell(ft.TextButton(
                        text=nombre, 
                        on_click=lambda e: abrir_archivo(nombre, "facturadas"),
                    )),
                    ft.DataCell(ft.Text(fecha_mod))  # Permitir que el texto se ajuste
                ],
            ),
        )
        try:
            tabla2.update()
        except Exception as e:
            print(f"Error 2 al actualizar las tablas: {e}")

    titulo_tabla_1 = ft.Text(value="No Facturadas", size=35, weight=ft.FontWeight.BOLD)
    titulo_tabla_2 = ft.Text(value="Facturadas", size=35, weight=ft.FontWeight.BOLD)

    with open(Path(direccion_carpeta) / "registro.csv", mode="r") as archivo:
        reader = csv.reader(archivo)
        for fila in reader:
            if fila[0] != "nombre_factura":
                facturado = fila[2] == 'True'  # Convertir cadena a booleano
                if not facturado:
                    cargar_tabla_1(fila[0], fila[1])
                else:
                    cargar_tabla_2(fila[0], fila[1])

    def mover_archivo(nombre_archivo, origen, destino):
        origen_archivo = Path(origen) / nombre_archivo
        destino_archivo = Path(destino) / nombre_archivo
        shutil.move(origen_archivo, destino_archivo)

    def mover_factura(nombre_factura, direccion):
        updated_rows = []
        with open(Path(direccion_carpeta) / "registro.csv", mode='r') as file:
            reader = csv.reader(file)
            for fila in reader:
                if fila[0] == nombre_factura:
                    fila[2] = 'False' if direccion == 'izquierda' else 'True'
                updated_rows.append(fila)

        with open(Path(direccion_carpeta) / "registro.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_rows)

        origen = direccion_carpeta + '/facturadas' if direccion == 'izquierda' else direccion_carpeta + '/no_facturadas'
        destino = direccion_carpeta + '/no_facturadas' if direccion == 'izquierda' else direccion_carpeta + '/facturadas'
        mover_archivo(nombre_factura, origen, destino)

    def mover_facturas_seleccionadas(direccion):
        global selected_rows
        for row in selected_rows:
            nombre_factura = row[0]
            mover_factura(nombre_factura, direccion)
        cargar_tablas()
        selected_rows = []

    def eliminar_facturas_seleccionadas(e):
        global selected_rows
        for row in selected_rows:
            nombre_factura = row[0]
            ruta_archivo_no_facturadas = Path(direccion_carpeta) / "no_facturadas" / nombre_factura
            ruta_archivo_facturadas = Path(direccion_carpeta) / "facturadas" / nombre_factura
            if ruta_archivo_no_facturadas.exists():
                os.remove(ruta_archivo_no_facturadas)
            if ruta_archivo_facturadas.exists():
                os.remove(ruta_archivo_facturadas)
            eliminar_registro_csv(nombre_factura)
        cargar_tablas()
        selected_rows = []
    
    def eliminar_registro_csv(nombre_archivo):
        registros = []
        archivo_registro = os.path.join(direccion_carpeta, "registro.csv")
        
        # Leer todos los registros del CSV
        with open(archivo_registro, mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] != nombre_archivo:
                    registros.append(row)
        
        # Sobrescribir el CSV sin el registro eliminado
        with open(archivo_registro, mode="w", newline='') as file:
            writer = csv.writer(file)
            writer.writerows(registros)
        cargar_tablas()
        page.update()

    def cargar_tablas():
        global selected_rows
        selected_rows = []
        tabla1.rows.clear()
        tabla2.rows.clear()
        with open(Path(direccion_carpeta) / "registro.csv", mode="r") as archivo:
            reader = csv.reader(archivo)
            for fila in reader:
                if fila[0] != "nombre_factura":
                    facturado = fila[2] == 'True'  # Convertir cadena a booleano
                    if not facturado:
                        cargar_tabla_1(fila[0], fila[1])
                    else:
                        cargar_tabla_2(fila[0], fila[1])

    def on_dialog_result(e):
        open_dlg_fecha(e, e.files, direccion1)

    filepicker = ft.FilePicker(on_result=on_dialog_result)
    page.overlay.append(filepicker)
    page.update()

    def files_p(direccion):
        global direccion1
        direccion1 = direccion
        filepicker.pick_files(allow_multiple=True)

    # Crear los botones de flechas
    boton_izquierda = ft.ElevatedButton(text="Mover a la izquierda", icon=ft.icons.ARROW_LEFT, on_click=lambda event: mover_facturas_seleccionadas('izquierda'))
    boton_derecha = ft.ElevatedButton(text="Mover a la derecha", icon=ft.icons.ARROW_RIGHT, on_click=lambda event: mover_facturas_seleccionadas('derecha'))

    # Crear botón de eliminación
    boton_eliminar = ft.ElevatedButton(text="Eliminar Facturas Seleccionadas", on_click=eliminar_facturas_seleccionadas)

    # Crear botones de "Añadir elemento"
    boton_agregar_tabla_1 = ft.ElevatedButton(text="Crear Factura no facturada", on_click=open_dlg_modal)
    boton_agregar_tabla_2 = ft.ElevatedButton(text="Crear Factura facturada", on_click=open_dlg_modal_2)

    # Crear botones cargar archivos
    boton_agregar_archivos1 = ft.ElevatedButton(text="Cargar archivos", on_click=lambda event: files_p("/no_facturadas"))
    boton_agregar_archivos2 = ft.ElevatedButton(text="Cargar archivos", on_click=lambda event: files_p("/facturadas"))

    fila_tabla_1 = ft.Column(
        controls=[tabla1],
        scroll=ft.ScrollMode.ALWAYS,
        height=350,
    )

    fila_tabla_2 = ft.Column(
        controls=[tabla2],
        scroll=ft.ScrollMode.ALWAYS,
        height=350,
    )

    # Crear filas para las tablas y botones
    fila_boton_tabla_1 = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[titulo_tabla_1, fila_tabla_1, boton_agregar_tabla_1, boton_agregar_archivos1])

    fila_boton_tabla_2 = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[titulo_tabla_2, fila_tabla_2, boton_agregar_tabla_2, boton_agregar_archivos2])

    # Modificar la fila para incluir los botones
    fila = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=100,
        width='90%',
        height='auto',
        controls=[
            fila_boton_tabla_1,
            ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER,controls=[boton_izquierda, boton_derecha, boton_eliminar]),
            fila_boton_tabla_2
        ],
    )

    legend = ft.Row(
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(width=20, height=20, bgcolor="blue"),
            ft.Text(" 6 meses o más "),
            ft.Container(width=20, height=20, bgcolor="green"),
            ft.Text(" menos de 6 meses "),
            ft.Container(width=20, height=20, bgcolor="yellow"),
            ft.Text(" menos de un mes "),
            ft.Container(width=20, height=20, bgcolor="red"),
            ft.Text(" menos de una semana ")
        ]
    )

    respuesta = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Row(alignment=ft.MainAxisAlignment.CENTER,controls=[search_field, date_field_text, date_button, clear_date_button]),
            fila,
            legend
        ],
        alignment=ft.alignment.center
    )

    page.update()

    return respuesta
