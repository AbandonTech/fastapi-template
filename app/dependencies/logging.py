import logging

from fastapi.requests import Request


def use_logging(request: Request) -> logging.Logger:
    """Get a contextual logger for the request

    Expected to be dependency injected into a request handler.

    ```python
    @app.get("/")
    async def index(logger=Depends(use_logging)):
        logger.info("Handling your request")
        ...
    ```
    """
    # Attached in the logging middleware
    return request.state.logger
