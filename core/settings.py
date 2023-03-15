from dataclasses import dataclass

from environs import Env


@dataclass
class Bots:
    bot_token: str
    admin_id: int
    chat_id: int


@dataclass
class DataBase:
    user: str
    password: str
    database: str
    host: str
    port: int
    command_timeout: int


@dataclass
class Settings:
    bots: Bots
    databases: DataBase


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str('TOKEN'),
            admin_id=env.int('ADMIN_ID'),
            chat_id=env.int('CHAT_ID'),
        ),
        databases=DataBase(
            user=env.str('USER'),
            password=env.str('PASSWORD'),
            database=env.str('DATABASE'),
            host=env.str('HOST'),
            port=env.int('PORT'),
            command_timeout=env.int('TIMEOUT'),
        )
    )


settings = get_settings('input')
