import json


def test_chat_streams_and_logs(client):
    r = client.post(
        "/chat", json={"messages": [{"role": "user", "content": "What is a star label?"}]}
    )
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/event-stream")
    assert 'data: {"delta": "You "}' in r.text
    assert "event: done" in r.text
    with open(client.settings.cost_log_path, encoding="utf-8") as f:
        record = json.loads(f.readline())
    assert record["ok"] is True and record["fallback_used"] is False


def test_chat_rejects_bad_input(client):
    r = client.post("/chat", json={"messages": [{"role": "hacker", "content": "hi"}]})
    assert r.status_code == 422
