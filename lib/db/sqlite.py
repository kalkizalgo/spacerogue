import sqlite3


def get_all_db_names():
    """
    Returns a list of all necessary sqlite databases
    :return:
    """


def get_cur_db_names():
    """
    Returns a list of currently existing sqlite databases
    :return:
    """


def validate_db_schema(db_name):
    """
    Validates if the schema in a currently existing db is correct.
    :param db_name:
    :return:
    """


def get_db_connection(db_name):
    """
    Returns a connection to given sqlite db
    :param db_name:
    :return:
    """
    # Is it necessary to close these ?!?


def commit_and_close(conn):
    """
    Commit changes and close connection
    :param conn:
    :return:
    """
    # Should these be seperated out, or not exist at all ?!?


def create_from_schema():
    """
    Creates dbs and tables from json file schema
    :return:
    """


def populate_from_json():
    """
    Do initial import into dbs from json files.
    :return:
    """
    # Perhaps find a specialise lib for transfering from
    # json to memory then passing it through.
