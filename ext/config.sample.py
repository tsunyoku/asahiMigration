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

asahi_postgres = { # output database
    'database': 'asahi',
    'host': 'localhost',
    'password': 'gay',
    'user': 'awesome'
}