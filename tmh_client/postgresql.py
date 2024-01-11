"""
Module to work with a PostgreSQL database.
"""
# stdlib
import os
import logging

# third party
import psycopg2
import pandas as pd

# relative
from . import read_file


class PostgreSQL:
    """
    Allows to interact with a PostgreSQL database by getting
    or retrieving information.

    Default port = 5432.
    Run SELECT * FROM pg_settings WHERE name = "port"; in command line to
    see the specified port.
    """
    def __init__(self,
                 config_path: str,
                 config_name: str):
        # Config variables
        self.config_path: str = config_path
        self.config_name: str = config_name
        self.config: dict = {}
        self.config_keys: list = ["user", "password", "db_name",
                                  "table_name","start_curtailment",
                                  "end_curtailment", "plant_id",
                                  "level"]

        self.connection = None
        self.cur = None

    def get_config(self) -> dict:
        """
        Getter function for internal variable
        :return: dict, config file
        """
        return self.config

    def connect_and_extract(self) -> pd.DataFrame:
        """
        Connect and extract information from a PostgreSQL database
        based on a config file.
        """
        if self._validate_config():
            self._connect_to_db()
            if self.config["table_name"] in self._get_tables():
                df: pd.DataFrame = self._get_rows()
                self.close_connection()
                return df

        logging.error("Invalid config file for %s", self.config_name)
        raise Exception(f"Invalid config file for {self.config_name}")

    def close_connection(self):
        """
        Close database connection
        """
        self.connection.close()

    def _validate_config(self) -> bool:
        if read_file.file_exists(os.path.join(self.config_path,
                                              self.config_name)):
            self.config: dict = read_file.json_to_dict(self.config_path,
                                                       self.config_name)
        if all(e in list(self.config.keys()) for e in self.config_keys):
            return True
        return False

    def _connect_to_db(self,
                       host: str="localhost",
                       port: int=5432):
        """
        Connects to a PostgreSQL database with a specific table, if a
        db_name is given.
        Password is set with Ansible playbook postgresql.yaml.

        :param host; str, IP address of PostgreSQL server
        :param port: int, port of PostgreSQL server
        :param user: str, PostgreSQL user name
        :param password: str, password for user
        :param db_name: str, database name
        """
        try:
            conn_string = "host=" + host + \
                          " port=" + str(port) + \
                          " user=" + self.config["user"] + \
                          " password=" + self.config["password"]
            if self.config["db_name"] is not None:
                conn_string += " dbname=" + self.config["db_name"]

            self.connection = psycopg2.connect(conn_string)
            self.cur = self.connection.cursor()

        except psycopg2.OperationalError as e:
            logging.error(e)

    def _get_tables(self,
                    public=True) -> list:
        """
        Returns all tables from the connect Postgresql host depending
        on the access of the table (public or not).

        :param public: boolean, list just public or all available tables
        :return: list, available tables
        """
        if public:
            self.cur.execute("""SELECT table_name FROM
            information_schema.tables WHERE
            table_schema = 'public'""")
        else:
            self.cur.execute("""SELECT table_name FROM
            information_schema.tables""")
        tables: list(tuple) = self.cur.fetchall()
        tables: list = [t[0] for t in tables]
        return tables

    def _build_query(self):
        conditions: list = [f"plant_id='{self.config['plant_id']}'",
                            f"start_curtailment>='{self.config['start_curtailment']}'",
                            f"start_curtailment<='{self.config['end_curtailment']}'"]

        if isinstance(self.config["level"], int):
            conditions.append(f"level={self.config['level']}")
        elif isinstance(self.config["level"], list):
            for l in self.config["level"]:
                conditions.append(f"level={l}")

        query: str = f"SELECT * FROM {self.config['table_name']} WHERE ("
        count_level: int = 0
        for i, cond in enumerate(conditions):
            if i == 0:
                query += cond
            elif "level" in cond and count_level == 0:
                query += ") AND (" + cond
                count_level += 1
            elif "level" in cond and count_level > 0:
                query += " OR " + cond
            else:
                query += " AND " + cond
        query += ");"
        return query

    def _get_rows(self) -> pd.DataFrame:
        query: str = self._build_query()
        df: pd.DataFrame = pd.read_sql_query(sql=query,
                                             con=self.connection)
        return df
