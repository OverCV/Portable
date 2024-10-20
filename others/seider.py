import flet as ft
from flet import TextStyle
import random

def main(page: ft.Page):
    # Tu nombre y apellidos
    nombre = "Seider"
    apellido1 = "Sanin"
    apellido2 = "Giraldo"
    
    # Texto que mostrará tu nombre completo
    nombre_completo = ft.Text(f"{nombre} {apellido1}")

    # Función que alterna entre los apellidos
    def alternar_apellido(_):
        if nombre_completo.value == f"{nombre} {apellido1}":
            nombre_completo.value = f"{nombre} {apellido2}"
        else:
            nombre_completo.value = f"{nombre} {apellido1}"
        # Necesitamos actualizar el texto en pantalla
        nombre_completo.update()

    # Botón que permite alternar entre los apellidos
    boton_alternar = ft.ElevatedButton("Cambiar Apellido", on_click=alternar_apellido)

    # Lista de notas
    notas = ft.Column()

    # Función para añadir una nueva nota
    def add_note(_):
        note_text = note_input.value
        if note_text:
            note = ft.Row([
                ft.Checkbox(on_change=toggle_note),
                ft.Text(note_text)
            ])
            notas.controls.append(note)
            note_input.value = ""
            note_input.update()
            notas.update()

    # Función para cambiar el color de la nota
    def toggle_note(e):
        checkbox = e.control
        note_text = checkbox.parent.controls[1]
        if checkbox.value:
            random_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            new_note_text = ft.Text(note_text.value, style=TextStyle(color=random_color))
        else:
            new_note_text = ft.Text(note_text.value, style=TextStyle(color="white"))
        checkbox.parent.controls[1] = new_note_text
        checkbox.parent.update()

    # Barra de entrada de notas
    note_input = ft.TextField(hint_text="Escribe una nota")

    # Botón para añadir notas
    add_note_button = ft.ElevatedButton("Agregar Nota", on_click=add_note)

    # Agregar el texto, el botón y la sección de notas a la página
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    nombre_completo,  # Muestra el nombre
                    boton_alternar,   # Botón para alternar
                    note_input,       # Barra de entrada de notas
                    add_note_button,  # Botón para añadir notas
                    notas             # Lista de notas
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # Alinear al centro verticalmente
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Alinear al centro horizontalmente
            ),
            alignment=ft.alignment.center,  # Alinear el contenedor al centro
            expand=True
        )
    )

    # Asegurarse de que la página esté centrada verticalmente
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

# Ejecutar la app
ft.app(target=main)