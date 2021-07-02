from enum import IntFlag

class gulagPrivileges(IntFlag):
    # privileges intended for all normal players.
    Normal      = 1 << 0 # is an unbanned player.
    Verified    = 1 << 1 # has logged in to the server in-game.

    # has bypass to low-ceiling anticheat measures (trusted).
    Whitelisted = 1 << 2

    # donation tiers, receives some extra benefits.
    Supporter   = 1 << 4
    Premium     = 1 << 5

    # notable users, receives some extra benefits.
    Alumni      = 1 << 7

    # staff permissions, able to manage server state.
    Tournament  = 1 << 10 # able to manage match state without host.
    Nominator   = 1 << 11 # able to manage maps ranked status.
    Mod         = 1 << 12 # able to manage users (level 1).
    Admin       = 1 << 13 # able to manage users (level 2).
    Dangerous   = 1 << 14 # able to manage full server state.

    Donator = Supporter | Premium
    Staff = Mod | Admin | Dangerous

class asahiPrivileges(IntFlag):
    Normal = 1 << 0
    Verified = 1 << 1
    Supporter = 1 << 2

    Nominator = 1 << 3
    Admin = 1 << 4
    Developer = 1 << 5
    Owner = 1 << 6

    # i'm making banned/restricted privileges separately because the system of removing normal really confuses me to this day
    Restricted = 1 << 7
    Banned = 1 << 8

    Whitelisted = 1 << 9 # can bypass anticheat checks
    Frozen = 1 << 10

    Staff = Nominator | Admin | Developer | Owner
    Manager = Admin | Developer | Owner
    Master = Normal | Verified | Supporter | Nominator | Admin | Developer | Owner
    Disallowed = Restricted | Banned