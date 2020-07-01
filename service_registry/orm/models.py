"""
SQLAlchemy models for the database
"""
import datetime
import uuid
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy import UniqueConstraint, ForeignKey
from service_registry.orm.guid import GUID
from service_registry.orm import Base


class URL(Base):
    """
    SQLAlchemy class/table representing URL of a service
    """
    __tablename__ = 'urls'
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String(100))
    url = Column(String(100))
    added = Column(DateTime, default=datetime.datetime.utcnow)
    service = Column(GUID(), ForeignKey('services.id'), default=None)
    __table_args__ = (
        UniqueConstraint('url'),
    )


class Type(Base):
    """
    SQLAlchemy class/table representing type of a service
    """
    __tablename__ = 'types'
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    group = Column(String(100))
    artifact = Column(String(100))
    version = Column(String(100))


class Organization(Base):
    """
    SQLAlchemy class/table representing organization of a service
    """
    __tablename__ = 'organizations'
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String(100))
    url = Column(String(100))


class Service(Base):
    """
    SQLAlchemy class/table representing a service
    """
    __tablename__ = 'services'
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String(100))
    type = Column(GUID(), ForeignKey('types.id'), default=None)
    description = Column(String(100))
    organization = Column(GUID(), ForeignKey('organizations.id'), default=None)
    contact_url = Column(String(100))
    documentation_url = Column(String(100))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    environment = Column(String(100))
    version = Column(String(100))
    active = Column(Boolean())
