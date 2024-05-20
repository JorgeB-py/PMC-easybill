import flet as ft
import pantalla_facturas as pf
import repath as rp
import os
import csv

class UI(ft.UserControl):
    def __init__(self, page):
        super().__init__(expand=True)

        if not os.path.exists('EasyBill'):
            os.makedirs('EasyBill')
        
        if not os.path.isfile('EasyBill/empresas.csv'):
            with open('EasyBill/empresas.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Empresa", "Direccion"])
        self.dialog = ft.AlertDialog(  
            modal=True,  # Nuevo cuadro de diálogo
            content=ft.TextField(hint_text="Nombre de la empresa", on_change=self.save_name),  # Campo de texto para el nombre de la empresa
            actions=[
                ft.TextButton(text="Guardar", on_click=self.add_company),
                ft.TextButton(text="Cancelar", on_click=self.dialog_close)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.edit_dialog_a = ft.AlertDialog(  
            modal=True,  # Nuevo cuadro de diálogo
            visible=True,
            content=ft.TextField(hint_text="Nombre de la empresa", on_change=self.save_name),  # Campo de texto para el nombre de la empresa
            actions=[
                ft.TextButton(text="Guardar", on_click=self.update_company),
                ft.TextButton(text="Cancelar", on_click=self.dialog_close)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.searh_field = ft.TextField(                        
                            suffix_icon = ft.icons.SEARCH,
                            label= "Buscar por el nombre",
                            border= ft.InputBorder.UNDERLINE,
                            border_color= "white",
                            label_style = ft.TextStyle(color= "white"),
                            on_change = self.searh_data,
                        )
        self.dialogAlert = ft.AlertDialog(
                modal=True,
                visible=True,
                content=ft.Text("La empresa ya existe"),
                actions=[
                    ft.TextButton(text="Aceptar", on_click=self.dialog_close)
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
        
        self.lista_empresas=[] # Lista de empresas
        self.direcciones={} # Diccionario de empresas y sus direcciones

        with open('EasyBill/empresas.csv', 'r') as file:
            reader = csv.reader(file)
            i=0
            for row in reader:
                if i!=0: # Ignora la primera fila
                    self.direcciones[row[0]] = row[1]
                    self.lista_empresas.append(row[0])
                i+=1



        self.navigation_bar=ft.Container(
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
        self.tablaDatos=ft.DataTable(
            data_row_max_height=50,
            width=800,
            bgcolor='white',
            border=ft.border.all(1, 'black'),
            border_radius=10,
            horizontal_lines=ft.border.BorderSide(1, 'black'),
            sort_ascending=True,
            expand=True,
            columns=[
                ft.DataColumn(
                    ft.Text("Empresa"),
                    on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                ft.DataColumn(
                    ft.Text("Editar"),
                    tooltip="This is a third column",
                    on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                ft.DataColumn(
                    ft.Text("Borrar"),
                    tooltip="This is a fourth column",
                ),
                ft.DataColumn(
                    ft.Text("Ver"),
                    tooltip="This is a fifth column",
                ),
            ]
        )
        self.table = ft.Container(
            border_radius=10,
            padding= 10,
            col = 8,
            expand=True,
            content= ft.Column(   
                expand=True,           
                controls=[
                    ft.Container(
                        padding = 10,
                        content= ft.Row(
                            controls=[
                                self.searh_field,
                                ]
                            )
                        ),
                    ft.Column(
                        expand= True, 
                        scroll="auto",
                        controls=[
                        ft.ResponsiveRow([
                            self.tablaDatos
                            ]),
                        ]
                    ),
                ]
            )
        )
    
        self.searh_field = ft.TextField(                        
                            suffix_icon = ft.icons.SEARCH,
                            label= "Buscar por el nombre",
                            border= ft.InputBorder.UNDERLINE,
                            border_color= "white",
                            label_style = ft.TextStyle(color= "white"),
                            on_change = self.searh_data,
                        )
        
        self.buttom=ft.Container(
                        expand=False,
                        padding=10,
                        col=1,
                        content=ft.IconButton(
                            icon=ft.icons.ADD,
                            bgcolor="black",
                            icon_color="white",  # Icono del botón
                            on_click=self.open_dialog,  # Evento que se dispara cuando se hace clic en el botón
                        )
                    )

        self.container = ft.Column(
            controls=[self.navigation_bar, self.table, self.buttom],
        )
        if len(self.lista_empresas) > 0:
            for empresa in self.lista_empresas:
                self.cargar_tabla(empresa)
        self.page=page
        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop

    def go_home(self,e):
        self.page=e.page
        self.page.go("/")
    
    def go_facturas(self, event):
        self.page=event.page
        # Nombre de la empresa y dirección de la carpeta
        self.pantalla_facturas=pf.__view__(self.page, event.control.parent.parent.cells[0].content.value, self.direcciones[event.control.parent.parent.cells[0].content.value])
        self.page.go("/facturas")
    
    def route_change(self, route):
        self.page.views.clear()
        if self.page.route == "/facturas":
            self.page.views.clear()
            self.page.views.append(
                ft.View(
                    "/facturas",
                    [
                        ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=self.go_home),
                        self.pantalla_facturas, # Botón para regresar a la pantalla principal (descomentar al final)
                    ],
                )
            )
        else:
            self.page.views.append(ft.View(self.page.route, self.page.controls))
        self.page.update()

    def view_pop(self, view):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)

    def open_dialog(self, event):
        self.page.dialog=self.dialog
        self.dialog.open=True  # Muestra el cuadro de diálogo
        self.page.update()

    def edit_dialog(self, event):
        self.page.dialog=self.edit_dialog_a
        self.edit_dialog_a.open=True  # Muestra el cuadro de diálogo
        self.page.update()

    def dialog_close(self, event):
        self.dialog.open=False
        self.dialogAlert.open=False # Oculta el cuadro de diálogo
        self.edit_dialog_a.open=False
        self.page.update()

    def save_name(self, event):
        self.company_name = event.data  # Guarda el nombre de la empresa

    def add_company(self, event):
        if self.company_name in self.lista_empresas:
            self.dialog_close(event)
            self.company_name = ""
            self.page.dialog = self.dialogAlert
            self.dialogAlert.open = True
            self.page.update()
        else:
            self.lista_empresas.append(self.company_name)
            folder_path = 'EasyBill/' + self.company_name
            folder_facturadas = folder_path + '/facturadas'
            folder_no_facturadas = folder_path + '/no_facturadas'
        
            os.makedirs(folder_path)
            os.makedirs(folder_facturadas)
            os.makedirs(folder_no_facturadas)
        
            # Crear los archivos .csv y añadir las columnas
            facturadas_file = os.path.join(folder_path, 'facturadas.csv')
            no_facturadas_file = os.path.join(folder_path, 'no_facturadas.csv')
        
            with open(facturadas_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["nombre_factura", "fecha_limite"])
        
            with open(no_facturadas_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["nombre_factura", "fecha_limite"])

            self.direcciones[self.company_name] = folder_path
            with open('EasyBill/empresas.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([self.company_name, folder_path])
        
            self.cargar_tabla(self.company_name)
            self.tablaDatos.update()
            self.dialog_close(event)

    def delete_company(self, event):
        company_name = event.control.parent.parent.cells[0].content.value # Get the company name from the first cell in the row
        self.lista_empresas.remove(company_name)
        self.tablaDatos.rows.clear()
        with open('EasyBill/empresas.csv', 'r') as f:
            reader = csv.reader(f)
            data = list(reader)

    # Buscar la empresa y eliminarla
        data = [row for row in data if row[0] != company_name]

    # Escribir los datos de nuevo al archivo CSV
        with open('EasyBill/empresas.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)
            for empresa in self.lista_empresas:
                self.cargar_tabla(empresa)
            self.tablaDatos.update()
    
    def edit_company(self, event):
        self.old_company_name = event.control.parent.parent.cells[0].content.value

        # Muestra un cuadro de diálogo para editar el nombre de la empresa
        self.edit_dialog(event)

    def update_company(self, event):
        if self.company_name in self.lista_empresas:
            self.dialog_close(event)
            self.company_name = ""
            self.page.dialog = self.dialogAlert
            self.dialogAlert.open = True
            self.page.update()
        else:
            self.lista_empresas.remove(self.old_company_name)
            self.lista_empresas.append(self.company_name)
            self.direcciones.pop(self.old_company_name)
            folder_path = 'EasyBill/' + self.company_name
            os.rename('EasyBill/' + self.old_company_name, folder_path)
            self.direcciones[self.company_name] = folder_path
            with open('empresas.csv', 'r') as f:
                reader = csv.reader(f)
                data = list(reader)

    # Buscar la empresa y modificar sus datos
            for row in data:
                if row[0] == self.old_company_name:
                    row[0] = self.company_name
                    row[1] = folder_path
                    break

    # Escribir los datos de nuevo al archivo CSV
            with open('empresas.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(data)
            
            self.tablaDatos.rows.clear()
            for empresa in self.lista_empresas:
                self.cargar_tabla(empresa)
            self.tablaDatos.update()
            self.dialog_close(event)

    def searh_data(self, e):
            if len(e.data) == 0:
                self.tablaDatos.rows.clear()
                for empresa in self.lista_empresas:
                    self.cargar_tabla(empresa)
                self.tablaDatos.update()
            else:
                self.search = e.data.lower()
                self.tablaDatos.rows.clear()
                for empresa in self.lista_empresas:
                    if self.search == empresa.lower():
                        self.cargar_tabla(empresa)
                self.tablaDatos.update()
    def cargar_tabla(self,company_name):
        self.tablaDatos.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(company_name)),
                    ft.DataCell(ft.IconButton(icon=ft.icons.EDIT, on_click=lambda event: self.edit_company(event))),
                    ft.DataCell(ft.IconButton(icon=ft.icons.DELETE, on_click=lambda event: self.delete_company(event))),
                    ft.DataCell(ft.IconButton(icon=ft.icons.VISIBILITY, on_click=lambda event: self.go_facturas(event))),
                ]
            )
        )
        try:
            self.tablaDatos.update()
        except:
            pass

    def build(self):
        return self.container

def main(page: ft.Page):
    page.window_min_height=800
    page.window_min_width=1400
    page.theme_mode=ft.ThemeMode.LIGHT
    file_picker = ft.FilePicker()
    page.controls.append(file_picker)
    page.title = "EasyBill"
    page.add(UI(page))


ft.app(main)
