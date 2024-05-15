import flet as ft

class UI(ft.UserControl):
    def __init__(self, page):
        super().__init__(expand=True)


def pantalla(page:ft.Page):
    new_page = page.open_window()
    new_page.window_min_height=600
    new_page.window_min_width=800
    new_page.theme_mode=ft.ThemeMode.LIGHT
    new_page.title = "EasyBill"
    new_page.add(UI(new_page))