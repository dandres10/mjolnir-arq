
from InquirerPy import inquirer

def main():
    options = [
        "Opción 1",
        "Opción 2",
        "Opción 3",
        "Salir"
    ]

    selected_option = inquirer.select(
        message="Seleccione una opción:",
        choices=options,
        default=options[0],
    ).execute()

    if selected_option == "Opción 1":
        print("Has seleccionado la Opción 1.")
    elif selected_option == "Opción 2":
        print("Has seleccionado la Opción 2.")
    elif selected_option == "Opción 3":
        print("Has seleccionado la Opción 3.")
    elif selected_option == "Salir":
        print("Saliendo...")


