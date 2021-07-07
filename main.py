from cmyui import AsyncSQLPool, log, Ansi
from pathlib import Path

from objects import glob

import asyncpg
import asyncio
import uvloop
import os
import time

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

async def startup():
    log('Connecting to databases...')

    glob.sql = AsyncSQLPool()
    await glob.sql.connect(glob.config.input_sql)
    log('Connected to MySQL (gulag/ripple)!')

    glob.postgres = await asyncpg.connect(**glob.config.asahi_postgres)
    log('Connected to PostgreSQL (Asahi)!')

async def close_dbs():
    await glob.sql.close()
    await glob.postgres.close()

async def import_db():
    db_file = Path.cwd() / 'ext/db.sql'

    if not db_file.exists():
        log("Couldn't find database file. Please ensure you cloned correctly and try again...", Ansi.LRED)

    log('Importing database. Note: You may be asked to enter your password, please do so!')

    # if they're running it again after first time then there's probably an error, lets just drop the database for safety
    # we need to restart postgres first incase of any dead sessions
    os.system('sudo /etc/init.d/postgresql restart >/dev/null 2>&1')
    os.system(f'sudo -u postgres -i psql -c "DROP DATABASE {glob.config.asahi_postgres["database"]};" >/dev/null 2>&1')
    os.system(f'sudo -u postgres -i psql -c "CREATE DATABASE {glob.config.asahi_postgres["database"]};" >/dev/null 2>&1')

    os.system(f'sudo -u postgres -i psql {glob.config.asahi_postgres["database"]} < {str(db_file)} >/dev/null 2>&1')

    log('Database imported!')

if glob.config.gulag:
    from servers.gulag import convert_users, convert_stats, convert_scores, convert_maps, convert_client_hashes, convert_friends, convert_achs
elif glob.config.ripple:
    from servers.ripple import convert_users, convert_stats, convert_scores, convert_maps, convert_client_hashes, convert_friends, convert_achs
else:
    raise RuntimeError('Please set either gulag or ripple to True!')

input(
    'Please be aware that before running this script, you should have made a blank database in PostgreSQL for Asahi and have a valid gulag database in MySQL. '
    'If not, please sort that now and run again (Ctrl + C to exit). '
    'Otherwise, press any key to continue!'
)

start = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(import_db())
loop.run_until_complete(startup())
loop.run_until_complete(convert_users())
loop.run_until_complete(convert_stats())
loop.run_until_complete(convert_scores())
loop.run_until_complete(convert_maps())
loop.run_until_complete(convert_client_hashes())
loop.run_until_complete(convert_friends())
loop.run_until_complete(convert_achs())
loop.run_until_complete(close_dbs())
log(f'Migration complete in {(time.time() - start) // 60:.2f} minutes!')