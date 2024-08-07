
from typing import List, Union
from abc import ABC, abstractmethod

from src.core.models.config import Config
from src.core.models.filter import Pagination

from src.domain.models.entities.language.index import (
    Language,
    LanguageDelete,
    LanguageRead,
    LanguageUpdate,
)

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
        