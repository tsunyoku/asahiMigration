from cmyui import AsyncSQLPool, log
from objects import glob
from constants.privs import gulagPrivileges, asahiPrivileges

import asyncpg
import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

async def startup():
    log('Connecting to databases...')

    glob.sql = AsyncSQLPool()
    await glob.sql.connect(glob.config.gulag_sql)
    log('Connected to MySQL!')
    
    glob.postgres = await asyncpg.connect(**glob.config.asahi_postgres)
    log('Connected to PostgreSQL!')
    
async def convert_priv(old_priv):
    new_priv = asahiPrivileges(0)
    new_priv |= asahiPrivileges.Normal # everyone has this no matter what

    if not old_priv & gulagPrivileges.Normal: # restricted
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
    gulag_users = await glob.sql.fetchall(f'SELECT * FROM users')
    
    # create users db
    await glob.postgres.execute(
        'CREATE TABLE public.users ('
        'id integer NOT NULL,'
        'name character varying(16) NOT NULL,'
        "email character varying(254) DEFAULT ''::character varying NOT NULL,"
        'pw text NOT NULL,'
        "country character varying(2) DEFAULT 'xx'::character varying NOT NULL,"
        'priv integer DEFAULT 1 NOT NULL,'
        'safe_name character varying(16) NOT NULL,'
        'clan integer DEFAULT 0 NOT NULL,'
        'freeze_timer bigint DEFAULT 0 NOT NULL,'
        'registered_at bigint NOT NULL,'
        'silence_end bigint DEFAULT 0 NOT NULL,'
        'donor_end bigint DEFAULT 0 NOT NULL'
        ');'
    )
    
    for user in gulag_users:
        id = user['id']
        name = user['name']
        safe_name = user['safe_name']
        email = user['email']
        pw = user['pw_bcrypt'] # absolutely cursed cus asahi doesn't use bcrypt, we will do some trolling in asahi repo for this
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
  
        await glob.postgres.execute('INSERT INTO users (id, name, safe_name, email, pw, country, priv, clan, freeze_timer, registered_at, silence_end, donor_end) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)', id, name, safe_name, email, pw, country, int(asahi_priv), clan, freeze, creation, silence, donor)
        log(f'Inserted {name} into Asahi database!')
        
    # fix auto increment
    last_id = gulag_users[-1]['id']
    await glob.postgres.execute(f'CREATE SEQUENCE users_id_seq START {last_id + 1};')
    await glob.postgres.execute("ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);")
    
    log('All users converted!')

input('Please be aware that before running this script, you should have made a blank database in postgresql for Asahi. If not, please do that now and run again (Ctrl + C to exit). If not, press any key to continue!')

loop = asyncio.get_event_loop()
loop.run_until_complete(startup())

#loop.run_until_complete(convert_users())