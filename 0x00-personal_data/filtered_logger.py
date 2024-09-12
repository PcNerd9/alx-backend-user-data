#!/usr/bin/env python3

"""
contains a function that filters a message
"""
import re
from typing import List

def filter_datum(fields: List[str], redaction: str, message: str, seperator: str) -> str:
    """ return the logs message obfuscated """
    pattern = r'({})([^{}]+)'.format("|".join(fields), seperator)
    repls = r'\1={}'.format(redaction)
    return re.sub(pattern, repls, message)
