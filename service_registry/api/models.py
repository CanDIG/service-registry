"""
API Data Model definitions
"""

from dataclasses import dataclass

@dataclass
class Error:
    status: int
    title: str
    detail: str


@dataclass
class ServiceType:
    group: str
    artifact: str
    version: str


@dataclass
class Organization:
    name: str
    url: str


@dataclass
class Service:
    id: str
    name: str
    type: ServiceType
    organization: Organization
    version: str
    contactUrl: str = ''
    documentation: str = ''
    description: str = ''
    createdAt: str = ''
    updatedAt: str = ''
    environment: str = ''

@dataclass
class ExternalService():
    id: str
    name: str
    type: ServiceType
    organization: Organization
    version: str
    url: str
    contactUrl: str = ''
    documentation: str = ''
    description: str = ''
    createdAt: str = ''
    updatedAt: str = ''
    environment: str = ''