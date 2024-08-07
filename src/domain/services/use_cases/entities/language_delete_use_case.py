
from typing import Union
from src.core.config import settings
from src.core.enums.layer import LAYER
from src.core.models.config import Config
from src.core.wrappers.execute_transaction import execute_transaction
from src.domain.models.entities.language.index import LanguageDelete, Language
from src.domain.services.repositories.entities.i_language_repository import (
    ILanguageRepository,
)


class LanguageDeleteUseCase:
    def __init__(self, language_repository: ILanguageRepository):
        self.language_repository = language_repository

    def execute(
        self,
        config: Config,
        params: LanguageDelete,
    ) -> Union[Language, str, None]:
        result = self.language_repository.delete(config=config, params=params)
        result = result.dict()
        if not result:
            return "No se encontro registro para eliminar"
        return result


if settings.has_track:
    LanguageDeleteUseCase.execute = execute_transaction(LAYER.D_S_U_E.value)(
        LanguageDeleteUseCase.execute
    )
        