"""Minimal OpenAI-compatible chat client used by stages 1 and 3.

The original code star-imported a large shared utility module; only two
entry points were ever used, so they are reproduced here with the same
semantics and no other dependencies.

Credentials are read from the environment and never stored:
    OPENAI_API_KEY   required
    OPENAI_BASE_URL  optional, for an OpenAI-compatible proxy
"""

from __future__ import annotations

import os
import time
from typing import Any, Dict

SYSTEM_PROMPT = "You are a helpful assistant skilled in handling tabular data."

# Reasoning effort for the GPT-5 family, lowest first. Reasoning is disabled
# where the model allows it, because none of these prompts benefit from it and
# reasoning tokens are billed as output. Not every GPT-5 variant accepts every
# value: the gpt-5.2 proxy alias accepts "none", while gpt-5-2025-08-07 accepts
# only minimal/low/medium/high. The first accepted value is remembered per
# model in _EFFORT_FOR_MODEL, so a model pays the discovery cost once.
REASONING_EFFORT_LADDER = ("none", "minimal")
DEFAULT_REASONING_EFFORT = os.environ.get("OPENAI_REASONING_EFFORT") or None

_EFFORT_FOR_MODEL: Dict[str, str | None] = {}

# Cumulative token usage across all calls in this process.
_TOTAL_INPUT_TOKENS = 0
_TOTAL_OUTPUT_TOKENS = 0


def _client():
    from openai import OpenAI

    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Export it in your shell before running "
            "any stage that calls an LLM (stage 1 keyword extraction, stage 3 "
            "disambiguation)."
        )
    kwargs: Dict[str, Any] = {"api_key": key}
    base_url = os.environ.get("OPENAI_BASE_URL")
    if base_url:
        kwargs["base_url"] = base_url
    return OpenAI(**kwargs)


def _usage(response) -> Dict[str, int]:
    """Normalize token usage across the Chat and Responses APIs."""
    u = getattr(response, "usage", None)
    if u is None:
        return {"input_tokens": 0, "output_tokens": 0}
    get = (lambda k, d=0: u.get(k, d)) if isinstance(u, dict) else (lambda k, d=0: getattr(u, k, d))
    return {
        "input_tokens": int(get("input_tokens") or get("prompt_tokens") or 0),
        "output_tokens": int(get("output_tokens") or get("completion_tokens") or 0),
    }


def _is_permanent(exc: Exception) -> bool:
    """True for errors that will fail identically on every retry.

    A bad request, an unknown model or a rejected parameter is a property of
    the call, not of the network. Retrying those only delays the error message
    the caller needs to see.
    """
    status = getattr(exc, "status_code", None) or getattr(exc, "code", None)
    if status in (400, 401, 403, 404, 422):
        return True
    return type(exc).__name__ in {
        "BadRequestError", "AuthenticationError", "PermissionDeniedError",
        "NotFoundError", "UnprocessableEntityError"}


def _is_unsupported_effort(exc: Exception) -> bool:
    """True when the API rejected the reasoning effort value itself.

    That is a permanent property of the model, not a transient failure, so it
    must not be retried with the same value.
    """
    text = str(exc)
    return "reasoning.effort" in text or (
        "reasoning" in text and "not supported" in text and "effort" in text)


def _efforts_to_try(model: str) -> list[str | None]:
    """Reasoning-effort values to attempt for this model, best first."""
    if model in _EFFORT_FOR_MODEL:
        return [_EFFORT_FOR_MODEL[model]]
    if DEFAULT_REASONING_EFFORT:
        return [DEFAULT_REASONING_EFFORT]
    # None means: send no reasoning field at all, and let the model decide.
    return [*REASONING_EFFORT_LADDER, None]


def _call(prompt: str, model: str, max_tokens: int, temperature: float,
          json_format: bool = False, seed: int | None = None):
    """One raw API call.

    The GPT-5 family goes through the Responses API; everything else through
    Chat Completions. For GPT-5 the reasoning effort is negotiated once per
    model against REASONING_EFFORT_LADDER, because the accepted values differ
    between variants.

    `json_format` is NOT decorative. Callers that parse the reply as JSON pass
    it, and it does two things: it asks the API for a guaranteed-parseable
    object, and it tells the model so in the system prompt. Accepting the flag
    and ignoring it — which this function used to do — leaves the model free to
    answer in prose or fenced markdown; the caller's json.loads then fails, and
    in the operator search a failed parse silently discards that candidate
    operator and the beam continues down a different chain.
    """
    client = _client()
    system = SYSTEM_PROMPT
    if json_format:
        system = (f"{system} Return only one valid JSON object. "
                  "Do not wrap the response in markdown or add explanatory text.")
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt},
    ]

    if model.startswith("gpt-5"):
        last_error: Exception | None = None
        for effort in _efforts_to_try(model):
            kwargs: Dict[str, Any] = dict(model=model, input=messages,
                                          stream=False, top_p=1)
            if effort is not None:
                kwargs["reasoning"] = {"effort": effort}
            try:
                response = client.responses.create(**kwargs)
            except Exception as exc:  # noqa: BLE001
                if _is_unsupported_effort(exc):
                    last_error = exc
                    continue          # try the next value on the ladder
                raise
            if model not in _EFFORT_FOR_MODEL:
                _EFFORT_FOR_MODEL[model] = effort
                print(f"[llm] {model}: using reasoning effort "
                      f"{effort if effort is not None else '(model default)'}")
            return getattr(response, "output_text", ""), response
        raise RuntimeError(
            f"{model} rejected every reasoning effort value "
            f"{list(_efforts_to_try(model))}: {last_error}")

    params: Dict[str, Any] = dict(model=model, messages=messages, stream=False,
                                  top_p=1, max_tokens=max_tokens)
    if temperature is not None:
        params["temperature"] = temperature
    if seed is not None:
        params["seed"] = seed          # best-effort determinism; the only handle the API offers
    if json_format:
        params["response_format"] = {"type": "json_object"}
    response = client.chat.completions.create(**params)
    return response.choices[0].message.content, response


def llm_generate(prompt: str, model: str = "gpt-4.1", max_tokens: int = 8192,
                 temperature: float | None = 0.0, max_retries: int = 5,
                 json_format: bool = False) -> str:
    """Return the model's text output, retrying transient API failures."""
    global _TOTAL_INPUT_TOKENS, _TOTAL_OUTPUT_TOKENS

    last_error = None
    for attempt in range(max_retries):
        try:
            text, response = _call(prompt, model, max_tokens, temperature,
                                   json_format=json_format)
            usage = _usage(response)
            _TOTAL_INPUT_TOKENS += usage["input_tokens"]
            _TOTAL_OUTPUT_TOKENS += usage["output_tokens"]
            return text or ""
        except Exception as e:  # noqa: BLE001 - retry transient API failures
            last_error = e
            if _is_permanent(e):
                raise
            print(f"[llm] request failed (attempt {attempt + 1}/{max_retries}): {e}")
            time.sleep(1.0 + attempt)
    raise RuntimeError(f"LLM request failed after {max_retries} attempts: {last_error}")


def llm_generate_setup(prompt: str, model: str = "gpt-4o-2024-08-06",
                       max_tokens: int = 8192, temperature: float | None = 0.0,
                       max_retries: int = 5, json_format: bool = False,
                       seed: int | None = None) -> Dict[str, Any]:
    """Same call, returning the text together with the token counts.

    temperature defaults to 0.0, not to a sampling value. Everything that calls
    this is a structured-output step — operator parameter synthesis, schema
    revision, table selection — where a different sample is simply a different
    answer to a question that has one. Running it at 0.3 turned the operator
    search into a stochastic one: the same table and the same declared schema
    produced different chains on different runs.
    """
    global _TOTAL_INPUT_TOKENS, _TOTAL_OUTPUT_TOKENS

    last_error = None
    for attempt in range(max_retries):
        try:
            text, response = _call(prompt, model, max_tokens, temperature,
                                   json_format=json_format, seed=seed)
            usage = _usage(response)
            _TOTAL_INPUT_TOKENS += usage["input_tokens"]
            _TOTAL_OUTPUT_TOKENS += usage["output_tokens"]
            return {
                "text": text or "",
                "input_tokens": usage["input_tokens"],
                "output_tokens": usage["output_tokens"],
                "total_tokens": usage["input_tokens"] + usage["output_tokens"],
                "model": model,
                "retries": attempt,
            }
        except Exception as e:  # noqa: BLE001 - retry transient API failures
            last_error = e
            if _is_permanent(e):
                raise
            print(f"[llm] request failed (attempt {attempt + 1}/{max_retries}): {e}")
            time.sleep(1.0 + attempt)
    raise RuntimeError(f"LLM request failed after {max_retries} attempts: {last_error}")


def get_llm_usage() -> Dict[str, int]:
    """Aggregated token usage across every successful call in this process."""
    return {
        "total_input_tokens": _TOTAL_INPUT_TOKENS,
        "total_output_tokens": _TOTAL_OUTPUT_TOKENS,
    }
