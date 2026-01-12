import sys

import pytest


def test_imports():
    try:
        import utils.client

        assert True, "Imported utils.client"
    except ImportError:
        try:
            import tradestation.utils.client

            assert True, "Imported tradestation.utils.client"
        except ImportError:
            pytest.fail(f"Could not import utils.client or tradestation.utils.client. Sys path: {sys.path}")
