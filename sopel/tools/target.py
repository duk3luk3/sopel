# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

import functools
from sopel.tools import Identifier


@functools.total_ordering
class User(object):
    """A representation of a user Sopel is aware of."""
    def __init__(self, nick, user, host):
        assert isinstance(nick, Identifier)
        self.nick = nick
        """The user's nickname."""
        self.user = user
        """The user's local username."""
        self.host = host
        """The user's hostname."""
        self.channels = {}
        """The channels the user is in.

        This maps channel name ``Identifier``\s to ``Channel`` objects."""
        self.account = None
        """The IRC services account of the user.

        This relies on IRCv3 account tracking being enabled."""
        self.away = None
        """Whether the user is marked as away."""

    hostmask = property(lambda self: '{}!{}@{}'.format(self.nick, self.user,
                                                       self.host))
    """The user's full hostmask."""

    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return self.nick == other.nick

    def __lt__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return self.nick < other.nick


@functools.total_ordering
class Channel(object):
    """A representation of a channel Sopel is in."""
    def __init__(self, name):
        assert isinstance(name, Identifier)
        self.name = name
        """The name of the channel."""
        self.users = {}
        """The users in the channel.

        This maps username ``Identifier``\s to channel objects."""
        self.privileges = {}
        """The permissions of the users in the channel.

        This maps username ``Identifier``s to bitwise integer values. This can
        be compared to appropriate constants from ``sopel.module``."""

    def clear_user(self, nick):
        user = self.users[nick]
        user.channels.pop(self.name, None)
        del self.users[nick]
        del self.privileges[nick]

    def add_user(self, user):
        assert isinstance(user, User)
        self.users[user.nick] = user
        self.privileges[user.nick] = 0
        user.channels[self.name] = self

    def rename_user(self, old, new):
        if old in self.users:
            self.users[new] = self.users.pop(old)
        if old in self.privileges:
            self.privileges[new] = self.privileges.pop(old)

    def __eq__(self, other):
        if not isinstance(other, Channel):
            return NotImplemented
        return self.name == other.name

    def __lt__(self, other):
        if not isinstance(other, Channel):
            return NotImplemented
        return self.name < other.name
