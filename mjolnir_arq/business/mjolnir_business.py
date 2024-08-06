import os
from typing import Any
from termcolor import colored
from sqlalchemy import BOOLEAN, TIMESTAMP, UUID, VARCHAR
from InquirerPy import inquirer
from mjolnir_arq.core.databases.connection_postgresql import ConnectionPostgresql
from mjolnir_arq.core.methods.methods import snake_to_pascal
from mjolnir_arq.core.models.directory_manager import DirectoryManager
from mjolnir_arq.core.models.file_manager import FileManager
from mjolnir_arq.core.models.login_db import LoginDB
import pyfiglet


def check_folder_exists_os(folder_path):
    return os.path.isdir(folder_path)


def get_current_directory():
    return os.getcwd()


class MjolnirBusiness:

    def __init__(self) -> None:
        self.db = None
        self.current_directory = get_current_directory()
        self.directory_manager = DirectoryManager()
        self.file_manager = FileManager()

    def data_connection_db(self):
        """name_db = inquirer.text(
            message="Introduce nombre de la base de datos:"
        ).execute()
        name_user = inquirer.text(message="Introduce nombre de usuario:").execute()
        password = inquirer.text(message="Introduce la contraseña:").execute()
        port = inquirer.text(message="Introduce el puerto:").execute()
        host = inquirer.text(message="Introduce host:").execute()"""

        return LoginDB(
            name_db="platform_qa",
            name_user="postgres",
            password="marlon",
            port="5432",
            host="localhost",
        )

    def create_flow_base(self):
        self.db = ConnectionPostgresql(loginDB=self.data_connection_db())
        name_table = inquirer.text(message="Introduce nombre de la tabla:").execute()

        result = self.validate_name_table(name_table=name_table)
        if not result:
            return

        result = self.domain_models_entities(name_table=name_table)
        if not result:
            return

    def domain_models_entities(self, name_table: str):
        result = self.directory_exists_entities(name_table=name_table)
        if not result:
            return False
        self.create_directory_entity(name_table=name_table)

        entity_base = self.create_entity_base(name_table=name_table)
        self.file_manager.create_file(
            file_path=f"{self.current_directory}/src/domain/models/entities/{name_table}/{name_table}.py",
            content=entity_base,
        )
        entity_save = self.create_entity_save(name_table=name_table)
        self.file_manager.create_file(
            file_path=f"{self.current_directory}/src/domain/models/entities/{name_table}/{name_table}_save.py",
            content=entity_save,
        )
        entity_read = self.create_entity_read(name_table=name_table)
        self.file_manager.create_file(
            file_path=f"{self.current_directory}/src/domain/models/entities/{name_table}/{name_table}_read.py",
            content=entity_read,
        )
        entity_delete = self.create_entity_delete(name_table=name_table)
        self.file_manager.create_file(
            file_path=f"{self.current_directory}/src/domain/models/entities/{name_table}/{name_table}_delete.py",
            content=entity_delete,
        )
        entity_update = self.create_entity_update(name_table=name_table)
        self.file_manager.create_file(
            file_path=f"{self.current_directory}/src/domain/models/entities/{name_table}/{name_table}_update.py",
            content=entity_update,
        )
        self.file_manager.create_file(
            file_path=f"{self.current_directory}/src/domain/models/entities/{name_table}/__init__.py"
        )

        return True

    def validate_name_table(self, name_table: str):
        table_names = self.db.inspector.get_table_names()
        if not name_table in table_names:
            print(
                colored(
                    "ERROR: 000 Ejecución no completada - nombre de la tabla no existe",
                    "light_red",
                )
            )
            return False
        return True

    def directory_exists_entities(self, name_table: str):
        folder_path = (
            f"{self.current_directory}/src/domain/models/entities/{name_table}"
        )
        directory_exists = self.directory_manager.directory_exists(dir_path=folder_path)

        if directory_exists:
            print(
                colored(
                    "ERROR: 001 Ejecución no completada - base ya existe en la arquitectura",
                    "light_red",
                )
            )
            return False
        return True

    def create_directory_entity(self, name_table: str):
        folder_path = (
            f"{self.current_directory}/src/domain/models/entities/{name_table}"
        )
        self.directory_manager.create_directory(dir_path=folder_path)

    def create_entity_base(self, name_table: str):
        model_code = f"from pydantic import BaseModel, Field, UUID4\n"
        model_code += f"from typing import Optional\n"
        model_code += f"from datetime import datetime\n\n"
        model_code += f"class {snake_to_pascal(snake_str=name_table)}(BaseModel):\n"
        columns = self.db.inspector.get_columns(name_table)
        for column in columns:
            name = column["name"]
            column_type = column["type"]
            nullable = column["nullable"]
            default = column.get("default")

            model_code += f"    {name}: {self.create_fields(column_type=column_type, name=name, nullable=nullable, default=default)}\n"

        model_code += f"\n"
        model_code += "    def dict(self, *args, **kwargs):\n"
        model_code += '        exclude = kwargs.pop("exclude", set())\n'
        model_code += '        exclude.update({"created_date", "updated_date"})\n'
        model_code += (
            "        return super().model_dump(*args, exclude=exclude, **kwargs)\n"
        )

        return model_code

    def create_entity_save(self, name_table: str):
        model_code = f"from pydantic import BaseModel, Field, UUID4\n"
        model_code += f"from typing import Optional\n"
        model_code += f"from datetime import datetime\n\n"
        model_code += f"class {snake_to_pascal(snake_str=name_table)}Save(BaseModel):\n"
        columns = self.db.inspector.get_columns(name_table)
        for column in columns:
            name = column["name"]
            column_type = column["type"]
            nullable = column["nullable"]
            default = column.get("default")

            exclude_fields = ["id", "created_date", "updated_date"]

            if not name in exclude_fields:
                model_code += f"    {name}: {self.create_fields(column_type=column_type, name=name, nullable=nullable, default=default)}\n"

        return model_code

    def create_entity_update(self, name_table: str):
        model_code = f"from pydantic import BaseModel, Field, UUID4\n"
        model_code += f"from typing import Optional\n"
        model_code += f"from datetime import datetime\n\n"
        model_code += (
            f"class {snake_to_pascal(snake_str=name_table)}Update(BaseModel):\n"
        )
        columns = self.db.inspector.get_columns(name_table)
        for column in columns:
            name = column["name"]
            column_type = column["type"]
            nullable = column["nullable"]
            default = column.get("default")

            exclude_fields = ["created_date", "updated_date"]

            if not name in exclude_fields:
                model_code += f"    {name}: {self.create_fields_update(column_type=column_type, name=name, nullable=nullable, default=default)}\n"

        return model_code

    def create_entity_read(self, name_table: str):
        model_code = (
            f"from pydantic import UUID4, BaseModel, field_validator, Field\n\n"
        )
        model_code += f"class {snake_to_pascal(snake_str=name_table)}Read(BaseModel):\n"
        model_code += f"    id: UUID4 = Field(...)\n"

        return model_code

    def create_entity_delete(self, name_table: str):
        model_code = (
            f"from pydantic import UUID4, BaseModel, field_validator, Field\n\n"
        )
        model_code += (
            f"class {snake_to_pascal(snake_str=name_table)}Delete(BaseModel):\n"
        )
        model_code += f"    id: UUID4 = Field(...)\n"

        return model_code

    def create_fields(self, column_type: Any, name: Any, nullable: Any, default: Any):
        if isinstance(column_type, UUID):
            field_type = "Optional[UUID4]"
            field_default = "Field(default=None)"
        elif isinstance(column_type, VARCHAR):
            field_type = "Optional[str]" if nullable else "str"
            max_length = column_type.length
            if nullable:
                field_default = f"Field(default=None, max_length={max_length})"
            else:
                field_default = f"Field(..., max_length={max_length})"
        elif isinstance(column_type, BOOLEAN):
            field_type = "bool"
            field_default = f"Field(default={default == 'true'})"
        elif isinstance(column_type, TIMESTAMP):
            field_type = "Optional[datetime]"
            field_default = "Field(default_factory=datetime.now)"
        else:
            field_type = "str"
            field_default = "Field(default=None)"

        return f"{field_type} = {field_default}"

    def create_fields_update(
        self, column_type: Any, name: Any, nullable: Any, default: Any
    ):
        if isinstance(column_type, UUID):
            field_type = "UUID4"
            field_default = "Field(...)"
        elif isinstance(column_type, VARCHAR):
            field_type = "Optional[str]" if nullable else "str"
            max_length = column_type.length
            if nullable:
                field_default = f"Field(default=None, max_length={max_length})"
            else:
                field_default = f"Field(..., max_length={max_length})"
        elif isinstance(column_type, BOOLEAN):
            field_type = "bool"
            field_default = f"Field(default={default == 'true'})"
        elif isinstance(column_type, TIMESTAMP):
            field_type = "Optional[datetime]"
            field_default = "Field(default_factory=datetime.now)"
        else:
            field_type = "str"
            field_default = "Field(default=None)"

        return f"{field_type} = {field_default}"
