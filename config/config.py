from environs import Env
from dataclasses import dataclass


@dataclass
class Config:
    token: str


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(token=env('TOKEN_BOT'))
