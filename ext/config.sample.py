# set to true which you are migrating from.
# input_sql should be mysql info & db for whichever you are switching from, the migrator will handle the rest
gulag = True
ripple = False

input_sql = { # input database
    'db': 'gulag',
    'host': 'localhost',
    'password': 'gay',
    'user': 'awesome'
}

output_sql = { # output database
    'database': 'asahi',
    'host': 'localhost',
    'password': 'gay',
    'user': 'awesome'
}

old_path = '' # old gulag/ripple path
old_path_cheat = '' # old gulag cheat 
new_path = '' # where asahi is kept