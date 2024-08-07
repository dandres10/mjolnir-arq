
from typing import Union
from src.core.enums.layer import LAYER
from src.core.models.config import Config
from src.core.wrappers.execute_transaction import execute_transaction
from src.domain.models.entities.language.index import Language, LanguageSave
from src.domain.services.repositories.entities.i_language_repository import (
    ILanguageRepository,
)
from src.core.config import settings
from src.infrastructure.database.mappers.language_mapper import (
    map_to_save_language_entity,
)


class LanguageSaveUseCase:
    def __init__(self, language_repository: ILanguageRepository):
        self.language_repository = language_repository

    def execute(
        self,
        config: Config,
        params: LanguageSave,
    ) -> Union[Language, str, None]:
        result = map_to_save_language_entity(params)
        result = self.language_repository.save(config=config, params=result)
        result = result.dict()
        if not result:
            return "Error en el flujo, contactar al administrador"
        return result


if settings.has_track:
    LanguageSaveUseCase.execute = execute_transaction(LAYER.D_S_U_E.value)(
        LanguageSaveUseCase.execute
    )
        