"""Polza AI image generation backend.

Exposes Polza AI's image generation models (FLUX 2 Pro/Flex, GPT Image 1.5,
Seedream 4.5/4, Qwen Image 2, Yandex Art, and more) as an
:class:`ImageGenProvider` implementation.

Polza AI uses an async API pattern:
1. POST /api/v1/images/generations → returns ``requestId``
2. GET /api/v1/images/{requestId} → poll until ``status == "COMPLETED"``

API key is read from ``POLZA_API_KEY`` env var.
"""

from __future__ import annotations

import json
import logging
import os
import time
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional, Tuple

from agent.image_gen_provider import (
    DEFAULT_ASPECT_RATIO,
    ImageGenProvider,
    error_response,
    resolve_aspect_ratio,
    save_url_image,
    success_response,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

POLZA_BASE_URL = "https://polza.ai/api/v1"
POLL_INTERVAL = 2.0  # seconds between poll attempts
MAX_POLL_ATTEMPTS = 60  # ~2 minutes max wait
GENERATE_TIMEOUT = 120  # per-request HTTP timeout

# ---------------------------------------------------------------------------
# Model catalog
# ---------------------------------------------------------------------------

# Map Hermes aspect_ratio (landscape / square / portrait) to Polza's format.
# Per-model overrides in _MODEL_ASPECT_MAP below.
_DEFAULT_ASPECT_MAP: Dict[str, str] = {
    "landscape": "16:9",
    "square": "1:1",
    "portrait": "9:16",
}

# Models with limited aspect ratio support — need non-standard mapping.
_MODEL_ASPECT_MAP: Dict[str, Dict[str, str]] = {
    "openai/gpt-image-1.5": {
        "landscape": "3:2",  # no 16:9 support
        "square": "1:1",
        "portrait": "2:3",
    },
    "openai/gpt-5-image": {
        "landscape": "3:2",
        "square": "1:1",
        "portrait": "2:3",
    },
    "x-ai/grok-imagine-image": {
        "landscape": "3:2",
        "square": "1:1",
        "portrait": "2:3",
    },
}

# Models that support ``image_resolution`` (1K / 2K / 4K).
_MODELS_WITH_RESOLUTION: Dict[str, str] = {
    "black-forest-labs/flux.2-pro": "1K",
    "black-forest-labs/flux.2-flex": "1K",
    "bytedance/seedream-4": "1K",
    "openai/gpt-5.4-image-2": "1K",
    "google/gemini-3.1-flash-image-preview": "1K",
    "google/gemini-3-pro-image-preview": "1K",
}

# Models that support ``quality`` parameter (basic / high).
_MODELS_WITH_QUALITY: Dict[str, str] = {
    "bytedance/seedream-4.5": "basic",
    "bytedance/seedream-5-lite": "basic",
    "openai/gpt-image-1.5": "medium",
}

# Models that support ``output_format``.
_MODELS_WITH_OUTPUT_FORMAT = {
    "qwen/image", "qwen/image-2",
    "google/gemini-3.1-flash-image-preview",
    "google/gemini-3-pro-image-preview",
    "google/gemini-2.5-flash-image",
}

# Price descriptions for each model (in RUB, from Polza API).
_MODEL_PRICES: Dict[str, str] = {
    "black-forest-labs/flux.2-pro": "5 ₽ (1K) / 7 ₽ (2K)",
    "black-forest-labs/flux.2-flex": "14 ₽ (1K) / 24 ₽ (2K)",
    "bytedance/seedream-4.5": "5 ₽",
    "bytedance/seedream-4": "3 ₽",
    "bytedance/seedream": "2.50 ₽",
    "bytedance/seedream-5-lite": "4 ₽",
    "openai/gpt-image-1.5": "3 ₽ (medium) / 16.50 ₽ (high)",
    "openai/gpt-5-image": "4.50 ₽",
    "openai/gpt-5.4-image-2": "4 ₽ (1K) / 7 ₽ (2K) / 11 ₽ (4K)",
    "qwen/image-2": "4 ₽",
    "qwen/image": "2.25–3 ₽",
    "yandex/yandex-art": "2.91 ₽",
    "x-ai/grok-imagine-image": "2.50 ₽",
    "tongyi-mai/z-image": "1.40 ₽",
    "google/gemini-2.5-flash-image": "2.90 ₽",
    "google/gemini-3.1-flash-image-preview": "4.80 ₽ (1K) / 7.20 ₽ (2K) / 10.80 ₽ (4K)",
    "google/gemini-3-pro-image-preview": "13.50 ₽ (1K/2K) / 18 ₽ (4K)",
}

_MODELS: Dict[str, Dict[str, Any]] = {
    # ── FLUX ──────────────────────────────────────────────────
    "black-forest-labs/flux.2-pro": {
        "display": "FLUX 2 Pro",
        "speed": "~6s",
        "strengths": "Studio photorealism, crisp text",
        "price": "5 ₽ (1K) / 7 ₽ (2K)",
    },
    "black-forest-labs/flux.2-flex": {
        "display": "FLUX 2 Flex",
        "speed": "~4s",
        "strengths": "Fast, flexible, good quality",
        "price": "14 ₽ (1K) / 24 ₽ (2K)",
    },
    # ── Seedream ───────────────────────────────────────────────
    "bytedance/seedream-4.5": {
        "display": "Seedream 4.5",
        "speed": "~10s",
        "strengths": "Wide ratio support (1:1 to 21:9), Basic=2K, High=4K",
        "price": "5 ₽",
    },
    "bytedance/seedream-4": {
        "display": "Seedream 4",
        "speed": "~8s",
        "strengths": "Good quality, 1K/2K/4K, versatile ratios",
        "price": "3 ₽",
    },
    "bytedance/seedream-5-lite": {
        "display": "Seedream 5 Lite",
        "speed": "~8s",
        "strengths": "Basic=2K, High=3K",
        "price": "4 ₽",
    },
    "bytedance/seedream": {
        "display": "Seedream 3.0",
        "speed": "~6s",
        "strengths": "Fast, reliable, cheapest Seedream",
        "price": "2.50 ₽",
    },
    # ── OpenAI ─────────────────────────────────────────────────
    "openai/gpt-image-1.5": {
        "display": "GPT Image 1.5",
        "speed": "~15s",
        "strengths": "Strong prompt adherence, medium/high quality",
        "price": "3 ₽ (medium) / 16.50 ₽ (high)",
    },
    "openai/gpt-5-image": {
        "display": "GPT-5 Image",
        "speed": "~15s",
        "strengths": "Latest OpenAI image gen, text+image output",
        "price": "4.50 ₽",
    },
    "openai/gpt-5.4-image-2": {
        "display": "GPT-5.4 Image 2",
        "speed": "~15s",
        "strengths": "Multi-resolution (1K/2K/4K), wide ratio support",
        "price": "4 ₽ (1K) / 7 ₽ (2K) / 11 ₽ (4K)",
    },
    # ── Google Gemini (Nano Banana) ─────────────────────────────
    "google/gemini-3.1-flash-image-preview": {
        "display": "Nano Banana 2 (Gemini 3.1 Flash)",
        "speed": "~5s",
        "strengths": "Typographic precision, up to 4K, 4-6s latency",
        "price": "4.80 ₽ (1K) / 7.20 ₽ (2K) / 10.80 ₽ (4K)",
    },
    "google/gemini-3-pro-image-preview": {
        "display": "Nano Banana Pro (Gemini 3 Pro)",
        "speed": "~8s",
        "strengths": "Reasoning depth, world-aware photorealism, 1K/2K/4K",
        "price": "13.50 ₽ (1K/2K) / 18 ₽ (4K)",
    },
    "google/gemini-2.5-flash-image": {
        "display": "Nano Banana (Gemini 2.5 Flash)",
        "speed": "~4s",
        "strengths": "Fastest Gemini image gen, 30+ aspect ratios",
        "price": "2.90 ₽",
    },
    # ── Qwen ────────────────────────────────────────────────────
    "qwen/image-2": {
        "display": "Qwen Image 2",
        "speed": "~12s",
        "strengths": "LLM-based, complex scene understanding",
        "price": "4 ₽",
    },
    "qwen/image": {
        "display": "Qwen Image",
        "speed": "~8s",
        "strengths": "Price varies by aspect ratio (2.25–3 ₽)",
        "price": "2.25–3 ₽",
    },
    # ─── Other ───────────────────────────────────────────────────
    "yandex/yandex-art": {
        "display": "Yandex Art",
        "speed": "~10s",
        "strengths": "Artistic styles, painterly output",
        "price": "2.91 ₽",
    },
    "x-ai/grok-imagine-image": {
        "display": "Grok Imagine (via Polza)",
        "speed": "~5s",
        "strengths": "Fast, 1:1/2:3/3:2 only",
        "price": "2.50 ₽",
    },
    "tongyi-mai/z-image": {
        "display": "Z-Image (Tongyi)",
        "speed": "~5s",
        "strengths": "Cheapest model — 1.40 ₽ per image",
        "price": "1.40 ₽",
    },
}

DEFAULT_MODEL = "bytedance/seedream-4.5"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _get_api_key() -> Optional[str]:
    """Return POLZA_API_KEY from env, or None."""
    return os.environ.get("POLZA_API_KEY") or None


def _polza_api(
    method: str,
    endpoint: str,
    payload: Optional[Dict[str, Any]] = None,
) -> Tuple[int, Any]:
    """Make an HTTP request to the Polza AI API.

    Returns ``(status_code, parsed_json)`` on success, or
    ``(status_code, error_dict)`` on failure.
    """
    key = _get_api_key()
    if not key:
        return 401, {"error": "POLZA_API_KEY is not set"}

    url = f"{POLZA_BASE_URL}/{endpoint}"
    data = json.dumps(payload).encode() if payload else None

    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method=method,
    )

    try:
        with urllib.request.urlopen(req, timeout=GENERATE_TIMEOUT) as resp:
            body = resp.read()
            if body:
                return resp.status, json.loads(body)
            return resp.status, {}
    except urllib.error.HTTPError as e:
        body = e.read()
        try:
            return e.code, json.loads(body)
        except (json.JSONDecodeError, ValueError):
            return e.code, {"raw": body.decode(errors="replace")[:500]}
    except urllib.error.URLError as e:
        return 0, {"error": f"Connection failed: {e.reason}"}
    except Exception as e:
        return 0, {"error": str(e)}


def _resolve_polza_aspect_ratio(model_id: str, hermes_ratio: str) -> str:
    """Map Hermes aspect_ratio to Polza's ``aspectRatio`` parameter."""
    model_map = _MODEL_ASPECT_MAP.get(model_id)
    if model_map:
        return model_map.get(hermes_ratio, _DEFAULT_ASPECT_MAP.get(hermes_ratio, "1:1"))
    return _DEFAULT_ASPECT_MAP.get(hermes_ratio, "1:1")


def _poll_for_result(request_id: str) -> Tuple[bool, Dict[str, Any]]:
    """Poll ``GET /api/v1/images/{request_id}`` until COMPLETED or FAILED.

    Returns ``(success, result_dict)``.
    """
    for attempt in range(MAX_POLL_ATTEMPTS):
        status, data = _polza_api("GET", f"images/{request_id}")
        if status != 200:
            logger.warning(
                "Polza poll attempt %d returned %d: %s",
                attempt, status, data,
            )
            time.sleep(POLL_INTERVAL)
            continue

        poll_status = data.get("status", "").upper()
        if poll_status == "COMPLETED":
            return True, data
        if poll_status in ("FAILED", "ERROR"):
            err_msg = data.get("error", data.get("message", "Unknown error"))
            return False, {"error": err_msg}
        if poll_status == "PENDING":
            time.sleep(POLL_INTERVAL)
            continue

        # Unknown status — wait and retry
        logger.debug("Polza poll: unknown status %r for %s", poll_status, request_id)
        time.sleep(POLL_INTERVAL)

    return False, {"error": f"Polling timed out after {MAX_POLL_ATTEMPTS * POLL_INTERVAL:.0f}s"}


def _cache_image(url: str, prefix: str = "polza") -> Optional[str]:
    """Download and cache an image URL, returning the local path.

    Falls back to the bare URL on any caching error.
    """
    try:
        saved_path = save_url_image(url, prefix=prefix)
        return str(saved_path)
    except Exception as exc:
        logger.warning("Could not cache Polza image %s: %s", url, exc)
        return url


# ---------------------------------------------------------------------------
# Provider
# ---------------------------------------------------------------------------


class PolzaImageGenProvider(ImageGenProvider):
    """Polza AI image generation backend."""

    @property
    def name(self) -> str:
        return "polza"

    @property
    def display_name(self) -> str:
        return "Polza AI"

    def is_available(self) -> bool:
        return _get_api_key() is not None

    def list_models(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": model_id,
                "display": meta.get("display", model_id),
                "speed": meta.get("speed", ""),
                "strengths": meta.get("strengths", ""),
            }
            for model_id, meta in _MODELS.items()
        ]

    def default_model(self) -> Optional[str]:
        return DEFAULT_MODEL

    def get_setup_schema(self) -> Dict[str, Any]:
        return {
            "name": "Polza AI",
            "badge": "paid",
            "tag": (
                "FLUX 2 Pro, GPT Image 1.5, Seedream 4.5, Qwen Image 2, "
                "Yandex Art, and more via polza.ai"
            ),
            "env_vars": [
                {
                    "key": "POLZA_API_KEY",
                    "prompt": "Polza AI API key",
                    "url": "https://polza.ai",
                },
            ],
        }

    def generate(
        self,
        prompt: str,
        aspect_ratio: str = DEFAULT_ASPECT_RATIO,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        prompt = (prompt or "").strip()
        aspect = resolve_aspect_ratio(aspect_ratio)

        if not prompt:
            return error_response(
                error="Prompt is required and must be a non-empty string",
                error_type="invalid_argument",
                provider="polza",
                aspect_ratio=aspect,
            )

        key = _get_api_key()
        if not key:
            return error_response(
                error=(
                    "POLZA_API_KEY not set. Run `hermes tools` → Image "
                    "Generation → Polza AI to configure, or add it to .env."
                ),
                error_type="auth_required",
                provider="polza",
                aspect_ratio=aspect,
            )

        # Resolve model from config or env
        model_id = (
            os.environ.get("POLZA_IMAGE_MODEL")
            or kwargs.get("model")
            or self.default_model()
            or DEFAULT_MODEL
        )

        # Build request payload with model-specific parameters
        polza_aspect = _resolve_polza_aspect_ratio(model_id, aspect)
        payload: Dict[str, Any] = {
            "model": model_id,
            "prompt": prompt,
            "n": 1,
            "aspectRatio": polza_aspect,
        }

        # Models that support ``image_resolution`` (1K / 2K / 4K)
        if model_id in _MODELS_WITH_RESOLUTION:
            payload["image_resolution"] = _MODELS_WITH_RESOLUTION[model_id]

        # Models that support ``quality`` (basic / high / medium)
        if model_id in _MODELS_WITH_QUALITY:
            payload["quality"] = _MODELS_WITH_QUALITY[model_id]

        # Models that support ``output_format``
        if model_id in _MODELS_WITH_OUTPUT_FORMAT:
            payload["output_format"] = "jpeg"

        logger.debug(
            "Polza image gen: model=%s aspect=%s payload=%s",
            model_id, aspect, payload,
        )

        # Step 1: Submit generation request
        create_status, create_data = _polza_api("POST", "images/generations", payload)

        if create_status not in (200, 201):
            err_msg = create_data.get("error", {}).get(
                "message",
                create_data.get("error", str(create_data)),
            )
            logger.error("Polza create failed (%d): %s", create_status, err_msg)
            return error_response(
                error=f"Polza AI generation request failed ({create_status}): {err_msg}",
                error_type="api_error",
                provider="polza",
                model=model_id,
                prompt=prompt,
                aspect_ratio=aspect,
            )

        request_id = create_data.get("requestId")
        if not request_id:
            return error_response(
                error="Polza AI returned no requestId",
                error_type="invalid_response",
                provider="polza",
                model=model_id,
                prompt=prompt,
                aspect_ratio=aspect,
            )

        # Step 2: Poll for completion
        success, poll_data = _poll_for_result(request_id)
        if not success:
            return error_response(
                error=f"Polza AI generation failed or timed out: {poll_data.get('error', 'unknown')}",
                error_type="generation_failed",
                provider="polza",
                model=model_id,
                prompt=prompt,
                aspect_ratio=aspect,
            )

        # Step 3: Extract image URL
        image_url = poll_data.get("url") or (
            poll_data.get("images", [None])[0] if poll_data.get("images") else None
        )

        if not image_url:
            return error_response(
                error="Polza AI returned no image URL in completed response",
                error_type="empty_response",
                provider="polza",
                model=model_id,
                prompt=prompt,
                aspect_ratio=aspect,
            )

        # Step 4: Cache the image locally (Polza URLs may expire)
        image_ref = _cache_image(image_url, prefix=f"polza_{model_id.split('/')[-1]}")

        return success_response(
            image=image_ref,
            model=model_id,
            prompt=prompt,
            aspect_ratio=aspect,
            provider="polza",
            extra={
                "request_id": request_id,
                "polza_aspect_ratio": polza_aspect,
            },
        )


# ---------------------------------------------------------------------------
# Plugin registration
# ---------------------------------------------------------------------------


def register(ctx: Any) -> None:
    """Register this provider with the image gen registry."""
    ctx.register_image_gen_provider(PolzaImageGenProvider())
