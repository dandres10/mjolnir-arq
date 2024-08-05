import pyfiglet
from InquirerPy import inquirer
from termcolor import colored

from mjolnir_arq.core.models.login_db import LoginDB
from mjolnir_arq.controller.mjolnir_controller import MjolnirController


def show_title():
    title = pyfiglet.figlet_format("MJOLNIR-ARQ")
    title = colored(title, "cyan")
    print(colored(".", "cyan") * 100)
    print(title)
    print(colored("mjolnir-arq: 0.0.4", "cyan"))
    print(colored("Python: 3.11", "cyan"))
    print(colored("Author: Marlon Andres Leon Leon", "cyan"))
    print(colored(".", "cyan") * 100)


def create_flow_base():
    """ name_db = inquirer.text(message="Introduce nombre de la base de datos:").execute()
    name_user = inquirer.text(message="Introduce nombre de usuario:").execute()
    password = inquirer.text(message="Introduce la contraseña:").execute()
    port = inquirer.text(message="Introduce el puerto:").execute()
    host = inquirer.text(message="Introduce host:").execute() """
    mjolnirController = MjolnirController(
        loginDB=LoginDB(
            name_db="platform_qa",
            name_user="postgres",
            password="marlon",
            port="5432",
            host="localhost",
        )
    )
    name_table = inquirer.text(message="Introduce nombre de la tabla:").execute()
    mjolnirController.create_flow_base(name_table)


def main():
    show_title()
    options = ["Crear flujo base", "Opción 2", "Opción 3", "Salir"]

    selected_option = inquirer.select(
        message="Seleccione una opción:",
        choices=options,
        default=options[0],
    ).execute()

    if selected_option == "Crear flujo base":
        create_flow_base()
    elif selected_option == "Opción 2":
        print("Has seleccionado la Opción 2.")
    elif selected_option == "Opción 3":
        print("Has seleccionado la Opción 3.")
    elif selected_option == "Salir":
        print("Saliendo...")


if __name__ == "__main__":
    main()
