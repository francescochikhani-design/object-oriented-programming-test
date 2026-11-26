import sys
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from src import groq_chat


def test_returns_answer_and_sends_expected_request(client):
    message = SimpleNamespace(content="An object holds state and behavior.")
    client.chat.completions.create.return_value = SimpleNamespace(
        choices=[SimpleNamespace(message=message)]
    )
    assert groq_chat.ask_groq("What is an object?", client) == message.content
    client.chat.completions.create.assert_called_once_with(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "What is an object?"}],
        max_tokens=1024,
    )


def test_propagates_api_failure(client):
    client.chat.completions.create.side_effect = TimeoutError("API timed out")
    with pytest.raises(TimeoutError, match="timed out"):
        groq_chat.ask_groq("Hello?", client)


def test_empty_question_skips_client(client):
    with pytest.raises(ValueError, match="empty"):
        groq_chat.ask_groq("  ", client)
    client.chat.completions.create.assert_not_called()


def test_default_client_can_be_patched(client, monkeypatch):
    client.chat.completions.create.return_value.choices = [
        SimpleNamespace(message=SimpleNamespace(content="Mocked"))
    ]
    constructor = Mock(return_value=client)
    monkeypatch.setitem(sys.modules, "groq", SimpleNamespace(Groq=constructor))
    assert groq_chat.ask_groq("Hello?") == "Mocked"
    constructor.assert_called_once_with()
