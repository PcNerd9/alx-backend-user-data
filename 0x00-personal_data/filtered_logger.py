#!/usr/bin/env python3

"""
contains a function that filters a message
"""
import logging
from mysql import connector
from mysql.connector.connection import MySQLConnection
import os
import re
from typing import List, Sequence

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
    fields: Sequence[str], redaction: str,
    message: str, separator: str
) -> str:
    """ return the logs message obfuscated """
    pattern = r'({})([^{}]+)'.format("|".join(fields), separator)
    repls = r'\1={}'.format(redaction)
    message = re.sub(pattern, repls, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPERATOR = ";"

    def __init__(self, fields: Sequence[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        return a formated redacted log string
        """
        formatted_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            formatted_message, self.SEPERATOR)


def get_logger() -> logging.Logger:
    """
    return a logger
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    formater = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formater)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> MySQLConnection:
    """
    connect to the mysql database server and return it's
    connection object
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    connection = connector.connect(
            host=host,
            user=username,
            password=password,
            database=database
            )
    return connection


def main():
    """
    obtains all the rows in the database and displays each
    row under a filtered format like this
    """

    logger = get_logger()
    db = get_db()

    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        message = "name={};email={};phone={};"\
                "ssn={};password={};ip={};"\
                "last_login={};user_agent={}".format(
                        row[0], row[1],
                        row[2], row[3],
                        row[4], row[5],
                        row[6], row[7]
                        )
        logger.info(message)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
