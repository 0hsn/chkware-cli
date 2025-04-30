"""System entities"""

from __future__ import annotations

import typing

from pydantic import BaseModel, Field


class Document(BaseModel):
    """Document model"""

    version: str
    variables: typing.Optional[list]
    expose: typing.Optional[list]


class ExecutionContext(BaseModel):
    """Information storage for execution context"""

    options: dict[str, typing.Any] = Field(default_factory=dict)
    arguments: dict[str, typing.Any] = Field(default_factory=dict)


class FileInfoContext(BaseModel):
    """Information of file being loaded"""

    document: dict = Field(default_factory=dict)
    filepath: str = Field(default_factory=str)
    filepath_hash: str = Field(default_factory=str)


class SpecificationMeta(BaseModel):
    """Meta for a spec document"""

    session_id: str
    ctx_file: FileInfoContext
    ctx_execution: ExecutionContext = Field(default_factory=ExecutionContext)


class Specification(BaseModel):
    """Base spec document"""

    meta: SpecificationMeta
    document: Document
