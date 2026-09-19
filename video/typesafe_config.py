import os

from loguru import logger

API_KEY_ENV_VAR = "TYPESAFE_API_KEY"


def mask(secret: str) -> str:
    """Render a secret as a short preview that is safe to log."""
    if len(secret) <= 8:
        return "*" * len(secret)
    return f"{secret[:4]}...{secret[-4:]}"


def get_api_key(required: bool = True) -> str | None:
    """Read the TypeSafe API key from the environment.

    `typesafe_sdk.TypeSafeClient()` reads this same variable automatically, so
    most call sites can just construct the client directly. Use this helper
    when you need to check for the key's presence before that, or want the
    masked log line.

    The key is never logged, only a masked preview. Keep it server-side: do not
    return it to clients or embed it in generated media or responses.
    """
    key = os.environ.get(API_KEY_ENV_VAR, "").strip()
    if not key:
        if required:
            raise RuntimeError(
                f"{API_KEY_ENV_VAR} is not set. Copy .env.example to .env and add "
                "your key, or pass it in the environment."
            )
        logger.warning("{} is not set, TypeSafe features are disabled", API_KEY_ENV_VAR)
        return None
    logger.info("Loaded {} ({})", API_KEY_ENV_VAR, mask(key))
    return key
