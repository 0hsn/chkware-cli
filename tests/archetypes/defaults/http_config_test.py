import pytest
import tests
from chk.archetypes.defaults.http_config import HttpV072
from chk.support.loader import ChkFileLoader


class TestHttpV072:
    """Test chk.archetypes.defaults.http_config.HttpV072"""

    def test_validate_schema(self):
        """when version string not given"""
        config = {
            'version': 'default:http:0.7.2',
            'request': {
                'url': 'https://example.com',
                'method': 'GET'
            }
        }

        ver = HttpV072()
        assert ver.validate_config(config) is True

    def test_validate_fail_if_url_empty(self):
        """when version string not given"""
        config = {
            'version': 'default:http:0.7.2',
            'request': {
                'url': None,
                'method': 'GET'
            }
        }

        ver = HttpV072()

        with pytest.raises(SystemExit) as ex:
            assert ver.validate_config(config) is True

    def test_validate_get_with_query_expect_pass(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'pass_cases/GET-WithQuery.chk')
        ver = HttpV072()
        assert ver.validate_config(doc) is True

    def test_validate_get_with_query_empty_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/GET-WithQuery-Empty.chk')
        ver = HttpV072()

        with pytest.raises(SystemExit):
            assert ver.validate_config(doc) is True

    def test_validate_get_with_query_as_list_expect_fail(self):
        """when version string not given"""
        doc = ChkFileLoader.to_dict(tests.RES_DIR + 'fail_cases/GET-WithQuery-AsList.chk')
        ver = HttpV072()

        with pytest.raises(SystemExit):
            assert ver.validate_config(doc) is True
