import asyncpg

from core.settings import settings


async def create_pool():
    return await asyncpg.create_pool(
        user=settings.databases.user,
        password=settings.databases.password,
        database=settings.databases.database,
        host=settings.databases.host,
        port=settings.databases.port,
        command_timeout=settings.databases.command_timeout,
    )


def double_quote(string):
    if string is None:
        return string
    return string.replace("'", "''")


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def add_data_with_referral(self, user_id, username, fullname, chat_id, referral_id):
        query = f"INSERT INTO datausers (user_id, full_name, username, chat_id, referral) " \
                f"VALUES ({user_id}, '{double_quote(fullname)}', '{double_quote(username)}', {chat_id}, {referral_id}) " \
                f"ON CONFLICT (id) DO UPDATE SET full_name='{double_quote(fullname)}'"
        await self.connector.execute(query)

    async def add_data(self, user_id, username, fullname, chat_id):
        double_quote(fullname)
        query = f"INSERT INTO datausers (user_id, full_name, username, chat_id) " \
                f"VALUES ({user_id}, '{double_quote(fullname)}', '{double_quote(username)}', {chat_id}) " \
                f"ON CONFLICT (id) DO UPDATE SET full_name='{double_quote(fullname)}'"
        await self.connector.execute(query)

    async def check_user(self, user_id, chat_id):
        query = f"SELECT (user_id) FROM datausers " \
                f"WHERE user_id={user_id} AND chat_id={chat_id}"
        return await self.connector.fetch(query)

    async def get_all_data(self, user_id, chat_id):
        query = f"SELECT * FROM datausers WHERE user_id={user_id} AND chat_id={chat_id}"
        return await self.connector.fetch(query)

    async def get_top_users(self, chat_id):
        query = f"SELECT (user_id, full_name, score) FROM datausers " \
                f"WHERE chat_id={chat_id} ORDER BY score DESC LIMIT 10"
        return await self.connector.fetch(query)

    async def get_top_week_users(self, chat_id):
        query = f"SELECT (user_id, full_name, messages_for_week) FROM datausers " \
                f"WHERE chat_id={chat_id} ORDER BY messages_for_week DESC LIMIT 10"
        return await self.connector.fetch(query)

    async def get_score_in_chat(self, chat_id):
        query = f"SELECT (user_id, chat_id, score) FROM datausers " \
                f"WHERE chat_id={chat_id}"
        return await self.connector.fetch(query)

    async def get_score(self, user_id, chat_id):
        query = f"SELECT (score) FROM datausers WHERE user_id={user_id} AND chat_id={chat_id}"
        return await self.connector.fetch(query)

    async def get_all_score(self, user_id, chat_id):
        query = f"SELECT (all_score) FROM datausers WHERE user_id={user_id} AND chat_id={chat_id}"
        return await self.connector.fetch(query)

    async def update_score(self, user_id, chat_id, value):
        query = f"UPDATE datausers " \
                f"SET (score, all_score) = (score + {value}, all_score + {value}) " \
                f"WHERE user_id={user_id} AND chat_id={chat_id}"
        await self.connector.execute(query)

    async def set_score(self, user_id, chat_id, value):
        query = f"UPDATE datausers " \
                f"SET score = {value} " \
                f"WHERE user_id={user_id} AND chat_id={chat_id}"
        await self.connector.execute(query)

    async def get_referral_id(self, user_id, chat_id):
        query = f"SELECT (referral) FROM datausers " \
                f"WHERE user_id={user_id} AND chat_id={chat_id}"
        return await self.connector.fetch(query)

    async def get_referral_score(self, user_id, chat_id):
        query = f"SELECT (from_referral) FROM datausers " \
                f"WHERE user_id={user_id} AND chat_id={chat_id}"
        return await self.connector.fetch(query)

    async def update_referral_score(self, user_id, chat_id, value):
        query = f"UPDATE datausers " \
                f"SET from_referral = datausers.from_referral + {value} " \
                f"WHERE user_id={user_id} AND chat_id={chat_id}"
        await self.connector.execute(query)

    async def set_referral_score(self, user_id, chat_id, value):
        query = f"UPDATE datausers " \
                f"SET from_referral = {value} " \
                f"WHERE user_id={user_id} AND chat_id={chat_id}"
        await self.connector.execute(query)

    async def get_limit(self, user_id, chat_id):
        query = f"SELECT (send_in_day) FROM datausers " \
                f"WHERE user_id={user_id} AND chat_id={chat_id}"
        return await self.connector.fetch(query)

    async def update_limit(self, user_id, chat_id, value):
        query = f"UPDATE datausers SET send_in_day = send_in_day + {value} " \
                f"WHERE user_id={user_id} AND chat_id={chat_id}"
        await self.connector.execute(query)

    async def set_limit(self, user_id, chat_id, value):
        query = f"UPDATE datausers SET send_in_day = {value} " \
                f"WHERE user_id={user_id} AND chat_id={chat_id}"
        await self.connector.execute(query)

    async def get_day_data_in_chat(self, chat_id):
        query = f"SELECT (user_id, chat_id, for_day) FROM datausers WHERE chat_id={chat_id}"
        return await self.connector.fetch(query)

    async def get_day_data(self, user_id, chat_id):
        query = f"SELECT (for_day) FROM datausers " \
                f"WHERE user_id={user_id} AND chat_id={chat_id}"
        return await self.connector.fetch(query)

    async def update_day_data(self, user_id, chat_id, value):
        query = f"UPDATE datausers SET for_day = for_day + {value} " \
                f"WHERE user_id={user_id} AND chat_id={chat_id}"
        await self.connector.execute(query)

    async def set_day_data(self, user_id, chat_id, value):
        query = f"UPDATE datausers SET for_day = {value} " \
                f"WHERE user_id={user_id} AND chat_id={chat_id}"
        await self.connector.execute(query)

    async def get_week_date_in_chat(self, chat_id):
        query = f"SELECT (user_id, chat_id, for_week) FROM datausers WHERE chat_id={chat_id}"
        return await self.connector.fetch(query)

    async def get_week_data(self, user_id, chat_id):
        query = f"SELECT (for_day) FROM datausers " \
                f"WHERE user_id={user_id} AND chat_id={chat_id}"
        return await self.connector.fetch(query)

    async def update_week_data(self, user_id, chat_id, value):
        query = f"UPDATE datausers SET for_week = for_week + {value} " \
                f"WHERE user_id={user_id} AND chat_id={chat_id}"
        await self.connector.execute(query)

    async def set_week_data(self, user_id, chat_id, value):
        query = f"UPDATE datausers SET for_week = {value} " \
                f"WHERE user_id={user_id} AND chat_id={chat_id}"
        await self.connector.execute(query)

    async def get_messages_for_week(self, user_id, chat_id):
        query = f"SELECT (messages_for_week) FROM datausers " \
                f"WHERE user_id={user_id} AND chat_id={chat_id}"
        return await self.connector.fetch(query)

    async def update_messages_for_week(self, user_id, chat_id, value):
        query = f"UPDATE datausers SET messages_for_week = messages_for_week + {value} " \
                f"WHERE user_id={user_id} AND chat_id={chat_id}"
        await self.connector.execute(query)

    async def set_messages_for_week(self, user_id, chat_id, value):
        query = f"UPDATE datausers SET messages_for_week = {value} " \
                f"WHERE user_id={user_id} AND chat_id={chat_id}"
        await self.connector.execute(query)
