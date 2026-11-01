import asyncio

import httpx
import pytest

from app.llm.base import LLMError, LLMUnavailable, StreamResult
from app.llm.openai_compat import OpenAICompatProvider
from app.schemas import Message

MSGS = [Message(role="user", content="hello")]


def sse_body(with_usage: bool) -> bytes:
    lines = [
        'data: {"choices":[{"delta":{"content":"Hel"}}]}',
        'data: {"choices":[{"delta":{"content":"lo"}}]}',
    ]
    if with_usage:
        lines.append('data: {"choices":[],"usage":{"prompt_tokens":7,"completion_tokens":2}}')
    lines.append("data: [DONE]")
    return ("\n\n".join(lines) + "\n\n").encode()


def provider(handler, max_retries=3):
    return OpenAICompatProvider(
        base_url="http://test/v1",
        api_key="k",
        model="m",
        max_retries=max_retries,
        backoff_base_seconds=0.0,
        transport=httpx.MockTransport(handler),
    )


def collect(p):
    result = StreamResult()

    async def run():
        return "".join([piece async for piece in p.stream_chat(MSGS, 0.2, result)])

    return asyncio.run(run()), result


def test_retries_503_then_succeeds():
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        if calls["n"] < 3:
            return httpx.Response(503)
        return httpx.Response(200, content=sse_body(True))

    text, _ = collect(provider(handler))
    assert text == "Hello" and calls["n"] == 3


def test_does_not_retry_on_401():
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        return httpx.Response(401, json={"error": "bad key"})

    with pytest.raises(LLMError) as exc:
        collect(provider(handler))
    assert calls["n"] == 1
    assert not isinstance(exc.value, LLMUnavailable)


def test_gives_up_after_timeouts():
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        raise httpx.ReadTimeout("slow", request=request)

    with pytest.raises(LLMUnavailable):
        collect(provider(handler, max_retries=2))
    assert calls["n"] == 3


def test_uses_provider_usage_when_given():
    _, result = collect(provider(lambda r: httpx.Response(200, content=sse_body(True))))
    assert result.usage.input_tokens == 7
    assert result.usage.output_tokens == 2
    assert result.usage.estimated is False


def test_estimates_usage_when_missing():
    _, result = collect(provider(lambda r: httpx.Response(200, content=sse_body(False))))
    assert result.usage.estimated is True
    assert result.usage.input_tokens > 0
