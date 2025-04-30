"""
Base document and utility
"""

import dataclasses
import hashlib
import typing

import cerberus
from pydantic import BaseModel, Field

from chk.infrastructure.entities import (
    ExecutionContext,
    FileInfoContext,
    SpecificationMeta,
)
from chk.infrastructure.file_loader import FileContext, FileLoader


@dataclasses.dataclass(slots=True)
class VersionedDocument:
    """
    Http document entity
    """

    context: tuple = dataclasses.field(default_factory=tuple)
    version: str = dataclasses.field(default_factory=str)


class VersionedDocumentV2(BaseModel):
    """
    versioned document entity
    """

    context: tuple = Field(default_factory=tuple)
    version: str = Field(default_factory=str)


class VersionedDocumentSupport:
    """DocumentVersionSupport"""

    @staticmethod
    def validate_with_schema(schema: dict, doc: VersionedDocument | VersionedDocumentV2) -> bool:
        """Validate a document with given schema

        Args:
            schema: dict that holds schema
            doc: VersionedDocument A versioned document

        Returns:
            bool: True on success

        Raises:
            RuntimeError
        """

        validator = cerberus.Validator()
        file_ctx = FileContext(*doc.context)

        try:
            if not validator.validate(file_ctx.document, schema):
                raise RuntimeError(f"File exception: Validation failed: {str(validator.errors)}")
        except cerberus.validator.DocumentError as doc_err:
            raise RuntimeError(f"Document exception: `version` string not found: {str(doc_err)}") from doc_err

        return True


class FileInfoContextService:
    """Service class of FileInfoContext"""

    @staticmethod
    def create(file: str) -> FileInfoContext:
        fp = FileLoader.load_file(file)
        absolute_path = str(fp.absolute())

        return FileInfoContext(
            filepath=absolute_path,
            filepath_hash=hashlib.sha256(absolute_path.encode("utf-8")).hexdigest(),
            document=FileLoader.load_yaml(absolute_path),
        )


class SpecificationMetaService:
    """Service for SpecificationMeta"""

    @staticmethod
    def create(
        session_id: str, file: str, opts: dict[str, typing.Any], args: dict[str, typing.Any]
    ) -> SpecificationMeta:
        assert len(session_id) > 0, "Session ID not set."

        return SpecificationMeta(
            session_id=session_id,
            ctx_execution=ExecutionContext(options=opts, arguments=args),
            ctx_file=FileInfoContextService.create(file),
        )
