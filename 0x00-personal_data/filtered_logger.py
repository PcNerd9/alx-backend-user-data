#!/usr/bin/env python3

"""
contains a function that filters a message
"""
import re


def filter_datum(fields, redaction, message, seperator):
    """ return the logs message obfuscated """
    pattern = r'({})([^{}]+)'.format("|".join(fields), seperator)
    repls = r'\1={}'.format(redaction)
    return re.sub(pattern, repls, message)
