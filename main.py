import flet as ft
import pantalla_facturas as pf

class UI(ft.UserControl):
    def __init__(self, page):
        super().__init__(expand=True)
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
        
        self.lista_empresas=[]

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
    def go_facturas(self, e):
        self.page.route="/facturas"
        self.page.update()
    
    def route_change(self, route):
        self.page.views.clear()
        self.page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Flet app"), bgcolor=ft.colors.SURFACE_VARIANT),
                    ft.ElevatedButton("Visit Store", on_click=lambda _: self.page.go("/store")),
                ],
            )
        )
        if self.page.route == "/store":
            self.page.views.append(
                ft.View(
                    "/store",
                    [
                        ft.AppBar(title=ft.Text("Store"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go Home", on_click=lambda _: self.page.go("/")),
                    ],
                )
            )
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
            self.cargar_tabla(self.company_name)
            self.tablaDatos.update()
            self.dialog_close(event)

    def delete_company(self, event):
        company_name = event.control.parent.parent.cells[0].content.value
    # Get the company name from the first cell in the row
        self.lista_empresas.remove(company_name)
        self.tablaDatos.rows.clear()
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
        self.tablaDatos.update()
    def build(self):
        return self.container

def main(page: ft.Page):
    page.window_min_height=600
    page.window_min_width=800
    page.theme_mode=ft.ThemeMode.LIGHT
    page.title = "EasyBill"
    page.add(UI(page))


ft.app(main, view=ft.AppView.WEB_BROWSER)
