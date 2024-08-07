
from typing import List, Union
from src.core.config import settings
from src.core.enums.layer import LAYER
from src.core.models.config import Config
from src.core.models.filter import Pagination
from src.domain.models.entities.language.index import Language
from src.core.wrappers.execute_transaction import execute_transaction
from src.domain.services.repositories.entities.i_language_repository import (
    ILanguageRepository,
)


class LanguageListUseCase:
    def __init__(self, language_repository: ILanguageRepository):
        self.language_repository = language_repository

    def execute(
        self,
        config: Config,
        params: Pagination,
    ) -> Union[List[Language], str, None]:
        results = self.language_repository.list(config=config, params=params)
        results = [result.dict() for result in results]
        if not results:
            return "No se encontraron resultados"
        return results


if settings.has_track:
    LanguageListUseCase.execute = execute_transaction(LAYER.D_S_U_E.value)(
        LanguageListUseCase.execute
    )
        