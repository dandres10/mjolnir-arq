
import pyfiglet
from InquirerPy import inquirer
from termcolor import colored
import os
from mjolnir_arq.business.mjolnir_business import MjolnirBusiness


def check_folder_exists_os(folder_path):
    return os.path.isdir(folder_path)


def get_current_directory():
    return os.getcwd()


class MjolnirController:
    def __init__(self) -> None:
        self.mjolnir_business = MjolnirBusiness()

    def show_title(self):
        title = pyfiglet.figlet_format("MJOLNIR-ARQ")
        title = colored(title, "cyan")
        print(colored(".", "cyan") * 100)
        print(title)
        print(colored("mjolnir-arq: 0.0.4", "cyan"))
        print(colored("Python: 3.11", "cyan"))
        print(colored("Author: Marlon Andres Leon Leon", "cyan"))
        print(colored(".", "cyan") * 100)

    def menu(self):
        self.show_title()
        options = ["Crear flujo base", "Opción 2", "Opción 3", "Salir"]

        selected_option = inquirer.select(
            message="Seleccione una opción:",
            choices=options,
            default=options[0],
        ).execute()

        if selected_option == "Crear flujo base":
            self.mjolnir_business.create_flow_base()
        elif selected_option == "Crear arquitectura inicial":
            print("Has seleccionado la Opción 2.")
        elif selected_option == "Crear flujo de negocio":
            print("Has seleccionado la Opción 3.")
        elif selected_option == "Salir":
            print("Saliendo...")
