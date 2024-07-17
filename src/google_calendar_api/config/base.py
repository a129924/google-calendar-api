from pydantic_settings import BaseSettings as PydanticBaseSettings
from pydantic_settings import (
    JsonConfigSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)
from typing_extensions import Self, override

__all__ = ["BaseSettings", "JsonBaseSettings"]


class BaseSettings(PydanticBaseSettings):
    @classmethod
    def set_model_config(cls, model_config: SettingsConfigDict) -> type[Self]:
        cls.model_config = model_config

        return cls


class JsonBaseSettings(BaseSettings):
    @classmethod
    @override
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (JsonConfigSettingsSource(settings_cls),)

    ...
