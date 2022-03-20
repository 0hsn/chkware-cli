"""
Versioned schema repository for http specifications
"""
from typing import Dict
from chk.modules.version.entities import AbstractSpecConfig, VersionConfigV072
from chk.modules.http.validation_rules import request_schema
from cerberus.validator import DocumentError
from chk.console.app_container import app


class HttpConfigV072(AbstractSpecConfig):
    """http config v0.7.2"""
    def __init__(self):
        super().__init__()
        self.version_config = VersionConfigV072()

    def get_schema(self) -> Dict:
        """create and validate schema against the dict passed"""
        return self.version_config.get_schema() | request_schema

    def validate_config(self, config: Dict) -> bool:
        """Validate the schema against config"""
        self.version_config.validate_config(config)  # validate version

        try:
            if self.validator.validate(config, self.get_schema()) is not True:  # validate request
                raise SystemExit(str(self.validator.errors))
        except DocumentError as doc_err:
            raise SystemExit(f'{app.messages.exception.fatal.V0001}: {doc_err}') from doc_err
        else:
            return True  # or is a success
