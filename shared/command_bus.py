from __future__ import annotations

from command_coach.adapter import DatabaseTransactionAsync
from command_coach.bus import async_command_bus_maker
from command_coach.command import Command
from command_coach.plugin import CommandCoachPluginAsync
from command_coach.plugin_included import LockingPluginAsync, TransactionPluginAsync

from shared.db import database, Database


class DatabaseAdapter(DatabaseTransactionAsync):
    def __init__(self, db: Database):
        self._session = db.current_session()

    async def begin_transaction(self):
        await self._session.begin()

    async def commit_transaction(self):
        await self._session.commit()

    async def rollback_transaction(self):
        await self._session.rollback()


bus = async_command_bus_maker([
    LockingPluginAsync(),
    TransactionPluginAsync(DatabaseAdapter(database)),
])


class CloseQueryTransactionPlugin(CommandCoachPluginAsync):
    def __init__(self, async_database: DatabaseTransactionAsync):
        self.database: DatabaseTransactionAsync = async_database

    async def before_handle(self, command: Command):
        ...

    async def handle_failed(self):
        ...

    async def after_handle(self, command: Command):
        await self.database.commit_transaction()


query_bus = async_command_bus_maker([
    CloseQueryTransactionPlugin(DatabaseAdapter(database))
])
