import os
import aiosqlite
from typing import List, Optional, Tuple
from contextlib import asynccontextmanager

from base.logger import Logger
from base.config import BotConfig


class DatabaseConnectionHandler:
    def __init__(self) -> None:
        self.logger = Logger(__name__).get_logger()
        self.config = BotConfig()
        self.db = self.config.DATABASE
        self.connection: Optional[aiosqlite.Connection] = None


    async def create_database(self) -> None:

        if os.path.exists(self.db):
            self.logger.debug(f"Database already exists at: {self.db}")
            return

        await self.create_connection()
        try:
            async with self.connection.cursor() as cursor:
                # Create users table
                await cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        discord_id INTEGER UNIQUE,
                        username TEXT NOT NULL,
                        discriminator TEXT NOT NULL
                    )
                    """
                )

                await cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS tickets (
                        uuid TEXT UNIQUE,
                        user_id INTEGER,
                        category TEXT NOT NULL,
                        channel_id INTEGER,
                        guild_id INTEGER
                    ) 
                    """
                )


                await self.connection.commit()
                self.logger.debug("Database created successfully")

        except aiosqlite.Error as e:
            self.logger.error("Error while creating database", exc_info=e)

        finally:
            await self.close_connection()

    @asynccontextmanager
    async def get_db_connection(self):
        await self.create_connection()
        try:
            yield self.connection
        finally:
            await self.close_connection()

    async def create_connection(self) -> None:
        try:
            if self.connection is None:
                self.connection = await aiosqlite.connect(self.db)
                self.logger.debug(f"Connected to database {self.db}")
            else:
                self.logger.debug(f"Connection already exists at: {self.db}")
        except aiosqlite.Error as e:
            self.logger.error("Error while connecting to database", exc_info=e)

    async def close_connection(self) -> None:
        try:
            if self.connection:
                await self.connection.close()
                self.logger.debug(f"Closed connection to database: {self.db}")
                self.connection = None
            else:
                self.logger.debug(f"No connection to close: {self.db}")
        except aiosqlite.Error as e:
            self.logger.error("Error closing connection", exc_info=e)

class Database(DatabaseConnectionHandler):
    def __init__(self) -> None:
        super().__init__()
        self.db_logger = Logger("Database").get_logger()

    async def add_user(self, discord_id: int, username: str, discriminator: str) -> None:
        async with self.get_db_connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    await cursor.execute(
                        """
                        INSERT INTO users (discord_id, username, discriminator)
                        VALUES (?, ?, ?)
                        """,
                        (discord_id, username, discriminator)
                    )
                    await connection.commit()
                    self.db_logger.debug(f"User {username} added to database")
                except aiosqlite.Error as e:
                    self.db_logger.error("Error adding user to database", exc_info=e)

    async def get_user(self, discord_id: int) -> Optional[Tuple[int, str, str]]:
        async with self.get_db_connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    await cursor.execute(
                        """
                        SELECT * FROM users WHERE discord_id = ?
                        """,
                        (discord_id,)
                    )
                    user = await cursor.fetchone()
                    return user
                except aiosqlite.Error as e:
                    self.db_logger.error("Error getting user from database", exc_info=e)
                    return None

    async def check_user(self, discord_id: int) -> bool:
        async with self.get_db_connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    await cursor.execute(
                        """
                        SELECT * FROM users WHERE discord_id = ?
                        """,
                        (discord_id,)
                    )
                    user = await cursor.fetchone()
                    return True if user else False
                except aiosqlite.Error as e:
                    self.db_logger.error("Error checking user in database", exc_info=e)
                    return False


    async def remove_user(self, discord_id: int) -> None:
        async with self.get_db_connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    await cursor.execute(
                        """
                        DELETE FROM users WHERE discord_id = ?
                        """,
                        (discord_id,)
                    )
                    await connection.commit()
                    self.db_logger.debug(f"User {discord_id} removed from database")
                except aiosqlite.Error as e:
                    self.db_logger.error("Error removing user from database", exc_info=e)

    async def add_ticket(self, uuid: str, user_id: int, category: str, channel_id: int, guild_id: int) -> None:
        async with self.get_db_connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    await cursor.execute(
                        """
                        INSERT INTO tickets (uuid, user_id, category, channel_id, guild_id)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (uuid, user_id, category, channel_id, guild_id)
                    )
                    await connection.commit()
                    self.db_logger.debug(f"Ticket {uuid} added to database")
                except aiosqlite.Error as e:
                    self.db_logger.error("Error adding ticket to database", exc_info=e)

    async def get_ticket(self, uuid: str) -> Optional[Tuple[str, int, str, int, int]]:
        async with self.get_db_connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    await cursor.execute(
                        """
                        SELECT * FROM tickets WHERE uuid = ?
                        """,
                        (uuid,)
                    )
                    ticket = await cursor.fetchone()
                    return ticket
                except aiosqlite.Error as e:
                    self.db_logger.error("Error getting ticket from database", exc_info=e)
                    return None

    async def check_ticket(self, uuid: str) -> bool:
        async with self.get_db_connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    await cursor.execute(
                        """
                        SELECT * FROM tickets WHERE uuid = ?
                        """,
                        (uuid,)
                    )
                    ticket = await cursor.fetchone()
                    return True if ticket else False
                except aiosqlite.Error as e:
                    self.db_logger.error("Error checking ticket in database", exc_info=e)
                    return False

    async def remove_ticket(self, uuid: str) -> None:
        async with self.get_db_connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    await cursor.execute(
                        """
                        DELETE FROM tickets WHERE uuid = ?
                        """,
                        (uuid,)
                    )
                    await connection.commit()
                    self.db_logger.debug(f"Ticket {uuid} removed from database")
                except aiosqlite.Error as e:
                    self.db_logger.error("Error removing ticket from database", exc_info=e)

    async def get_tickets(self, user_id: int) -> List[Tuple[str, int, str, int, int]]:
        async with self.get_db_connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    await cursor.execute(
                        """
                        SELECT * FROM tickets WHERE user_id = ?
                        """,
                        (user_id,)
                    )
                    tickets = await cursor.fetchall()
                    return tickets
                except aiosqlite.Error as e:
                    self.db_logger.error("Error getting tickets from database", exc_info=e)
                    return []

    async def get_tickets_by_category(self, category: str) -> List[Tuple[str, int, str, int, int]]:
        async with self.get_db_connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    await cursor.execute(
                        """
                        SELECT * FROM tickets WHERE category = ?
                        """,
                        (category,)
                    )
                    tickets = await cursor.fetchall()
                    return tickets
                except aiosqlite.Error as e:
                    self.db_logger.error("Error getting tickets from database", exc_info=e)
                    return []

    async def get_tickets_by_guild(self, guild_id: int) -> List[Tuple[str, int, str, int, int]]:
        async with self.get_db_connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    await cursor.execute(
                        """
                        SELECT * FROM tickets WHERE guild_id = ?
                        """,
                        (guild_id,)
                    )
                    tickets = await cursor.fetchall()
                    return tickets
                except aiosqlite.Error as e:
                    self.db_logger.error("Error getting tickets from database", exc_info=e)
                    return []

    async def get_ticket_by_channel_id(self, channel_id: int) -> Optional[Tuple[str, int, str, int, int]]:
        async with self.get_db_connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    await cursor.execute(
                        """
                        SELECT * FROM tickets WHERE channel_id = ?
                        """,
                        (channel_id,)
                    )
                    ticket = await cursor.fetchone()
                    return ticket
                except aiosqlite.Error as e:
                    self.db_logger.error("Error getting ticket from database", exc_info=e)
                    return None