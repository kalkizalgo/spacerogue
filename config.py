import logging
from spacerogue.lib import config

LOG = logging.getLogger(__name__)


class Config(BaseConfig):
    """
    Configuration class for spacerogue.
    """
    CONFIG_SOURCE = 'sqllite_db'

    APP_NAME = 'spacerogue'
    DEBUG = False

    def __init__(self):
        super(Config, self).__init__()
        # self.xyz


class LiveConfig(Config):
    """
    Live configuration for Advance Notices.
    """
    pass


class DebugConfig(LiveConfig):
    """
    Local configuration for Advance Notices.
    """
    CONFIG_SOURCE = 'local_json'

    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s %(name)-20s "
                               "[%(lineno)s] [%(levelname)s]: %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
    LOG.debug("Loaded local config")


class TestConfig(DebugConfig):
    """
    Test configuration for Advance Notices.
    """

    # REQUIRE_LOGIN = False
    # DISABLE_PAGE_LEAVE_WARNING = True


settings = \
    {
        'live': LiveConfig,
        'debug': DebugConfig,
        'test': TestConfig,
    }[Config.GAME_MODE]()
# This is the main output of this module that everyone is after
"""
:type settings: Config
"""
