from main.database.db import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey, Column, Integer, String, Table, MetaData

auth_metadata = MetaData(schema="auth")

User = Table(
    "users",
    auth_metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
)

class Service(Base):
    __tablename__ = "service"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    importance = Column(Integer)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.c.id))