
from typing import Union
from src.core.enums.layer import LAYER
from src.core.models.config import Config
from src.core.wrappers.execute_transaction import execute_transaction
from src.domain.models.entities.language.index import Language, LanguageUpdate
from src.domain.services.repositories.entities.i_language_repository import (
    ILanguageRepository,
)
from src.core.config import settings


class LanguageUpdateUseCase:
    def __init__(self, language_repository: ILanguageRepository):
        self.language_repository = language_repository

    def execute(
        self,
        config: Config,
        params: LanguageUpdate,
    ) -> Union[Language, str, None]:
        result = self.language_repository.update(config=config, params=params)
        result = result.dict()
        if not result:
            return "No se pudo realizar la actualización, no se encontro registro para actualizar"
        return result


if settings.has_track:
    LanguageUpdateUseCase.execute = execute_transaction(LAYER.D_S_U_E.value)(
        LanguageUpdateUseCase.execute
    )
        