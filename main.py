from cmyui import log, Ansi
from pathlib import Path

from objects import glob
from fatFuckSQL import fatFawkSQL

import asyncio
import uvloop
import os
import time

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

async def startup():
    log('Connecting to databases...')

    glob.input = await fatFawkSQL.connect(**glob.config.input_sql)
    log('Connected to MySQL (gulag/ripple)!')

    glob.output = await fatFawkSQL.connect(**glob.config.output_sql)
    log('Connected to MySQL (Asahi)!')

async def close_dbs():
    await glob.input.close()
    await glob.output.close()

async def import_db():
    db_file = Path.cwd() / 'ext/db.sql'

    if not db_file.exists():
        log("Couldn't find database file. Please ensure you cloned correctly and try again...", Ansi.LRED)

    log('Importing database. Note: You may be asked to enter your password, please do so!')

    os.system(f'sudo mariadb -e "DROP DATABASE {glob.config.output_sql["db"]};" >/dev/null 2>&1')
    os.system(f'sudo mariadb -e "CREATE DATABASE {glob.config.output_sql["db"]};" >/dev/null 2>&1')

    os.system(f'sudo mariadb {glob.config.output_sql["db"]} < {str(db_file)} >/dev/null 2>&1')

    log('Database imported!')

if glob.config.gulag:
    from servers.gulag import convert_users, convert_stats, convert_scores, convert_maps, convert_client_hashes, convert_friends, convert_achs, convert_clans, convert_favourites, convert_ratings, migrate_data, migrate_data_cheat, convert_achs_cheat, convert_scores_cheat, convert_stats_cheat
elif glob.config.ripple:
    from servers.ripple import convert_users, convert_stats, convert_scores, convert_maps, convert_client_hashes, convert_friends, convert_achs, convert_clans, convert_favourites, convert_ratings, migrate_data, migrate_data_cheat, convert_achs_cheat, convert_scores_cheat, convert_stats_cheat
else:
    raise RuntimeError('Please set either gulag or ripple to True!')

input(
    'Please be aware that before running this script, you should have made a blank database Asahi and have a valid gulag database in MySQL. '
    'If not, please sort that now and run again (Ctrl + C to exit). '
    'Otherwise, press any key to continue!'
)

start = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(import_db())
loop.run_until_complete(startup())
loop.run_until_complete(convert_users())
loop.run_until_complete(convert_stats())
loop.run_until_complete(convert_stats_cheat())
loop.run_until_complete(convert_scores())
loop.run_until_complete(convert_scores_cheat())
loop.run_until_complete(convert_maps())
loop.run_until_complete(convert_client_hashes())
loop.run_until_complete(convert_friends())
loop.run_until_complete(convert_achs())
loop.run_until_complete(convert_clans())
loop.run_until_complete(convert_favourites())
loop.run_until_complete(convert_ratings())
loop.run_until_complete(convert_achs_cheat())
loop.run_until_complete(close_dbs())
loop.run_until_complete(migrate_data())
loop.run_until_complete(migrate_data_cheat())
log(f'Migration complete in {(time.time() - start) // 60:.2f} minutes!')