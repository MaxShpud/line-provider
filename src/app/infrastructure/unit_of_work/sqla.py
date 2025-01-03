from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession
)

from app.infrastructure.repositories.sqla.event import EventRepository
from app.app_layer.interfaces.unit_of_work.sql import IUnitOfWork


class Uow(IUnitOfWork):
    """
    Provides a unit of work pattern for managing transactions and repositories in
    an asynchronous SQLAlchemy session.
    """

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def __aenter__(self) -> IUnitOfWork:
        self._session = self._session_factory()
        self.event = EventRepository(session=self._session)

        return await super().__aenter__()

    async def commit(self) -> None:
        """Commits the changes made in the session."""

        await self._session.commit()

    async def rollback(self) -> None:
        """Rolls back the changes made in the session."""

        await self._session.rollback()

    async def shutdown(self) -> None:
        """Closes the session."""

        await self._session.close()