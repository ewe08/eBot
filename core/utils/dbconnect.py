import asyncpg


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def add_data(self, user_id, username, fullname, chat_id):
        query = f"INSERT INTO datausers (user_id, full_name, username, chat_id) " \
                f"VALUES ({user_id}, '{fullname}', '{username}', {chat_id}) " \
                f"ON CONFLICT (id) DO UPDATE SET full_name='{fullname}'"
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

    async def get_data_score(self, user_id, chat_id):
        query = f"SELECT (score) FROM datausers WHERE user_id={user_id} AND chat_id={chat_id}"
        return await self.connector.fetch(query)

    async def update_data_score(self, user_id, chat_id, value):
        query = f"UPDATE datausers SET score = score + {value} " \
                f"WHERE user_id={user_id} AND chat_id={chat_id}"
        await self.connector.execute(query)

    async def update_data_day(self, user_id, chat_id, value):
        query = f"UPDATE datausers SET for_day = for_day + {value} " \
                f"WHERE user_id={user_id} AND chat_id={chat_id}"
        await self.connector.execute(query)

    async def update_data_week(self, user_id, chat_id, value):
        query = f"UPDATE datausers SET for_week = for_week + {value} " \
                f"WHERE user_id={user_id} AND chat_id={chat_id}"
        await self.connector.execute(query)

    async def get_data_limit(self, user_id, chat_id):
        query = f"SELECT (send_in_day) FROM datausers " \
                f"WHERE user_id={user_id} AND chat_id={chat_id}"
        return await self.connector.fetch(query)

    async def update_data_limit(self, user_id, chat_id, value):
        query = f"UPDATE datausers SET send_in_day = send_in_day + {value} " \
                f"WHERE user_id={user_id} AND chat_id={chat_id}"
        await self.connector.execute(query)
