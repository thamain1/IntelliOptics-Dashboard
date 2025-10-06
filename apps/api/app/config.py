"""Application configuration for the IntelliOptics API."""

import os
from functools import lru_cache
from typing import Optional

from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Runtime configuration loaded from environment variables."""

    app_name: str = Field(default="IntelliOptics API")
    app_version: str = Field(default="0.1.0")

    postgres_url: str = Field(default="")
    servicebus_connection: str = Field(default="")
    blob_account: str = Field(default="")
    blob_image_container: str = Field(default="images")
    blob_models_container: str = Field(default="models")

    sendgrid_api_key: Optional[str] = Field(default=None)
    twilio_account_sid: Optional[str] = Field(default=None)
    twilio_auth_token: Optional[str] = Field(default=None)

    keyvault_uri: Optional[str] = Field(default=None)
    appinsights_connection_string: Optional[str] = Field(default=None)
    jwt_secret: str = Field(default="change-me")

    image_query_wait_timeout_seconds: float = Field(default=10.0, ge=0.0)
    image_query_wait_poll_seconds: float = Field(default=0.5, ge=0.0)

    
    def database_url(self) -> str:
        """Return the configured SQLAlchemy database URL."""

        if self.postgres_url.startswith("postgresql://"):
            return self.postgres_url.replace("postgresql://", "postgresql+psycopg://", 1)
        return self.postgres_url

    @classmethod
    def from_env(cls) -> "Settings":
        """Create a settings object using environment variables."""

        return cls(
            postgres_url=os.getenv("POSTGRES_URL", ""),
            servicebus_connection=os.getenv("SERVICEBUS_CONNECTION", ""),
            blob_account=os.getenv("BLOB_ACCOUNT", ""),
            blob_image_container=os.getenv("BLOB_IMAGE_CONTAINER", "images"),
            blob_models_container=os.getenv("BLOB_MODELS_CONTAINER", "models"),
            sendgrid_api_key=os.getenv("SENDGRID_API_KEY"),
            twilio_account_sid=os.getenv("TWILIO_ACCOUNT_SID"),
            twilio_auth_token=os.getenv("TWILIO_AUTH_TOKEN"),
            keyvault_uri=os.getenv("KEYVAULT_URI"),
            appinsights_connection_string=os.getenv("APPINSIGHTS_CONNECTION_STRING"),
            jwt_secret=os.getenv("JWT_SECRET", "change-me"),
            image_query_wait_timeout_seconds=float(
                os.getenv("IMAGE_QUERY_WAIT_TIMEOUT_SECONDS", 10.0)
            ),
            image_query_wait_poll_seconds=float(
                os.getenv("IMAGE_QUERY_WAIT_POLL_SECONDS", 0.5)
            ),
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached settings object."""

    return Settings.from_env()


settings = get_settings()
