from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from mjolnir_arq.core.models.login_db import LoginDB
from sqlalchemy.exc import SQLAlchemyError


class ConnectionPostgresql:
    def __init__(self, loginDB: LoginDB) -> None:
        self.DATABASE_URL = f"postgresql+psycopg2://{loginDB.name_user}:{loginDB.password}@{loginDB.host}:{loginDB.port}/{loginDB.name_db}"
        self.engine = None
        self.session = None
        self.inspector = None
        self._connect()

    def _connect(self):
        try:
            self.engine = create_engine(self.DATABASE_URL, pool_size=20)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
            self.inspector = inspect(self.engine)
            print("SUCESS: Conexión a la base de datos establecida con éxito.")
        except SQLAlchemyError as e:
            print(f"ERROR: Error al conectar con la base de datos: {e}")
            self._disconnect()

    def close(self):
        self._disconnect()
