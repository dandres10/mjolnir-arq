
from typing import List, Union
from abc import ABC, abstractmethod

from pydantic import UUID4
from src.core.models.config import Config
from src.core.models.filter import Pagination
from src.domain.models.entities.language.language import Language
from src.domain.models.entities.language.language_delete import LanguageDelete
from src.domain.models.entities.language.language_read import LanguageRead
from src.domain.models.entities.language.language_update import LanguageUpdate
from src.infrastructure.database.entities.language_entity import LanguageEntity


class ILanguageRepository(ABC):
    @abstractmethod
    def save(
        self,
        config: Config,
        params: LanguageEntity,
    ) -> Union[Language, None]:
        pass

    @abstractmethod
    def update(
        self,
        config: Config,
        params: LanguageUpdate,
    ) -> Union[Language, None]:
        pass

    @abstractmethod
    def list(
        self,
        config: Config,
        params: Pagination,
    ) -> Union[List[Language], None]:
        pass

    @abstractmethod
    def delete(
        self,
        config: Config,
        params: LanguageDelete,
    ) -> Union[Language, None]:
        pass

    @abstractmethod
    def read(
        self,
        config: Config,
        params: LanguageRead,
    ) -> Union[Language, None]:
        pass
        