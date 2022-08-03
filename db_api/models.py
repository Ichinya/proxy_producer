import dataclasses
import json

from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry

mapper_registry = registry()
Base = mapper_registry.generate_base()


class BaseModel(Base):
    __abstract__ = True
    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class BaseTimeModel(BaseModel):
    __abstract__ = True

    created_at = Column(DateTime(True), server_default=func.now())
    updated_at = Column(DateTime(True), server_default=func.now(), default=func.now(), onupdate=func.now())


class Proxy(BaseTimeModel):
    __tablename__ = 'proxies'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    proxy = Column(String(1000), unique=True, nullable=False)
    is_good = Column(Boolean, nullable=True)
    send_to_mq = Column(DateTime, default=None, index=True)
    check_at = Column(DateTime, default=None, index=True)
    import_at = Column(DateTime, default=None, index=True)


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


__all__ = ['mapper_registry', 'EnhancedJSONEncoder', 'Proxy']
