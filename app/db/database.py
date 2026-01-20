from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from ..core.config import get_settings
from ..db.models import Base


class Database:
    def __init__(self):
        self._settings = get_settings()
        self._engine: AsyncEngine = self._create_engine()
        self._session_factory: sessionmaker = self._create_session_factory(self._engine)
        self._tables_created = False  # флаг, чтобы создать таблицы только один раз
        self._initialized = True

    def _create_engine(self) -> AsyncEngine:
        return create_async_engine(self._settings.database_url, echo=self._settings.debug, future=True)

    def _create_session_factory(self, engine) -> sessionmaker:
        return sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    @classmethod
    async def init_tables(cls):
        instance = cls()
        async with instance._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @asynccontextmanager
    async def get_session(self) -> AsyncSession:
        """Возвращает новую сессию на каждый запрос и закрывает её после использования."""
        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()  # опционально, можно делать коммит в сервисе
            except:
                await session.rollback()
                raise
            finally:
                await session.close()
