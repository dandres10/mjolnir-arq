
from typing import Union
from src.core.config import settings
from src.core.enums.layer import LAYER
from src.core.models.config import Config
from src.core.wrappers.execute_transaction import execute_transaction
from src.domain.models.entities.language.index import Language, LanguageRead
from src.domain.services.repositories.entities.i_language_repository import (
    ILanguageRepository,
)


class LanguageReadUseCase:
    def __init__(self, language_repository: ILanguageRepository):
        self.language_repository = language_repository

    def execute(
        self,
        config: Config,
        params: LanguageRead,
    ) -> Union[Language, str, None]:
        result = self.language_repository.read(config=config, params=params)
        result = result.dict()
        if not result:
            return "No se encontro el registro"
        return result


if settings.has_track:
    LanguageReadUseCase.execute = execute_transaction(LAYER.D_S_U_E.value)(
        LanguageReadUseCase.execute
    )
        