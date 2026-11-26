# Testing and mocking

Slide 93 covers testing a small shop and replacing an LLM client with a mock. Unit tests cover discount, tax, totals and the in-memory stock repository. Integration tests exercise order placement and stock together. The Groq tests inject a mock client, assert the request and response, and simulate an API failure.

From this folder, with Python 3.10 or newer, run the following in your Python environment.

```bash
python -m pip install -r requirements.txt
python -m pytest
python -m pytest --cov=src --cov-report=term-missing
python -m pytest -m slow
```

The `slow` test simulates a batch of orders in memory. All tests run without an API key or network access. To use `ask_groq` with a real client, install the optional `groq` SDK and provide `GROQ_API_KEY` in your environment.
