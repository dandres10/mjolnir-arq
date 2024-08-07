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

        """ result = self.domain_models_entities(name_table=name_table)
        if not result:
            return

        result = self.domain_services_repositories_entities(name_table=name_table)
        if not result:
            return

        result = self.domain_services_use_cases_entities(name_table=name_table)
        if not result:
            return

        result = self.infrastructure_database_entities(name_table=name_table)
        if not result:
            return

        result = self.infrastructure_database_mappers(name_table=name_table)
        if not result:
            return """

        result = self.infrastructure_database_repositories(name_table=name_table)
        if not result:
            return

    def domain_models_entities(self, name_table: str) -> bool:
        base_path = os.path.join(
            self.current_directory, "src", "domain", "models", "entities", name_table
        )
        if not self.directory_exists(folder_path=base_path):
            return False
        self.directory_manager.create_directory(dir_path=base_path)

        file_contents: dict[str, str] = {
            f"{name_table}.py": self.create_entity_base(name_table=name_table),
            f"{name_table}_save.py": self.create_entity_save(name_table=name_table),
            f"{name_table}_read.py": self.create_entity_read(name_table=name_table),
            f"{name_table}_delete.py": self.create_entity_delete(name_table=name_table),
            f"{name_table}_update.py": self.create_entity_update(name_table=name_table),
            f"index.py": self.domain_models_entities_index(name_table=name_table),
            "__init__.py": "",
        }

        for file_name, content in file_contents.items():
            file_path = os.path.join(base_path, file_name)
            self.file_manager.create_file(file_path=file_path, content=content)

        return True

    def domain_models_entities_index(self, name_table: str):
        pascal_name_table = snake_to_pascal(snake_str=name_table)
        model_code = f"""
from .{name_table} import {pascal_name_table}
from .{name_table}_delete import {pascal_name_table}Delete
from .{name_table}_read import {pascal_name_table}Read
from .{name_table}_save import {pascal_name_table}Save
from .{name_table}_update import {pascal_name_table}Update

__all__ = [
    "{pascal_name_table}",
    "{pascal_name_table}Delete",
    "{pascal_name_table}Read",
    "{pascal_name_table}Save",
    "{pascal_name_table}Update",
]
        """
        return model_code

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

    def domain_services_use_cases_entities(self, name_table: str) -> bool:
        base_path = os.path.join(
            self.current_directory,
            "src",
            "domain",
            "services",
            "use_cases",
            "entities",
        )
        if not self.directory_exists(folder_path=f"{base_path}/{name_table}"):
            return False

        self.directory_manager.create_directory(dir_path=f"{base_path}/{name_table}")

        file_contents: dict[str, str] = {
            f"{name_table}_delete_use_case.py": self.create_domain_services_use_cases_entities_delete(
                name_table=name_table
            ),
            f"{name_table}_list_use_case.py": self.create_domain_services_use_cases_entities_list(
                name_table=name_table
            ),
            f"{name_table}_read_use_case.py": self.create_domain_services_use_cases_entities_read(
                name_table=name_table
            ),
            f"{name_table}_save_use_case.py": self.create_domain_services_use_cases_entities_save(
                name_table=name_table
            ),
            f"{name_table}_update_use_case.py": self.create_domain_services_use_cases_entities_update(
                name_table=name_table
            ),
            "index.py": self.create_domain_services_use_cases_entities_index(
                name_table=name_table
            ),
            "__init__.py": "",
        }

        for file_name, content in file_contents.items():
            file_path = os.path.join(f"{base_path}/{name_table}", file_name)
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

    def map_column_type(self, postgres_type):
        type_mapping = {
            "UUID": "UUID(as_uuid=True)",
            "VARCHAR": "String",
            "BOOLEAN": "Boolean",
            "TIMESTAMP": "DateTime",
            "INTEGER": "Integer",
            "FLOAT": "Float",
            "NUMERIC": "Float",
            "TEXT": "Text",
        }
        postgres_type_str = str(postgres_type)
        for postgres, sqlalchemy in type_mapping.items():
            if postgres in postgres_type_str:
                return postgres_type_str.replace(postgres, sqlalchemy)
        return postgres_type_str

    def infrastructure_database_repositories(self, name_table: str):
        pascal_name_table = snake_to_pascal(snake_str=name_table)
        base_path = os.path.join(
            self.current_directory, "src", "infrastructure", "database", "repositories"
        )
        if not self.file_exists(file_path=f"{base_path}/{name_table}_repository.py"):
            return False

        model_code = f"""
from typing import List, Union
from pydantic import UUID4
from src.core.config import settings
from src.core.enums.layer import LAYER
from src.core.methods.get_filter import get_filter
from src.core.models.config import Config
from src.core.models.filter import Pagination
from src.core.wrappers.execute_transaction import execute_transaction
from src.domain.models.entities.{name_table}.index import (
    {pascal_name_table},
    {pascal_name_table}Delete,
    {pascal_name_table}Read,
    {pascal_name_table}Update,
)
from src.domain.services.repositories.entities.i_{name_table}_repository import (
    I{pascal_name_table}Repository,
)
from src.infrastructure.database.entities.{name_table}_entity import {pascal_name_table}Entity
from src.infrastructure.database.mappers.{name_table}_mapper import (
    map_to_{name_table},
    map_to_list_{name_table},
)


class {pascal_name_table}Repository(I{pascal_name_table}Repository):

    def save(self, config: Config, params: {pascal_name_table}Entity) -> Union[{pascal_name_table}, None]:
        db = config.db
        db.add(params)
        db.commit()
        db.refresh(params)
        return map_to_{name_table}(params)

    def update(self, config: Config, params: {pascal_name_table}Update) -> Union[{pascal_name_table}, None]:
        db = config.db

        {name_table}: {pascal_name_table}Entity = (
            db.query({pascal_name_table}Entity).filter({pascal_name_table}Entity.id == params.id).first()
        )

        if not {name_table}:
            return None

        update_data = params.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr({name_table}, key, value)

        db.commit()
        db.refresh({name_table})
        return map_to_{name_table}({name_table})

    def list(self, config: Config, params: Pagination) -> Union[List[{pascal_name_table}], None]:
        db = config.db
        query = db.query({pascal_name_table}Entity)

        if params.all_data:
            {name_table}s = query.all()
        else:
            if params.filters:
                query = get_filter(
                    query=query, filters=params.filters, entity={pascal_name_table}Entity
                )
                {name_table}s = query.offset(params.skip).limit(params.limit).all()

        if not {name_table}s:
            return None
        return map_to_list_{name_table}({name_table}s)

    def delete(
        self,
        config: Config,
        params: {pascal_name_table}Delete,
    ) -> Union[{pascal_name_table}, None]:
        db = config.db
        {name_table}: {pascal_name_table}Entity = (
            db.query({pascal_name_table}Entity).filter({pascal_name_table}Entity.id == params.id).first()
        )

        if not {name_table}:
            return None

        db.delete({name_table})
        db.commit()
        return map_to_{name_table}({name_table})

    def read(
        self,
        config: Config,
        params: {pascal_name_table}Read,
    ) -> Union[{pascal_name_table}, None]:
        db = config.db
        {name_table}: {pascal_name_table}Entity = (
            db.query({pascal_name_table}Entity).filter({pascal_name_table}Entity.id == params.id).first()
        )

        if not {name_table}:
            return None

        return map_to_{name_table}({name_table})


if settings.has_track:
    {pascal_name_table}Repository.save = execute_transaction(LAYER.I_D_R.value)(
        {pascal_name_table}Repository.save
    )
    {pascal_name_table}Repository.update = execute_transaction(LAYER.I_D_R.value)(
        {pascal_name_table}Repository.update
    )
    {pascal_name_table}Repository.list = execute_transaction(LAYER.I_D_R.value)(
        {pascal_name_table}Repository.list
    )
    {pascal_name_table}Repository.delete = execute_transaction(LAYER.I_D_R.value)(
        LanguageRepository.delete
    )
    {pascal_name_table}Repository.read = execute_transaction(LAYER.I_D_R.value)(
        LanguageRepository.read
    )
        """

        file_contents: dict[str, str] = {f"{name_table}_repository.py": model_code}

        for file_name, content in file_contents.items():
            file_path = os.path.join(base_path, file_name)
            self.file_manager.create_file(file_path=file_path, content=content)

        return True

    def infrastructure_database_mappers(self, name_table: str):
        pascal_name_table = snake_to_pascal(snake_str=name_table)
        base_path = os.path.join(
            self.current_directory, "src", "infrastructure", "database", "mappers"
        )
        if not self.file_exists(file_path=f"{base_path}/{name_table}_mapper.py"):
            return False

        columns = self.db.inspector.get_columns(name_table)
        pascal_name_table = snake_to_pascal(name_table)
        fields = [col["name"] for col in columns]

        def generate_map_to_entity(pascal_name_table, fields):
            method = f"""
from typing import List
from src.domain.models.entities.{name_table}.index import (
    {pascal_name_table},
    {pascal_name_table}Save,
    {pascal_name_table}Update,
)
from src.infrastructure.database.entities.language_entity import LanguageEntity\n\n
"""
            method += f"def map_to_{name_table}({name_table}_entity: {pascal_name_table}Entity) -> {pascal_name_table}:\n"
            method += f"    return {pascal_name_table}(\n"
            for field in fields:
                method += (
                    f"        {field}={pascal_name_table.lower()}_entity.{field},\n"
                )
            method += f"    )\n\n"
            return method

        def generate_map_to_list_entity(pascal_name_table):
            method = f"def map_to_list_{name_table}({name_table}_entities: List[{pascal_name_table}Entity]) -> List[{pascal_name_table}]:\n"
            method += f"    return [map_to_{name_table}({name_table}) for {name_table} in {name_table}_entities]\n\n"
            return method

        def generate_map_to_entity_entity(pascal_name_table, fields):
            method = f"def map_to_{name_table}_entity({name_table}: {pascal_name_table}) -> {pascal_name_table}Entity:\n"
            method += f"    return {pascal_name_table}Entity(\n"
            for field in fields:
                method += f"        {field}={pascal_name_table.lower()}.{field},\n"
            method += f"    )\n\n"
            return method

        def generate_map_to_list_entity_entity(pascal_name_table):
            method = f"def map_to_list_{name_table}_entity({name_table}s: List[{pascal_name_table}]) -> List[{pascal_name_table}Entity]:\n"
            method += f"    return [map_to_{name_table}_entity({name_table}) for {name_table} in {name_table}s]\n\n"
            return method

        def generate_map_to_save_entity(pascal_name_table, fields):
            fields = [
                f
                for f in fields
                if f != "id"
                and not f.startswith("created_date")
                and not f.startswith("updated_date")
            ]
            method = f"def map_to_save_{name_table}_entity({name_table}: {pascal_name_table}Save) -> {pascal_name_table}Entity:\n"
            method += f"    return {pascal_name_table}Entity(\n"
            for field in fields:
                method += f"        {field}={name_table}.{field},\n"
            method += f"    )\n\n"
            return method

        def generate_map_to_update_entity(pascal_name_table, fields):
            fields = [
                f
                for f in fields
                if not f.startswith("created_date") and not f.startswith("updated_date")
            ]
            method = f"def map_to_update_{name_table}_entity({name_table}: {pascal_name_table}Update) -> {pascal_name_table}Entity:\n"
            method += f"    return {pascal_name_table}Entity(\n"
            for field in fields:
                method += f"        {field}={name_table}.{field},\n"
            method += f"    )\n\n"
            return method

        methods = ""
        methods += generate_map_to_entity(pascal_name_table, fields)
        methods += generate_map_to_list_entity(pascal_name_table)
        methods += generate_map_to_entity_entity(pascal_name_table, fields)
        methods += generate_map_to_list_entity_entity(pascal_name_table)
        methods += generate_map_to_save_entity(pascal_name_table, fields)
        methods += generate_map_to_update_entity(pascal_name_table, fields)

        file_contents: dict[str, str] = {f"{name_table}_mapper.py": methods}

        for file_name, content in file_contents.items():
            file_path = os.path.join(base_path, file_name)
            self.file_manager.create_file(file_path=file_path, content=content)

        return True

    def infrastructure_database_entities(self, name_table: str):
        pascal_name_table = snake_to_pascal(snake_str=name_table)
        base_path = os.path.join(
            self.current_directory, "src", "infrastructure", "database", "entities"
        )
        if not self.file_exists(file_path=f"{base_path}/{name_table}_entity.py"):
            return False

        columns = self.db.inspector.get_columns(name_table)

        class_code = f"from sqlalchemy.sql import func\n"
        class_code += f"from src.core.models.base import Base\n"
        class_code += (
            f"from sqlalchemy import Column, String, Boolean, DateTime, text\n"
        )
        class_code += f"from sqlalchemy.dialects.postgresql import UUID\n\n"
        class_code += f"class {pascal_name_table}Entity(Base):\n"
        class_code += f"    __tablename__ = '{name_table}'\n\n"

        for column in columns:
            col_name = column["name"]
            col_type = self.map_column_type(postgres_type=column["type"])
            nullable = column["nullable"]
            default = column["default"]
            primary_key = col_name == "id"
            unique = col_name == "code"
            onupdate = "onupdate=text('now()')" if col_name == "updated_date" else ""

            col_args = [col_type]
            if primary_key:
                col_args.append("primary_key=True")
            if nullable is not None:
                col_args.append(f"nullable={nullable}")
            if default:
                col_args.append(f"server_default=text('{default}')")
            if unique:
                col_args.append("unique=True")
            if onupdate:
                col_args.append(onupdate)

            col_definition = f"    {col_name} = Column({', '.join(col_args)})\n"

            class_code += col_definition

        file_contents: dict[str, str] = {f"{name_table}_entity.py": class_code}

        for file_name, content in file_contents.items():
            file_path = os.path.join(base_path, file_name)
            self.file_manager.create_file(file_path=file_path, content=content)

        return True

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

from src.domain.models.entities.{name_table}.index import (
    {pascal_name_table},
    {pascal_name_table}Delete,
    {pascal_name_table}Read,
    {pascal_name_table}Update,
)

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

    def create_domain_services_use_cases_entities_delete(self, name_table: str):
        pascal_name_table = snake_to_pascal(snake_str=name_table)

        model_code = f"""
from typing import Union
from src.core.config import settings
from src.core.enums.layer import LAYER
from src.core.models.config import Config
from src.core.wrappers.execute_transaction import execute_transaction
from src.domain.models.entities.{name_table}.index import {pascal_name_table}Delete, {pascal_name_table}
from src.domain.services.repositories.entities.i_{name_table}_repository import (
    I{pascal_name_table}Repository,
)


class {pascal_name_table}DeleteUseCase:
    def __init__(self, {name_table}_repository: I{pascal_name_table}Repository):
        self.{name_table}_repository = {name_table}_repository

    def execute(
        self,
        config: Config,
        params: {pascal_name_table}Delete,
    ) -> Union[{pascal_name_table}, str, None]:
        result = self.{name_table}_repository.delete(config=config, params=params)
        result = result.dict()
        if not result:
            return "No se encontro registro para eliminar"
        return result


if settings.has_track:
    {pascal_name_table}DeleteUseCase.execute = execute_transaction(LAYER.D_S_U_E.value)(
        {pascal_name_table}DeleteUseCase.execute
    )
        """

        return model_code

    def create_domain_services_use_cases_entities_list(self, name_table: str):
        pascal_name_table = snake_to_pascal(snake_str=name_table)

        model_code = f"""
from typing import List, Union
from src.core.config import settings
from src.core.enums.layer import LAYER
from src.core.models.config import Config
from src.core.models.filter import Pagination
from src.domain.models.entities.{name_table}.index import {pascal_name_table}
from src.core.wrappers.execute_transaction import execute_transaction
from src.domain.services.repositories.entities.i_{name_table}_repository import (
    I{pascal_name_table}Repository,
)


class {pascal_name_table}ListUseCase:
    def __init__(self, {name_table}_repository: I{pascal_name_table}Repository):
        self.{name_table}_repository = {name_table}_repository

    def execute(
        self,
        config: Config,
        params: Pagination,
    ) -> Union[List[{pascal_name_table}], str, None]:
        results = self.{name_table}_repository.list(config=config, params=params)
        results = [result.dict() for result in results]
        if not results:
            return "No se encontraron resultados"
        return results


if settings.has_track:
    {pascal_name_table}ListUseCase.execute = execute_transaction(LAYER.D_S_U_E.value)(
        {pascal_name_table}ListUseCase.execute
    )
        """

        return model_code

    def create_domain_services_use_cases_entities_read(self, name_table: str):
        pascal_name_table = snake_to_pascal(snake_str=name_table)

        model_code = f"""
from typing import Union
from src.core.config import settings
from src.core.enums.layer import LAYER
from src.core.models.config import Config
from src.core.wrappers.execute_transaction import execute_transaction
from src.domain.models.entities.{name_table}.index import {pascal_name_table}, {pascal_name_table}Read
from src.domain.services.repositories.entities.i_{name_table}_repository import (
    I{pascal_name_table}Repository,
)


class {pascal_name_table}ReadUseCase:
    def __init__(self, {name_table}_repository: I{pascal_name_table}Repository):
        self.{name_table}_repository = {name_table}_repository

    def execute(
        self,
        config: Config,
        params: {pascal_name_table}Read,
    ) -> Union[{pascal_name_table}, str, None]:
        result = self.{name_table}_repository.read(config=config, params=params)
        result = result.dict()
        if not result:
            return "No se encontro el registro"
        return result


if settings.has_track:
    {pascal_name_table}ReadUseCase.execute = execute_transaction(LAYER.D_S_U_E.value)(
        {pascal_name_table}ReadUseCase.execute
    )
        """

        return model_code

    def create_domain_services_use_cases_entities_save(self, name_table: str):
        pascal_name_table = snake_to_pascal(snake_str=name_table)

        model_code = f"""
from typing import Union
from src.core.enums.layer import LAYER
from src.core.models.config import Config
from src.core.wrappers.execute_transaction import execute_transaction
from src.domain.models.entities.{name_table}.index import {pascal_name_table}, {pascal_name_table}Save
from src.domain.services.repositories.entities.i_{name_table}_repository import (
    I{pascal_name_table}Repository,
)
from src.core.config import settings
from src.infrastructure.database.mappers.{name_table}_mapper import (
    map_to_save_{name_table}_entity,
)


class {pascal_name_table}SaveUseCase:
    def __init__(self, {name_table}_repository: I{pascal_name_table}Repository):
        self.{name_table}_repository = {name_table}_repository

    def execute(
        self,
        config: Config,
        params: {pascal_name_table}Save,
    ) -> Union[{pascal_name_table}, str, None]:
        result = map_to_save_{name_table}_entity(params)
        result = self.{name_table}_repository.save(config=config, params=result)
        result = result.dict()
        if not result:
            return "Error en el flujo, contactar al administrador"
        return result


if settings.has_track:
    {pascal_name_table}SaveUseCase.execute = execute_transaction(LAYER.D_S_U_E.value)(
        {pascal_name_table}SaveUseCase.execute
    )
        """

        return model_code

    def create_domain_services_use_cases_entities_update(self, name_table: str):
        pascal_name_table = snake_to_pascal(snake_str=name_table)

        model_code = f"""
from typing import Union
from src.core.enums.layer import LAYER
from src.core.models.config import Config
from src.core.wrappers.execute_transaction import execute_transaction
from src.domain.models.entities.{name_table}.index import {pascal_name_table}, {pascal_name_table}Update
from src.domain.services.repositories.entities.i_{name_table}_repository import (
    I{pascal_name_table}Repository,
)
from src.core.config import settings


class {pascal_name_table}UpdateUseCase:
    def __init__(self, {name_table}_repository: I{pascal_name_table}Repository):
        self.{name_table}_repository = {name_table}_repository

    def execute(
        self,
        config: Config,
        params: {pascal_name_table}Update,
    ) -> Union[{pascal_name_table}, str, None]:
        result = self.{name_table}_repository.update(config=config, params=params)
        result = result.dict()
        if not result:
            return "No se pudo realizar la actualización, no se encontro registro para actualizar"
        return result


if settings.has_track:
    {pascal_name_table}UpdateUseCase.execute = execute_transaction(LAYER.D_S_U_E.value)(
        {pascal_name_table}UpdateUseCase.execute
    )
        """

        return model_code

    def create_domain_services_use_cases_entities_index(self, name_table: str):
        pascal_name_table = snake_to_pascal(snake_str=name_table)

        model_code = f"""
from .{name_table}_delete_use_case import {pascal_name_table}DeleteUseCase
from .{name_table}_list_use_case import {pascal_name_table}ListUseCase
from .{name_table}_read_use_case import {pascal_name_table}ReadUseCase
from .{name_table}_save_use_case import {pascal_name_table}SaveUseCase
from .{name_table}_update_use_case import {pascal_name_table}UpdateUseCase


__all__ = [
    "{pascal_name_table}DeleteUseCase",
    "{pascal_name_table}ListUseCase",
    "{pascal_name_table}ReadUseCase",
    "{pascal_name_table}SaveUseCase",
    "{pascal_name_table}UpdateUseCase",
]
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
