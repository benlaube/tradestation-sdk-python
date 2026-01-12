from dataclasses import dataclass

from tradestation.utils.client import parse_api_error_response


@dataclass
class MockResponse:
    status_code: int
    _json: dict

    def json(self):
        return self._json


def test_parse_multiple_errors():
    """Test that multiple errors in the 'Errors' list are parsed correctly."""
    error_body = {"Errors": [{"Error": "First error", "Code": "100"}, {"Error": "Second error", "Code": "101"}]}
    response = MockResponse(400, error_body)

    details = parse_api_error_response(response)

    assert len(details.api_errors) == 2
    assert details.api_errors[0].code == "100"
    assert details.api_errors[0].error == "First error"
    assert details.api_errors[1].code == "101"
    assert details.api_errors[1].error == "Second error"

    # Check top-level message matches first error
    assert details.api_error_code == "100"
    assert "First error" in details.message


def test_parse_single_error_format():
    """Test standard single error format."""
    error_body = {"Error": "Single error", "Code": "200"}
    response = MockResponse(400, error_body)

    details = parse_api_error_response(response)

    assert len(details.api_errors) == 1
    assert details.api_errors[0].code == "200"
    assert details.api_errors[0].error == "Single error"


def test_parse_simple_message():
    """Test parsing simple Message format."""
    # Note: simple message format doesn't populate api_errors list in current implementation
    # unless we update it to do so. Let's verify behavior.
    error_body = {"Message": "Simple message"}
    response = MockResponse(400, error_body)

    details = parse_api_error_response(response)
    # Current implementation only appends to api_errors for Format 1 and Format 2
    # Standardizing Format 3 to also add to api_errors would be consistent.
    # For now, verify current implementation.
    assert details.message == "Simple message"
