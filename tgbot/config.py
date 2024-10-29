from dataclasses import dataclass

from environs import Env

SOCIAL_MEDIA = ["instagram", 'tik tok', 'telegram']


@dataclass
class TgBot:
    """
    Creates the TgBot object from environment variables.
    """

    token: str
    admin_ids: list[int]
    ad_username: str

    @staticmethod
    def from_env(env: Env):
        """
        Creates the TgBot object from environment variables.
        """
        token = env.str("BOT_TOKEN")
        admin_ids = env.list("ADMINS", subcast=int)
        ad_username = env.str("AD_USERNAME")
        return TgBot(token=token, admin_ids=admin_ids, ad_username=ad_username)


@dataclass
class Miscellaneous:

    other_params: str = None


@dataclass
class Config:

    tg_bot: TgBot
    misc: Miscellaneous


def load_config(path: str = None) -> Config:
    # Create an Env object.
    # The Env object will be used to read environment variables.
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot.from_env(env),
        misc=Miscellaneous(),
    )
