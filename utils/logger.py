"""
SDK Internal Logger

Provides logging for the SDK. Falls back to standard Python logging if external
logger is not available. This makes the SDK portable.

Dependencies: logging (standard library)
"""

import logging

# Try to import external logger if available (when SDK is used within parent project)
try:
    from src.utils.logger import log_with_context, setup_logger

    HAS_EXTERNAL_LOGGER = True
except ImportError:
    HAS_EXTERNAL_LOGGER = False

    # Fallback to standard Python logging
    def setup_logger(name: str, log_level: str = "INFO") -> logging.Logger:
        """
        Fallback logger setup using standard Python logging.

        Args:
            name: Logger name (usually __name__)
            log_level: Log level string (DEBUG, INFO, WARNING, ERROR, CRITICAL)

        Returns:
            Python logger instance
        """
        logger = logging.getLogger(name)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        # Set log level
        numeric_level = getattr(logging, log_level.upper(), logging.INFO)
        logger.setLevel(numeric_level)

        return logger

    def log_with_context(
        logger: logging.Logger,
        level: str,
        message: str,
        source: str | None = None,
        action: str | None = None,
        component: str | None = None,
        **kwargs,
    ):
        """
        Fallback context logging using standard Python logging.

        Args:
            logger: Logger instance
            level: Log level (debug, info, warning, error, critical)
            message: Log message
            source: Source identifier (optional)
            action: Action identifier (optional)
            component: Component identifier (optional)
            **kwargs: Additional context (unused in fallback)
        """
        # Build context string if provided
        context_parts = []
        if source:
            context_parts.append(f"source={source}")
        if action:
            context_parts.append(f"action={action}")
        if component:
            context_parts.append(f"component={component}")

        context_str = f" [{', '.join(context_parts)}]" if context_parts else ""
        full_message = f"{message}{context_str}"

        # Log at appropriate level
        log_method = getattr(logger, level.lower(), logger.info)
        log_method(full_message)


# Re-export for convenience
__all__ = ["setup_logger", "log_with_context", "HAS_EXTERNAL_LOGGER"]
