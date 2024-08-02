import pyfiglet
from InquirerPy import inquirer
from termcolor import colored

def show_title():
    title = pyfiglet.figlet_format("MJOLNIR-ARQ")
    title = colored(title, 'cyan')
    print(colored(".", 'cyan') * 100)
    print(title)
    print(colored("mjolnir-arq: 0.0.4", 'cyan'))
    print(colored("Python: 3.11", 'cyan'))
    print(colored("Author: Marlon Andres Leon Leon", 'cyan'))
    print(colored(".", 'cyan') * 100)

def option1():
    name = inquirer.text(message="Introduce tu nombre:").execute()
    print(f"Has introducido: {name}")


def main():
    show_title()
    options = ["Opción 1", "Opción 2", "Opción 3", "Salir"]

    selected_option = inquirer.select(
        message="Seleccione una opción:",
        choices=options,
        default=options[0],
    ).execute()

    if selected_option == "Opción 1":
        option1()
    elif selected_option == "Opción 2":
        print("Has seleccionado la Opción 2.")
    elif selected_option == "Opción 3":
        print("Has seleccionado la Opción 3.")
    elif selected_option == "Salir":
        print("Saliendo...")


if __name__ == "__main__":
    main()
