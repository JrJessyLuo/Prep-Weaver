"""The slice of the original `prep_utils` package the engine actually uses.

`bounded_explore_loop` and `test_param_synthesis` import
`llm_generate_setup` and `timed_llm_generate` from `prep_utils`, lazily, inside
the function that calls them. Providing that name here keeps those call sites
untouched while routing every request through Prep-Weaver's shared client, so
there is one place that holds credentials and one place that handles retries.

The lazy import is also what makes the per-task token meter work: `synthesize`
rebinds `prep_utils.llm_generate_setup` to a metered wrapper, and because the
engine resolves the name at CALL time rather than import time, it picks the
wrapper up.
"""

from __future__ import annotations

import time
from typing import Any, Dict

from common.llm_client import llm_generate_setup as _client_generate


def llm_generate_setup(prompt: str, model: str = "gpt-4o-2024-08-06",
                       json_format: bool = False, temperature=0.0,
                       **kwargs) -> Dict[str, Any]:
    """One LLM call, returning {text, input_tokens, output_tokens, ...}.

    A failure is returned rather than raised, matching the original contract:
    the search treats a failed parameter synthesis as one dead candidate and
    carries on with the rest of the beam. `require_text` is what turns an empty
    reply into a diagnosable error at the point that needs the text.
    """
    try:
        return _client_generate(prompt, model=model, json_format=json_format,
                                temperature=temperature, **kwargs)
    except Exception as exc:  # noqa: BLE001
        return {"text": "", "error": f"{type(exc).__name__}: {exc}",
                "input_tokens": 0, "output_tokens": 0, "total_tokens": 0,
                "model": model}


def timed_llm_generate(generate_fn, prompt: str, **kwargs):
    """(response, usage) with the wall-clock time of the call attached."""
    start = time.perf_counter()
    resp = generate_fn(prompt, **kwargs)
    return resp, {
        "input_tokens": int(resp.get("input_tokens") or 0),
        "output_tokens": int(resp.get("output_tokens") or 0),
        "total_tokens": int(resp.get("total_tokens") or 0),
        "elapsed_seconds": time.perf_counter() - start,
        "raw_usage": resp.get("usage") or {},
    }


def require_text(resp: dict, what: str = "LLM call") -> str:
    """The reply text, or a failure that says why.

    `llm_generate_setup` returns {"text": "", "error": ...} once it exhausts its
    retries, and a caller that runs json.loads on that empty string gets

        JSONDecodeError: Expecting value: line 1 column 1 (char 0)

    which names neither the API nor the reason — a run whose credits ran out
    mid-way then looks exactly like a run where the model declined to answer.
    Raising here keeps the attribution.
    """
    text = (resp or {}).get("text") or ""
    if not text.strip():
        raise RuntimeError(f"{what} returned no text: {(resp or {}).get('error') or resp}")
    return text
