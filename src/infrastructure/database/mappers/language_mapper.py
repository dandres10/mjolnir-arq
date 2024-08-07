
from typing import List
from src.domain.models.entities.language.index import (
    Language,
    LanguageSave,
    LanguageUpdate,
)
from src.infrastructure.database.entities.language_entity import LanguageEntity


def map_to_language(language_entity: LanguageEntity) -> Language:
    return Language(
        id=language_entity.id,
        name=language_entity.name,
        code=language_entity.code,
        native_name=language_entity.native_name,
        state=language_entity.state,
        created_date=language_entity.created_date,
        updated_date=language_entity.updated_date,
    )

def map_to_list_language(language_entities: List[LanguageEntity]) -> List[Language]:
    return [map_to_language(language) for language in language_entities]

def map_to_language_entity(language: Language) -> LanguageEntity:
    return LanguageEntity(
        id=language.id,
        name=language.name,
        code=language.code,
        native_name=language.native_name,
        state=language.state,
        created_date=language.created_date,
        updated_date=language.updated_date,
    )

def map_to_list_language_entity(languages: List[Language]) -> List[LanguageEntity]:
    return [map_to_language_entity(language) for language in languages]

def map_to_save_language_entity(language: LanguageSave) -> LanguageEntity:
    return LanguageEntity(
        name=language.name,
        code=language.code,
        native_name=language.native_name,
        state=language.state,
    )

def map_to_update_language_entity(language: LanguageUpdate) -> LanguageEntity:
    return LanguageEntity(
        id=language.id,
        name=language.name,
        code=language.code,
        native_name=language.native_name,
        state=language.state,
    )

