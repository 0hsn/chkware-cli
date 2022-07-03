"""
testcase related support services
"""
from cerberus import validator
from chk.infrastructure.exception import err_message, messages
from chk.modules.testcase.constants import TestSpecConfigNode, ExecuteConfigNode
from chk.modules.http.constants import RequestConfigNode
from chk.modules.testcase.validation_rules import testcase_schema


class TestSpecMixin:
    """
    Mixin for version spec. for v0.7.2
    """

    def __init_testcase_mixin(self):
        self.in_file = True
        
    def is_request_infile(self) -> bool:
        return self.in_file;

    def testcase_validated(self) -> dict[str, str]:
        """
        Validate the schema against config
        """
        try:
            testcase_doc = self.testcase_as_dict()
            if not self.validator.validate(testcase_doc, testcase_schema):
                raise SystemExit(err_message('fatal.V0006', extra=self.validator.errors))

            # validate request if it exists in-file
            self.validate_request_block()
            self.validate_with_block()
        except validator.DocumentError as doc_err:
            raise SystemExit(err_message('fatal.V0001', extra=doc_err)) from doc_err

        return testcase_doc  # or is a success

    def testcase_as_dict(self) -> dict[str, str]:
        """
        Get version string
        """
        if not hasattr(self, 'validator') or not hasattr(self, 'document'):
            raise SystemExit(err_message('fatal.V0005'))

        try:
            return {key: self.document[key] for key in (TestSpecConfigNode.ROOT, ) if key in self.document}
        except Exception as ex:
            raise SystemExit(err_message('fatal.V0005', extra=ex))

    def validate_request_block(self) -> None:
        """
        If request in file validate it or set False to internal in_file
        :return: None
        """
        out_file_request = self.document\
                               .get(TestSpecConfigNode.ROOT)\
                               .get(ExecuteConfigNode.ROOT)\
                               .get(ExecuteConfigNode.FILE) is not None
        in_file_request = self.document.get(RequestConfigNode.ROOT) is not None

        if in_file_request is out_file_request:
            raise SystemExit(err_message('fatal.V0020', extra={'spec': {'execute': {'file': '...'}}}))

        self.__init_testcase_mixin()

        if in_file_request:
            self.request_validated()
            self.in_file = True
        else:
            self.in_file = False

    def validate_with_block(self) -> None:
        """
        Check is data passing to same context
        :return: None
        """
        in_file_request = self.document.get(RequestConfigNode.ROOT) is not None

        out_file_with = self.document\
                            .get(TestSpecConfigNode.ROOT)\
                            .get(ExecuteConfigNode.ROOT)\
                            .get(ExecuteConfigNode.WITH) is not None

        if in_file_request and out_file_with:
            raise SystemExit(err_message('fatal.V0021', extra={'spec': {'execute': {'with': 'Not allowed'}}}))