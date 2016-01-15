import inspect
import json
import os
import logging

LOG = logging.getLogger(__name__)


# ---------------#------------------------------------------------------------#
# Generic Config #
# ---------------#


class GameModeDescriptor(object):
    def __init__(self):
        pass

    def __get__(self, instance, owner):
        mode = instance._game_mode if instance else owner._game_mode
        return mode.partition('/')[0]

    def __set__(self, instance, value):
        instance._game_mode = value


class BaseConfig(object):
    """
    A base class for creating and accessing configuration. This class is shared
    by all projects, and should only contain truly generic functionality.
    """
    base_dir = None

    GAME_MODE = GameModeDescriptor()
    _game_mode = os.environ['GAME_MODE']
    _collection_factory = None

    def __init__(self):
        # Here we use inspect to work out what class we are. This will change
        # when we are sub-classed to be the child class. From this we can
        # determine where the child class is in the file system.
        self.base_dir = os.path.split(inspect.getfile(type(self)))[0]

        config_source = None
        if hasattr(self, 'CONFIG_SOURCE'):
            config_source = self.CONFIG_SOURCE

        if not config_source or config_source == 'local_json':
            self.get_settings = LocalJSON(self)

        elif config_source == 'sqlite':
            self.get_settings = sqlite(self)

        else:
            raise ValueError(
                "The CONFIG_SOURCE value '%s' is not a valid source type"
                % config_source)

        self._load_external_settings()

    def mode_suffix(self, value=''):
        """
        Return the mode suffix (if any) with reference to GAME_MODE

        :param value: If you supply a value, the suffix will be added to it and
                      returned. Otherwise only the suffix is returned.
        """

        if self.GAME_MODE in ['test', 'local']:
            value += '_' + self.GAME_MODE

        return value

    def get_path(self, *path_parts):
        """
        Returns a path relative to the location of the child task.
        By convention you should place your subclass
        in the root of your project to benefit from this.
        """

        return os.path.join(self.base_dir, *path_parts)

    def get_product_name(self):
        return self.base_dir.split(os.sep)[-1]

# ---------------#
# Helper Methods #
# ---------------#
#
# The following methods aren't exactly essential, you could do this
# yourself, but they are very commonly used, and very handy.

    def get_json(self, *path_parts):
        """
        Takes a relative path to a JSON file and returns the contents.
        """
        filename = self.get_path(*path_parts)
        with open(filename, 'r') as fh:
            return json.load(fh)

    def get_db_connection(self, db_name=None):

        # conn = 'the sqlite connection'

        if db_name is not None:
            conn = conn[self.mode_suffix(db_name)]
        return conn

    @property
    def collection_factory(self):
        if self._collection_factory is None:
            from lib.db import CollectionFactory
            self._collection_factory = \
                CollectionFactory(self.get_db_connection)

        return self._collection_factory


class SettingsNotFoundException(Exception):
    pass


class SettingsSource(object):
    """
    An abstraction over providing settings dicts for a settings object
    """
    def __init__(self, settings):
        """
        :param settings:
        """
        self.settings = settings

    def get_settings(self, config_type, key):
        """
        :param config_type: The type of configuration you want
        :param key: The specific item in that category
        :return: A dict of configuration
        """

        raise NotImplementedError()

    def __call__(self, config_type, key):
        """
        This object can be called as a function, which will be proxied through
        to the get_settings() function.
        """
        return self.get_settings(config_type, key)


class LocalJSON(SettingsSource):
    def get_settings(self, config_type, key):
        """
        Returns a dict of details read from:

            resource/config/<config_type>/<GAME_MODE>/<key>.json
            or alternative...

        The path is relative to this class, or subclass if you are subclassed.
        """
        try:
            details = self.settings.get_json(
                'resource', 'config', config_type,
                self.settings.GAME_MODE, key + '.json')
        except IOError, e:
            raise SettingsNotFoundException(e)

        return details
