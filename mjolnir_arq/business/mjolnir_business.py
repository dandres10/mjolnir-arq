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

        result = self.domain_services_repositories_entities(name_table=name_table)
        if not result:
            return

    def domain_models_entities(self, name_table: str) -> bool:
        base_path = os.path.join(
            self.current_directory, "src", "domain", "models", "entities", name_table
        )
        if not self.directory_exists(folder_path=base_path):
            return False
        print(base_path)
        self.directory_manager.create_directory(dir_path=base_path)

        file_contents: dict[str, str] = {
            f"{name_table}.py": self.create_entity_base(name_table=name_table),
            f"{name_table}_save.py": self.create_entity_save(name_table=name_table),
            f"{name_table}_read.py": self.create_entity_read(name_table=name_table),
            f"{name_table}_delete.py": self.create_entity_delete(name_table=name_table),
            f"{name_table}_update.py": self.create_entity_update(name_table=name_table),
            "__init__.py": "",
        }

        for file_name, content in file_contents.items():
            file_path = os.path.join(base_path, file_name)
            self.file_manager.create_file(file_path=file_path, content=content)

        return True

    def domain_services_repositories_entities(self, name_table: str) -> bool:
        base_path = os.path.join(
            self.current_directory,
            "src",
            "domain",
            "services",
            "repositories",
            "entities",
        )
        if not self.file_exists(file_path=f"{base_path}/i_{name_table}_repository.py"):
            return False

        file_contents: dict[str, str] = {
            f"i_{name_table}_repository.py": self.create_domain_services_repositories_entities(
                name_table=name_table
            )
        }

        for file_name, content in file_contents.items():
            file_path = os.path.join(base_path, file_name)
            self.file_manager.create_file(file_path=file_path, content=content)

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

    def directory_exists(self, folder_path: str):

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

    def file_exists(self, file_path: str):

        directory_exists = self.file_manager.file_exists(file_path=file_path)

        if directory_exists:
            print(
                colored(
                    f"ERROR: 002 Ejecución no completada - archivo {file_path} ya existe en la arquitectura",
                    "light_red",
                )
            )
            return False
        return True

    def create_directory(self, folder_path: str):
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

    def create_domain_services_repositories_entities(self, name_table: str):
        pascal_name_table = snake_to_pascal(snake_str=name_table)

        model_code = f"""
from typing import List, Union
from abc import ABC, abstractmethod

from src.core.models.config import Config
from src.core.models.filter import Pagination
from src.domain.models.entities.{name_table}.{name_table} import {pascal_name_table}
from src.domain.models.entities.{name_table}.{name_table}_delete import {pascal_name_table}Delete
from src.domain.models.entities.{name_table}.{name_table}_read import {pascal_name_table}Read
from src.domain.models.entities.{name_table}.{name_table}_update import {pascal_name_table}Update
from src.infrastructure.database.entities.{name_table}_entity import {pascal_name_table}Entity


class I{pascal_name_table}Repository(ABC):
    @abstractmethod
    def save(
        self,
        config: Config,
        params: {pascal_name_table}Entity,
    ) -> Union[{pascal_name_table}, None]:
        pass

    @abstractmethod
    def update(
        self,
        config: Config,
        params: {pascal_name_table}Update,
    ) -> Union[{pascal_name_table}, None]:
        pass

    @abstractmethod
    def list(
        self,
        config: Config,
        params: Pagination,
    ) -> Union[List[{pascal_name_table}], None]:
        pass

    @abstractmethod
    def delete(
        self,
        config: Config,
        params: {pascal_name_table}Delete,
    ) -> Union[{pascal_name_table}, None]:
        pass

    @abstractmethod
    def read(
        self,
        config: Config,
        params: {pascal_name_table}Read,
    ) -> Union[{pascal_name_table}, None]:
        pass
        """

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
