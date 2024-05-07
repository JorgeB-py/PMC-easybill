import flet as ft

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
        self.navigation_bar=ft.Container(
            expand=True,
            content=ft.ResponsiveRow(
                expand=True,
                controls=[
                    ft.Container(
                        border_radius=10,
                        expand=False,
                        height=50,
                        padding=10,
                        bgcolor='black',
                        content=ft.Row(
                            expand=True,
                            height=50,
                            alignment=ft.MainAxisAlignment.END,
                            controls=[
                                ft.IconButton(
                                    icon=ft.icons.NOTIFICATIONS_ACTIVE,
                                    icon_color='yellow',
                                ),
                                ft.IconButton(
                                    icon=ft.icons.PERSON,
                                    icon_color='white',
                                ),
                                ft.Text('PERSONA', color='white'),
                            ]
                        )
                    ),
                    ft.Container(
            padding=200,
            content=ft.DataTable(
            width=800,
            bgcolor='white',
            border=ft.border.all(1, 'black'),
            border_radius=10,
            horizontal_lines=ft.border.BorderSide(1, 'black'),
            sort_ascending=True,
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
        )
                ]
            )
        )
        self.add_button = ft.ElevatedButton(
            text="Agregar empresa",
            on_click=self.open_dialog,  # Evento que se dispara cuando se hace clic en el botón
        )

        self.container = ft.Column(
            controls=[self.navigation_bar, self.add_button, self.dialog],
        )
    def open_dialog(self, event):
        self.page.dialog=self.dialog
        self.dialog.open=True  # Muestra el cuadro de diálogo
        self.page.update()
    def dialog_close(self, event):
        self.dialog.open=False  # Oculta el cuadro de diálogo
        self.page.update()

    def save_name(self, event):
        self.company_name = event.data  # Guarda el nombre de la empresa

    def add_company(self, event):
        self.navigation_bar.content.controls[1].content.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(self.company_name)),
                    ft.DataCell(ft.IconButton(icon=ft.icons.EDIT)),
                    ft.DataCell(ft.IconButton(icon=ft.icons.DELETE)),
                    ft.DataCell(ft.IconButton(icon=ft.icons.VISIBILITY)),
                ]
            )
        )
        self.navigation_bar.content.controls[1].content.update()

    def build(self):
        return self.container

def main(page: ft.Page):
    page.window_min_height=600
    page.window_min_width=800
    page.theme_mode=ft.ThemeMode.LIGHT
    page.add(UI(page))


ft.app(main)
