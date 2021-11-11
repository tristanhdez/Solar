# Copyright (c) 2012, 2021, Oracle and/or its affiliates.
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


"""MySQL Connector/Python version information

The file version.py gets installed and is available after installation
as mysql.connector.version.
"""

VERSION = (8, 0, 27, '', 1)

if VERSION[3] and VERSION[4]:
    VERSION_TEXT = '{0}.{1}.{2}{3}{4}'.format(*VERSION)
else:
    VERSION_TEXT = '{0}.{1}.{2}'.format(*VERSION[0:3])

VERSION_EXTRA = ''
LICENSE = 'GPLv2 with FOSS License Exception'
EDITION = ''  # Added in package names, after the version
