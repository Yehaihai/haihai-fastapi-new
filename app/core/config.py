
import secrets
import warnings
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    BeforeValidator,
    HttpUrl,
    PostgresDsn,
    computed_field,
    model_validator,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


def parse_cors(v: Any) -> list[str] | str:
    """解析CORS配置，支持字符串或列表格式"""
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    """应用配置类，管理所有环境变量和系统设置"""

    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    # 基础配置
    RUNINDOCKER: bool = True
    USER_HOME_PAGE_TITLE: str = "🍉 24小时等待你的分享，负责整理、体会与反馈。"
    DEFAULT_AVATAR: str = "prod/default_avatar.png"
    DEFAULT_PROFILE_PIC: str = "prod/default_profile_picture.png"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30 * 3 # 3 个月过期
    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    # 用户系统配置
    DAILY_TOKEN_LIMIT: int = 12999
    INVITE_CODE_INPUT_REWARD: int = 2999
    INVITE_CODE_SHARE_REWARD: int = 3999

    # CORS配置
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    # 项目配置
    PROJECT_NAME: str
    SENTRY_DSN: HttpUrl | None = None

    # 数据库配置
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = ""

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """构建PostgreSQL连接URI"""
        return f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # 超级用户配置
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str
    FIRST_SUPERUSER_PHONE_NUMBER: str

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        """检查关键配置项是否使用了默认值"""
        if value == "必须设置":
            message = f'{var_name} 是 "必须设置", 为了安全，必须设置这些值.'
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        """验证关键安全配置"""
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        self._check_default_secret("POSTGRES_PASSWORD", self.POSTGRES_PASSWORD)
        self._check_default_secret(
            "FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD
        )
        return self


settings = Settings()  # type: ignore
