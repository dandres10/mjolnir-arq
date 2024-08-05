from mjolnir_arq.core.databases.connection_postgresql import ConnectionPostgresql
from mjolnir_arq.core.models.login_db import LoginDB

from pydantic import BaseModel, Field, UUID4
from typing import Optional
from datetime import datetime
from sqlalchemy import UUID, VARCHAR, BOOLEAN, TIMESTAMP

import os


def check_folder_exists_os(folder_path):
    return os.path.isdir(folder_path)


def get_current_directory():
    return os.getcwd()


class MjolnirController:
    def __init__(self, loginDB: LoginDB) -> None:
        self.db = ConnectionPostgresql(loginDB)

    def create_flow_base(self, name_table: str):

        try:

            folder_path = f"{get_current_directory()}/src"
            if check_folder_exists_os(f"{folder_path}"):
                print(f"(os) La carpeta '{folder_path}' existe.")
            else:
                print(f"(os) La carpeta '{folder_path}' no existe.")

            model_code = f"from pydantic import BaseModel, Field, UUID4\n"
            model_code += f"from typing import Optional\n"
            model_code += f"from datetime import datetime\n\n"
            model_code += f"class {name_table}(BaseModel):\n"
            columns = self.db.inspector.get_columns(name_table)
            for column in columns:
                name = column["name"]
                column_type = column["type"]
                nullable = column["nullable"]
                default = column.get("default")

                if isinstance(column_type, UUID):
                    field_type = "UUID4"
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

                model_code += f"    {name}: {field_type} = {field_default}\n"

            model_code += f"\n"
            model_code += "    def dict(self, *args, **kwargs):\n"
            model_code += '        exclude = kwargs.pop("exclude", set())\n'
            model_code += '        exclude.update({"created_date", "updated_date"})\n'
            model_code += (
                "        return super().dict(*args, exclude=exclude, **kwargs)\n"
            )

            print(model_code)

        except Exception as e:
            print(f"ERROR: No se pudieron obtener las columnas: {e}")
