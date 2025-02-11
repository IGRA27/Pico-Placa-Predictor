# flet_ui/counter.py
import flet as ft
import datetime
import sys
import os

#Ajusto el path para poder importar el módulo de 'src'
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.predictor import PicoPlacaPredictor

def main(page: ft.Page):
    page.title = "Pico y Placa Predictor"
    page.padding = 20
    page.scroll = "adaptive"
    #centro el contenido en la pantalla
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    #instanciar el predictor
    predictor = PicoPlacaPredictor()

    #campos de entrada con mayor tamaño
    txt_plate = ft.TextField(
        label="Número de placa (ej. PBX-1234)",
        width=400,
        text_size=18
    )
    txt_date = ft.TextField(
        label="Fecha (YYYY-MM-DD)",
        width=400,
        text_size=18
    )
    txt_time = ft.TextField(
        label="Hora (HH:MM)",
        width=400,
        text_size=18
    )

    #textos para mostrar mensajes de resultado y error
    result_text = ft.Text(value="", size=20)
    error_text = ft.Text(value="", color="red", size=18)

    def submit_click(e):
        #Reiniciar mensajes
        error_text.value = ""
        result_text.value = ""

        plate = txt_plate.value.strip()
        date_str = txt_date.value.strip()
        time_str = txt_time.value.strip()

        errors = []

        #Validar formato de fecha
        try:
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            errors.append(f"La fecha '{date_str}' no cumple con el formato YYYY-MM-DD.")

        #validar formato de hora
        try:
            hour, minute = map(int, time_str.split(':'))
            datetime.time(hour, minute)
        except ValueError:
            errors.append(f"La hora '{time_str}' no cumple con el formato HH:MM.")

        if errors:
            error_text.value = "\n".join(errors)
            page.update()
            return

        try:
            #llamo a la lógica del predictor
            can_drive = predictor.can_circulate(plate, date_str, time_str)
            if can_drive:
                result_text.value = f"El vehículo con placa {plate} SÍ puede circular."
                result_text.color = "green"
            else:
                result_text.value = f"El vehículo con placa {plate} NO puede circular."
                result_text.color = "red"
        except Exception as ex:
            error_text.value = str(ex)
        page.update()

    submit_button = ft.ElevatedButton(
        text="Verificar",
        on_click=submit_click,
        height=50,
        width=200,
        style=ft.ButtonStyle(
            #uso RoundedRectangleBorder porque lo anterior no me funcionaba que era round
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )

    #organizo todos los controles en una columna centrada
    content_column = ft.Column(
        [
            ft.Text("Pico y Placa Predictor", size=32, weight="bold"),
            txt_plate,
            txt_date,
            txt_time,
            submit_button,
            error_text,
            result_text,
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    #envuelvo la columna en un contenedor que ocupe el espacio disponible y se centre
    container = ft.Container(
        content=content_column,
        alignment=ft.alignment.center,
        expand=True,
    )

    page.add(container)

#ejecuto la aplicación Flet en modo web.
ft.app(target=main, view=ft.WEB_BROWSER)
