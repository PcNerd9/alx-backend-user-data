#!/usr/bin/env python3

"""
contains a function that filters a message
"""
import re
from typing import List


def filter_datum(
    fields: List[str], redaction: str,
    message: str, separator: str
    ) -> str:
    """ return the logs message obfuscated """
    pattern = r'({})([^{}]+)'.format("|".join(fields), seperator)
    repls = r'\1={}'.format(redaction)
    message = re.sub(pattern, repls, message)
    return message
