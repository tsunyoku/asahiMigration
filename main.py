from cmyui import AsyncSQLPool, log, Ansi
from pathlib import Path

from constants.privs import gulagPrivileges, asahiPrivileges
from constants.mods import convert
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

        log(f'Inserted {name} into users database!')

    # fix auto increment
    last_id = gulag_users[-1]['id']
    await glob.postgres.execute(f'CREATE SEQUENCE users_id_seq START {last_id + 1};')
    await glob.postgres.execute("ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);")

    log('All users converted!')
    
async def convert_stats():
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
        
        pp_std = user['pp_vn_std']
        pp_taiko = user['pp_vn_taiko']
        pp_catch = user['pp_vn_catch']
        pp_mania = user['pp_vn_mania']
        
        pc_std = user['plays_vn_std']
        pc_taiko = user['plays_vn_taiko']
        pc_catch = user['plays_vn_catch']
        pc_mania = user['plays_vn_mania']

        pt_std = user['playtime_vn_std']
        pt_taiko = user['playtime_vn_taiko']
        pt_catch = user['playtime_vn_catch']
        pt_mania = user['playtime_vn_mania']

        acc_std = user['acc_vn_std']
        acc_taiko = user['acc_vn_taiko']
        acc_catch = user['acc_vn_catch']
        acc_mania = user['acc_vn_mania']

        mc_std = user['maxcombo_vn_std']
        mc_taiko = user['maxcombo_vn_taiko']
        mc_catch = user['maxcombo_vn_catch']
        mc_mania = user['maxcombo_vn_mania']

        tscore_std_rx = user['tscore_rx_std']
        tscore_taiko_rx = user['tscore_rx_taiko']
        tscore_catch_rx = user['tscore_rx_catch']

        rscore_std_rx = user['rscore_rx_std']
        rscore_taiko_rx = user['rscore_rx_taiko']
        rscore_catch_rx = user['rscore_rx_catch']

        pp_std_rx = user['pp_rx_std']
        pp_taiko_rx = user['pp_rx_taiko']
        pp_catch_rx = user['pp_rx_catch']

        pc_std_rx = user['plays_rx_std']
        pc_taiko_rx = user['plays_rx_taiko']
        pc_catch_rx = user['plays_rx_catch']

        pt_std_rx = user['playtime_rx_std']
        pt_taiko_rx = user['playtime_rx_taiko']
        pt_catch_rx = user['playtime_rx_catch']

        acc_std_rx = user['acc_rx_std']
        acc_taiko_rx = user['acc_rx_taiko']
        acc_catch_rx = user['acc_rx_catch']

        mc_std_rx = user['maxcombo_rx_std']
        mc_taiko_rx = user['maxcombo_rx_taiko']
        mc_catch_rx = user['maxcombo_rx_catch']

        tscore_std_ap = user['tscore_ap_std']
        rscore_std_ap = user['rscore_ap_std']
        pp_std_ap = user['pp_ap_std']
        pc_std_ap = user['plays_ap_std']
        pt_std_ap = user['playtime_ap_std']
        acc_std_ap = user['acc_ap_std']
        mc_std_ap = user['maxcombo_ap_std']
        
        # LOL
        await glob.postgres.execute(
            'INSERT INTO stats (id, '
            'tscore_std, tscore_taiko, tscore_catch, tscore_mania, '
            'rscore_std, rscore_taiko, rscore_catch, rscore_mania, '
            'pp_std, pp_taiko, pp_catch, pp_mania, '
            'pc_std, pc_taiko, pc_catch, pc_mania, '
            'pt_std, pt_taiko, pt_catch, pt_mania, '
            'acc_std, acc_taiko, acc_catch, acc_mania, '
            'mc_std, mc_taiko, mc_catch, mc_mania, '
            'tscore_std_rx, tscore_taiko_rx, tscore_catch_rx, '
            'rscore_std_rx, rscore_taiko_rx, rscore_catch_rx, '
            'pp_std_rx, pp_taiko_rx, pp_catch_rx, '
            'pc_std_rx, pc_taiko_rx, pc_catch_rx, '
            'pt_std_rx, pt_taiko_rx, pt_catch_rx, '
            'acc_std_rx, acc_taiko_rx, acc_catch_rx, '
            'mc_std_rx, mc_taiko_rx, mc_catch_rx, '
            'tscore_std_ap, '
            'rscore_std_ap, '
            'pp_std_ap, '
            'pc_std_ap, '
            'pt_std_ap, '
            'acc_std_ap, '
            'mc_std_ap) '
            'VALUES ('
            '$1, $2, $3, $4,'
            '$5, $6, $7, $8,'
            '$9, $10, $11, $12,'
            '$13, $14, $15, $16,'
            '$17, $18, $19, $20,'
            '$21, $22, $23, $24,'
            '$25, $26, $27, $28,'
            '$29, $30, $31,'
            '$32, $33, $34,'
            '$35, $36, $37,'
            '$38, $39, $40,'
            '$41, $42, $43,'
            '$44, $45, $46,'
            '$47, $48, $49,'
            '$50,'
            '$51,'
            '$52,'
            '$53,'
            '$54,'
            '$55,'
            '$56,'
            '$57)',
            id,
            tscore_std, tscore_taiko, tscore_catch, tscore_mania,
            rscore_std, rscore_taiko, rscore_catch, rscore_mania,
            pp_std, pp_taiko, pp_catch, pp_mania,
            pc_std, pc_taiko, pc_catch, pc_mania,
            pt_std, pt_taiko, pt_catch, pt_mania,
            acc_std, acc_taiko, acc_catch, acc_mania,
            mc_std, mc_taiko, mc_catch, mc_mania,
            tscore_std_rx, tscore_taiko_rx, tscore_catch_rx,
            rscore_std_rx, rscore_taiko_rx, rscore_catch_rx,
            pp_std_rx, pp_taiko_rx, pp_catch_rx,
            pc_std_rx, pc_taiko_rx, pc_catch_rx,
            pt_std_rx, pt_taiko_rx, pt_catch_rx,
            acc_std_rx, acc_taiko_rx, acc_catch_rx,
            mc_std_rx, mc_taiko_rx, mc_catch_rx,
            tscore_std_ap,
            rscore_std_ap,
            pp_std_ap,
            pc_std_ap,
            pt_std_ap,
            acc_std_ap,
            mc_std_ap
        )
        
        log(f'Inserted user ID {id} into stats database!')
        
    log('All stats converted!')
    
async def convert_scores():
    for table in ('scores_vn', 'scores_rx', 'scores_ap'):
        scores = await glob.sql.fetchall(f'SELECT * FROM {table}')
        
        asahi_table = table
        
        if table == 'scores_vn':
            asahi_table = 'scores'
        
        for score in scores:
            id = score['id']
            md5 = score['map_md5']
            scr = score['score']
            pp = score['pp']
            acc = score['acc']
            combo = score['max_combo']
            mods = score['mods']
            n300 = score['n300']
            n100 = score['n100']
            n50 = score['n50']
            miss = score['nmiss']
            geki = score['ngeki']
            katu = score['nkatu']
            grade = score['grade']
            status = score['status']
            mode = score['mode']
            
            try: # some use unix, other use timestamp
                _time = int(score['play_time'])
            except Exception: # not unix
                _time = score['play_time'].timestamp()
                
            uid = score['userid']
            
            try:
                readable_mods = score['mods_readable']
            except Exception: # not iteki-based gulag
                readable_mods = convert(mods)
            
            fc = score['perfect']
            
            await glob.postgres.execute(
                f'INSERT INTO {asahi_table} ('
                'id, md5, score, pp, '
                'acc, combo, mods, n300, '
                'n100, n50, miss, geki, '
                'katu, grade, status, mode, '
                'time, uid, readable_mods, fc'
                ') VALUES ('
                '$1, $2, $3, $4, '
                '$5, $6, $7, $8, '
                '$9, $10, $11, $12, '
                '$13, $14, $15, $16, '
                '$17, $18, $19, $20'
                ')',
                id, md5, scr, pp,
                acc, combo, mods, n300,
                n100, n50, miss, geki,
                katu, grade, status, mode,
                _time, uid, readable_mods, fc
            )
            
            log(f'Converted score ID {id} on table {asahi_table}!')
            
        log(f'Converted all scores on table {asahi_table}!')

input(
    'Please be aware that before running this script, you should have made a blank database in PostgreSQL for Asahi and have a valid gulag database in MySQL. '
    'If not, please sort that now and run again (Ctrl + C to exit). '
    'Otherwise, press any key to continue!'
)

loop = asyncio.get_event_loop()
loop.run_until_complete(import_db())
loop.run_until_complete(startup())
loop.run_until_complete(convert_users())
loop.run_until_complete(convert_stats())
loop.run_until_complete(convert_scores())
loop.run_until_complete(close_dbs())
log('Migration complete!')
