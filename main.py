from cmyui import AsyncSQLPool, log, Ansi
from pathlib import Path

from constants.privs import gulagPrivileges, asahiPrivileges
from objects import glob

import asyncpg
import asyncio
import uvloop
import os

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

async def startup():
    log('Connecting to databases...')

    glob.sql = AsyncSQLPool()
    await glob.sql.connect(glob.config.gulag_sql)
    log('Connected to MySQL (gulag)!')

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

async def convert_priv(old_priv):
    new_priv = asahiPrivileges(0)
    new_priv |= asahiPrivileges.Normal  # everyone has this no matter what

    if not old_priv & gulagPrivileges.Normal:  # restricted
        new_priv |= asahiPrivileges.Restricted

    if old_priv & gulagPrivileges.Verified:
        new_priv |= asahiPrivileges.Verified

    if old_priv & gulagPrivileges.Whitelisted:
        new_priv |= asahiPrivileges.Whitelisted

    if old_priv & gulagPrivileges.Supporter or old_priv & gulagPrivileges.Premium:
        new_priv |= asahiPrivileges.Supporter

    if old_priv & gulagPrivileges.Nominator:
        new_priv |= asahiPrivileges.Nominator

    if old_priv & gulagPrivileges.Mod or old_priv & gulagPrivileges.Admin:
        new_priv |= asahiPrivileges.Admin

    if old_priv & gulagPrivileges.Dangerous:
        new_priv |= asahiPrivileges.Owner

    return new_priv

async def convert_users():
    gulag_users = await glob.sql.fetchall('SELECT * FROM users')

    for user in gulag_users:
        id = user['id']
        name = user['name']
        safe_name = user['safe_name']
        email = user['email']
        pw = user['pw_bcrypt']  # absolutely cursed cus asahi doesn't use bcrypt, we will do some trolling in asahi repo for this
        country = user['country']

        gulag_priv = gulagPrivileges(user['priv'])
        asahi_priv = await convert_priv(gulag_priv)

        silence = user['silence_end']
        frozen = user['frozen']
        freeze = user['freezetime']
        clan = user['clan_id']
        creation = user['creation_time']
        donor = user['donor_end']

        if frozen:
            asahi_priv |= asahiPrivileges.Frozen

        await glob.postgres.execute(
            'INSERT INTO users '
            '(id, name, safe_name, email, pw, country, priv, clan, freeze_timer, registered_at, silence_end, donor_end) '
            'VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)',
            id, name, safe_name, email, pw, country, int(asahi_priv), clan, freeze, creation, silence, donor
        )

        log(f'Inserted {name} into Asahi database!')

    # fix auto increment
    last_id = gulag_users[-1]['id']
    await glob.postgres.execute(f'CREATE SEQUENCE users_id_seq START {last_id + 1};')
    await glob.postgres.execute("ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);")

    log('All users converted!')
    
async def convert_stats(): # TODO: finish this & the rest when im not lazy and have some final things added to asahi
    gulag_stats = await glob.sql.fetchall('SELECT * FROM stats')
    
    for user in gulag_stats:
        id = user['id']

        tscore_std = user['tscore_vn_std']
        tscore_taiko = user['tscore_vn_taiko']
        tscore_catch = user['tscore_vn_catch']
        tscore_mania = user['tscore_vn_mania']

        rscore_std = user['rscore_vn_std']
        rscore_taiko = user['rscore_vn_taiko']
        rscore_catch = user['rscore_vn_catch']
        rscore_mania = user['rscore_vn_mania']

input(
    'Please be aware that before running this script, you should have made a blank database in PostgreSQL for Asahi and have a valid gulag database in MySQL. '
    'If not, please sort that now and run again (Ctrl + C to exit). '
    'Otherwise, press any key to continue!'
)

loop = asyncio.get_event_loop()
loop.run_until_complete(import_db())
loop.run_until_complete(startup())
loop.run_until_complete(convert_users())
loop.run_until_complete(close_dbs())
log('Migration complete!')
