# Copyright (c) 2016, 2020, Oracle and/or its affiliates.
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


"""Implementation of MySQL Authentication Plugin."""

import hashlib
import struct

from .helpers import hexlify


def xor_string(hash1, hash2, hash_size):
    """Encrypt/Decrypt function used for password encryption in
    authentication, using a simple XOR.

    Args:
        hash1 (str): The first hash.
        hash2 (str): The second hash.

    Returns:
        str: A string with the xor applied.
    """
    xored = [h1 ^ h2 for (h1, h2) in zip(hash1, hash2)]
    return struct.pack("{0}B".format(hash_size), *xored)


class BaseAuthPlugin(object):
    """Base class for implementing the authentication plugins."""
    def __init__(self, username=None, password=None):
        self._username = username
        self._password = password

    def name(self):
        """Returns the plugin name.

        Returns:
            str: The plugin name.
        """
        raise NotImplementedError

    def auth_name(self):
        """Returns the authentication name.

        Returns:
            str: The authentication name.
        """
        raise NotImplementedError


class MySQL41AuthPlugin(BaseAuthPlugin):
    """Class implementing the MySQL Native Password authentication plugin."""
    def name(self):
        """Returns the plugin name.

        Returns:
            str: The plugin name.
        """
        return "MySQL 4.1 Authentication Plugin"

    def auth_name(self):
        """Returns the authentication name.

        Returns:
            str: The authentication name.
        """
        return "MYSQL41"

    def auth_data(self, data):
        """Hashing for MySQL 4.1 authentication.

        Args:
            data (str): The authentication data.

        Returns:
            str: The authentication response.
        """
        if self._password:
            password = self._password.encode("utf-8") \
                if isinstance(self._password, str) else self._password
            hash1 = hashlib.sha1(password).digest()
            hash2 = hashlib.sha1(hash1).digest()
            xored = xor_string(hash1, hashlib.sha1(data + hash2).digest(), 20)
            return "{0}\0{1}\0*{2}\0".format("", self._username, hexlify(xored))
        return "{0}\0{1}\0".format("", self._username)


class PlainAuthPlugin(BaseAuthPlugin):
    """Class implementing the MySQL Plain authentication plugin."""
    def name(self):
        """Returns the plugin name.

        Returns:
            str: The plugin name.
        """
        return "Plain Authentication Plugin"

    def auth_name(self):
        """Returns the authentication name.

        Returns:
            str: The authentication name.
        """
        return "PLAIN"

    def auth_data(self):
        """Returns the authentication data.

        Returns:
            str: The authentication data.
        """
        return "\0{0}\0{1}".format(self._username, self._password)


class Sha256MemoryAuthPlugin(BaseAuthPlugin):
    """Class implementing the SHA256_MEMORY authentication plugin."""
    def name(self):
        """Returns the plugin name.

        Returns:
            str: The plugin name.
        """
        return "SHA256_MEMORY Authentication Plugin"

    def auth_name(self):
        """Returns the authentication name.

        Returns:
            str: The authentication name.
        """
        return "SHA256_MEMORY"

    def auth_data(self, data):
        """Hashing for SHA256_MEMORY authentication.

        The scramble is of the form:
            SHA256(SHA256(SHA256(PASSWORD)),NONCE) XOR SHA256(PASSWORD)

        Args:
            data (str): The authentication data.

        Returns:
            str: The authentication response.
        """
        password = self._password.encode("utf-8") \
            if isinstance(self._password, str) else self._password
        hash1 = hashlib.sha256(password).digest()
        hash2 = hashlib.sha256(hashlib.sha256(hash1).digest() + data).digest()
        xored = xor_string(hash2, hash1, 32)
        return "\0{0}\0{1}".format(self._username, hexlify(xored))
