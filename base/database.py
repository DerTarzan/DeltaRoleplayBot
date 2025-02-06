import asyncio
import datetime
import os
from datetime import timedelta

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

                await cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS checkouts (
                        user_id INTEGER,
                        reason TEXT NOT NULL,
                        duration TEXT NOT NULL
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

    async def schedule_backup(self):
        while True:
            now = datetime.datetime.now()
            midnight = datetime.datetime.combine(now.date() + timedelta(days=1), datetime.time.min)
            seconds_until_midnight = (midnight - now).total_seconds()

            if seconds_until_midnight > 3600:
                self.logger.debug(f"Backing up database in {seconds_until_midnight / 3600:.2f} hours")
            elif seconds_until_midnight > 60:
                self.logger.debug(f"Backing up database in {seconds_until_midnight / 60:.1f} minutes")
            else:
                self.logger.debug(f"Backing up database in {seconds_until_midnight:.0f} seconds")

            # In 60-Sekunden-Intervallen schlafen, um Zeitverschiebungen zu berücksichtigen
            while seconds_until_midnight > 0:
                sleep_time = min(60, seconds_until_midnight)
                await asyncio.sleep(sleep_time)
                now = datetime.datetime.now()
                seconds_until_midnight = (midnight - now).total_seconds()

    async def backup_database(self):
        backup_file = f"{self.db}.backup"
        try:
            self.logger.debug(f"Backing up database to {backup_file}")
            async with aiosqlite.connect(self.db) as source_conn:
                async with aiosqlite.connect(backup_file) as backup_conn:
                    await source_conn.backup(backup_conn)
            self.logger.debug("Database backup successful")
        except aiosqlite.Error as e:
            self.logger.error("Error while backing up database", exc_info=e)

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

    async def add_checkout(self, user_id: int, reason: str, duration: datetime.datetime):
        async with self.get_db_connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    await cursor.execute(
                        """
                        INSERT INTO checkouts (user_id, reason, duration)
                        VALUES (?, ?, ?)
                        """,
                        (user_id, reason, duration)
                    )
                    await connection.commit()
                    self.db_logger.debug(f"Checkout {user_id} added to database")
                except aiosqlite.Error as e:
                    self.db_logger.error("Error adding checkout to database", exc_info=e)

    async def get_checkout(self, user_id: int) -> Optional[Tuple[int, str, datetime.datetime]]:
        async with self.get_db_connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    await cursor.execute(
                        """
                        SELECT * FROM checkouts WHERE user_id = ?
                        """,
                        (user_id,)
                    )
                    checkout = await cursor.fetchone()
                    return checkout
                except aiosqlite.Error as e:
                    self.db_logger.error("Error getting checkout from database", exc_info=e)
                    return None

    async def remove_checkout(self, user_id: int) -> None:
        async with self.get_db_connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    await cursor.execute(
                        """
                        DELETE FROM checkouts WHERE user_id = ?
                        """,
                        (user_id,)
                    )
                    await connection.commit()
                    self.db_logger.debug(f"Checkout {user_id} removed from database")
                except aiosqlite.Error as e:
                    self.db_logger.error("Error removing checkout from database", exc_info=e)

    async def get_checkouts(self) -> List[Tuple[int, str, datetime.datetime]]:
        async with self.get_db_connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    await cursor.execute(
                        """
                        SELECT * FROM checkouts
                        """
                    )
                    checkouts = await cursor.fetchall()
                    return checkouts
                except aiosqlite.Error as e:
                    self.db_logger.error("Error getting checkouts from database", exc_info=e)
                    return []

    async def get_expired_checkouts(self) -> List[Tuple[int, str, datetime.datetime]]:
        async with self.get_db_connection() as connection:
            async with connection.cursor() as cursor:
                try:
                    await cursor.execute(
                        """
                        SELECT * FROM checkouts WHERE duration <= datetime('now')
                        """
                    )
                    expired_checkouts = await cursor.fetchall()
                    return expired_checkouts
                except aiosqlite.Error as e:
                    self.db_logger.error("Error getting expired checkouts from database", exc_info=e)
                    return []