# Copyright (c) 2014, Oracle and/or its affiliates.
#
# Following empty comments are intentional.
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# End empty comments.


"""Custom Python types used by MySQL Connector/Python"""


import sys


class HexLiteral(str):

    """Class holding MySQL hex literals"""

    def __new__(cls, str_, charset='utf8'):
        if sys.version_info[0] == 2:
            hexed = ["%02x" % ord(i) for i in str_.encode(charset)]
        else:
            hexed = ["%02x" % i for i in str_.encode(charset)]
        obj = str.__new__(cls, ''.join(hexed))
        obj.charset = charset
        obj.original = str_
        return obj

    def __str__(self):
        return '0x' + self
