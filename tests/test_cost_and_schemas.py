import pytest
from pydantic import ValidationError

from app.cost import cost_usd
from app.schemas import ChatRequest, Usage


def test_cost_usd():
    usage = Usage(input_tokens=1200, output_tokens=300)
    assert cost_usd(usage, 0.5, 1.5) == pytest.approx(0.00105)


def test_chat_request_limits():
    with pytest.raises(ValidationError):
        ChatRequest(messages=[{"role": "user", "content": "hi"}], temperature=3.0)
    with pytest.raises(ValidationError):
        ChatRequest(messages=[])
