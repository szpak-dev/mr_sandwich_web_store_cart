from __future__ import annotations

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from shared.config import settings


class Database:
    def __init__(self, dsn: str):
        self._engine = create_async_engine(
            dsn,
            echo=False,
        )

        self._session: AsyncSession = AsyncSession(
            bind=self._engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

    def current_session(self) -> AsyncSession:
        return self._session


database = Database(settings['DATABASE_DSN'])
