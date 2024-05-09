import flet as ft

class UI(ft.Component):
    pass

def main(page: ft.Page):
    page.window_min_height=600
    page.window_min_width=800
    page.theme_mode=ft.ThemeMode.LIGHT
    page.title = "EasyBill"
    page.add(UI(page))


ft.app(main)