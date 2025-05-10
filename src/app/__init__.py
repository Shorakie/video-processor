from fastapi import FastAPI

from app.api import router as api_router
from app.core.config import Environments, settings
from app.core.logging import configure_logging
from app.metadata import metadata


def create_app() -> FastAPI:
    """Factory function that creates and configures a FastAPI application instance.

    Initializes the application with proper configuration based on environment settings,
    sets up logging, and includes all API routes from the main router.

    Returns:
        FastAPI: A configured FastAPI application instance with the following features:
        - Application title from settings.APP.NAME
        - Application description from settings.APP.DESCRIPTION
        - Application version from settings.APP.VERSION
        - Application contact information from settings.APP.CONTACT_*
        - Debug mode enabled if environment is LOCAL
        - All API routes included from app.api.router
        - Pre-configured logging

    Example:
        ```python
        from app.main import create_app
        app = create_app()
        ```

    Note:
        The debug mode is automatically set based on the environment configuration.
        In LOCAL environment, debug features like automatic reload and detailed
        error messages will be enabled.

    Side Effects:
        - Configures the global logging system via configure_logging()
        - Registers all API endpoints from the included router
    """
    configure_logging()

    app = FastAPI(
        title=settings.APP.NAME,
        description=settings.APP.DESCRIPTION,
        version=settings.APP.VERSION,
        contact={
            "name": settings.APP.CONTACT_NAME,
            "email": settings.APP.CONTACT_EMAIL,
            "url": settings.APP.CONTACT_URL,
        },
        debug=settings.ENVIRONMENT == Environments.LOCAL,
    )

    # add api router
    app.include_router(api_router)

    return app
