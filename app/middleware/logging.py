import logging

from fastapi import FastAPI
from fastapi.requests import HTTPConnection
from starlette.types import ASGIApp, Receive, Scope, Send
from uvicorn.logging import ColourizedFormatter


class _ContextFilter(logging.Filter):
    """Attaches request context to logs."""

    def __init__(self, remote: str, request_line: str):
        super().__init__("request-context")
        self.remote = remote
        self.request_line = request_line

    def filter(self, record) -> bool:
        record.levelprefix = record.levelname
        record.client_addr = self.remote
        record.request_line = self.request_line
        return True


class LoggingMiddleware:
    """Configure logging and attach a contextual logger to each request's state."""

    def __init__(self, app: ASGIApp, fastapi: FastAPI) -> None:
        self.asgi = app
        self.fastapi = fastapi
        self._configure_logging()

    def _configure_logging(self) -> None:
        app_logger = logging.getLogger(self.fastapi.title)

        # Steal log handler and log level from uvicorn
        uvicorn_logger = logging.getLogger("uvicorn.access")
        app_logger.setLevel(uvicorn_logger.level)
        # This should always exist as we only use uvicorn
        use_color = uvicorn_logger.handlers[0].formatter.use_colors  # type: ignore[reportOptionalMemberAccess]

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(
            ColourizedFormatter(
                "%(levelprefix)s %(client_addr)s - \"%(request_line)s\" %(message)s",
                use_colors=use_color
            ))
        app_logger.addHandler(stream_handler)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Add a logger to request state that inherits from the uvicorn root logger."""
        if scope["type"] in ["http", "websocket"]:
            connection = HTTPConnection(scope)
            connection.state.logger = logging.getLogger(f"{self.fastapi.title}.{scope['path']}")

            request_line = f"{scope['method']} {scope['path']} HTTP/{scope['http_version']}"
            remote_client = f"{scope['client'][0]}:{scope['client'][1]}"
            connection.state.logger.addFilter(_ContextFilter(remote_client, request_line))

        await self.asgi(scope, receive, send)
