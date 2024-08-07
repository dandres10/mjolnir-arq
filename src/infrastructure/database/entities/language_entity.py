from sqlalchemy.sql import func
from src.core.models.base import Base
from sqlalchemy import Column, String, Boolean, DateTime, text
from sqlalchemy.dialects.postgresql import UUID

class LanguageEntity(Base):
    __tablename__ = 'language'

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, server_default=text('uuid_generate_v4()'))
    name = Column(String(100), nullable=False)
    code = Column(String(10), nullable=False, unique=True)
    native_name = Column(String(100), nullable=True)
    state = Column(Boolean, nullable=False, server_default=text('true'))
    created_date = Column(DateTime, nullable=False, server_default=text('now()'))
    updated_date = Column(DateTime, nullable=False, server_default=text('now()'), onupdate=text('now()'))
