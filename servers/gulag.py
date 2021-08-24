from cmyui import log, Ansi

from constants.privs import gulagPrivileges, asahiPrivileges
from constants.mods import convert
from objects import glob

import os

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
    gulag_users = await glob.input.fetch('SELECT * FROM users')

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

        userpage = user['uptext']

        if frozen:
            asahi_priv |= asahiPrivileges.Frozen

        await glob.output.execute(
            'INSERT INTO users '
            '(id, name, safe_name, email, pw, country, priv, clan, freeze_timer, registered_at, silence_end, donor_end, userpage) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            [id, name, safe_name, email, pw, country, int(asahi_priv), clan, freeze, creation, silence, donor, userpage]
        )

        log(f'Inserted {name} into users database!')

    # fix auto increment
    last_id = int(gulag_users[-1]['id'])
    await glob.output.execute(f'ALTER TABLE users AUTO_INCREMENT={last_id + 1}')

    log('All users converted!')
    
async def convert_stats():
    gulag_stats = await glob.input.fetch('SELECT * FROM stats')
    
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
        await glob.output.execute(
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
            '%s, %s, %s, %s,'
            '%s, %s, %s, %s,'
            '%s, %s, %s, %s,'
            '%s, %s, %s, %s,'
            '%s, %s, %s, %s,'
            '%s, %s, %s, %s,'
            '%s, %s, %s, %s,'
            '%s, %s, %s,'
            '%s, %s, %s,'
            '%s, %s, %s,'
            '%s, %s, %s,'
            '%s, %s, %s,'
            '%s, %s, %s,'
            '%s, %s, %s,'
            '%s,'
            '%s,'
            '%s,'
            '%s,'
            '%s,'
            '%s,'
            '%s,'
            '%s)',
            [id,
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
            mc_std_ap]
        )
        
        log(f'Inserted user ID {id} into stats database!')

    # fix auto increment
    last_id = int(gulag_stats[-1]['id'])
    await glob.output.execute(f"ALTER TABLE stats AUTO_INCREMENT={last_id + 1}")

    log('All stats converted!')

async def convert_stats_cheat():
    gulag_stats = await glob.input.fetch('SELECT * FROM stats')
    
    for user in gulag_stats:
        id = user['id']

        tscore_std = user['tscore_cheat_vn_std']
        tscore_taiko = user['tscore_cheat_vn_taiko']
        tscore_catch = user['tscore_cheat_vn_catch']
        tscore_mania = user['tscore_cheat_vn_mania']

        rscore_std = user['rscore_cheat_vn_std']
        rscore_taiko = user['rscore_cheat_vn_taiko']
        rscore_catch = user['rscore_cheat_vn_catch']
        rscore_mania = user['rscore_cheat_vn_mania']
        
        pp_std = user['pp_cheat_vn_std']
        pp_taiko = user['pp_cheat_vn_taiko']
        pp_catch = user['pp_cheat_vn_catch']
        pp_mania = user['pp_cheat_vn_mania']
        
        pc_std = user['plays_cheat_vn_std']
        pc_taiko = user['plays_cheat_vn_taiko']
        pc_catch = user['plays_cheat_vn_catch']
        pc_mania = user['plays_cheat_vn_mania']

        pt_std = user['playtime_cheat_vn_std']
        pt_taiko = user['playtime_cheat_vn_taiko']
        pt_catch = user['playtime_cheat_vn_catch']
        pt_mania = user['playtime_cheat_vn_mania']

        acc_std = user['acc_cheat_vn_std']
        acc_taiko = user['acc_cheat_vn_taiko']
        acc_catch = user['acc_cheat_vn_catch']
        acc_mania = user['acc_cheat_vn_mania']

        mc_std = user['maxcombo_cheat_vn_std']
        mc_taiko = user['maxcombo_cheat_vn_taiko']
        mc_catch = user['maxcombo_cheat_vn_catch']
        mc_mania = user['maxcombo_cheat_vn_mania']

        tscore_std_rx = user['tscore_cheat_rx_std']
        tscore_taiko_rx = user['tscore_cheat_rx_taiko']
        tscore_catch_rx = user['tscore_cheat_rx_catch']

        rscore_std_rx = user['rscore_cheat_rx_std']
        rscore_taiko_rx = user['rscore_cheat_rx_taiko']
        rscore_catch_rx = user['rscore_cheat_rx_catch']

        pp_std_rx = user['pp_cheat_rx_std']
        pp_taiko_rx = user['pp_cheat_rx_taiko']
        pp_catch_rx = user['pp_cheat_rx_catch']

        pc_std_rx = user['plays_cheat_rx_std']
        pc_taiko_rx = user['plays_cheat_rx_taiko']
        pc_catch_rx = user['plays_cheat_rx_catch']

        pt_std_rx = user['playtime_cheat_rx_std']
        pt_taiko_rx = user['playtime_cheat_rx_taiko']
        pt_catch_rx = user['playtime_cheat_rx_catch']

        acc_std_rx = user['acc_cheat_rx_std']
        acc_taiko_rx = user['acc_cheat_rx_taiko']
        acc_catch_rx = user['acc_cheat_rx_catch']

        mc_std_rx = user['maxcombo_cheat_rx_std']
        mc_taiko_rx = user['maxcombo_cheat_rx_taiko']
        mc_catch_rx = user['maxcombo_cheat_rx_catch']

        tscore_std_ap = user['tscore_cheat_ap_std']
        rscore_std_ap = user['rscore_cheat_ap_std']
        pp_std_ap = user['pp_cheat_ap_std']
        pc_std_ap = user['plays_cheat_ap_std']
        pt_std_ap = user['playtime_cheat_ap_std']
        acc_std_ap = user['acc_cheat_ap_std']
        mc_std_ap = user['maxcombo_cheat_ap_std']
        
        # LOL
        await glob.output.execute(
            'REPLACE INTO stats (id, '
            'tscore_std_cheat, tscore_taiko_cheat, tscore_catch_cheat, tscore_mania_cheat, '
            'rscore_std_cheat, rscore_taiko_cheat, rscore_catch_cheat, rscore_mania_cheat, '
            'pp_std_cheat, pp_taiko_cheat, pp_catch_cheat, pp_mania_cheat, '
            'pc_std_cheat, pc_taiko_cheat, pc_catch_cheat, pc_mania_cheat, '
            'pt_std_cheat, pt_taiko_cheat, pt_catch_cheat, pt_mania_cheat, '
            'acc_std_cheat, acc_taiko_cheat, acc_catch_cheat, acc_mania_cheat, '
            'mc_std_cheat, mc_taiko_cheat, mc_catch_cheat, mc_mania_cheat, '
            'tscore_std_rx_cheat, tscore_taiko_rx_cheat, tscore_catch_rx_cheat, '
            'rscore_std_rx_cheat, rscore_taiko_rx_cheat, rscore_catch_rx_cheat, '
            'pp_std_rx_cheat, pp_taiko_rx_cheat, pp_catch_rx_cheat, '
            'pc_std_rx_cheat, pc_taiko_rx_cheat, pc_catch_rx_cheat, '
            'pt_std_rx_cheat, pt_taiko_rx_cheat, pt_catch_rx_cheat, '
            'acc_std_rx_cheat, acc_taiko_rx_cheat, acc_catch_rx_cheat, '
            'mc_std_rx_cheat, mc_taiko_rx_cheat, mc_catch_rx_cheat, '
            'tscore_std_ap_cheat, '
            'rscore_std_ap_cheat, '
            'pp_std_ap_cheat, '
            'pc_std_ap_cheat, '
            'pt_std_ap_cheat, '
            'acc_std_ap_cheat, '
            'mc_std_ap_cheat) '
            'VALUES ('
            '%s, %s, %s, %s,'
            '%s, %s, %s, %s,'
            '%s, %s, %s, %s,'
            '%s, %s, %s, %s,'
            '%s, %s, %s, %s,'
            '%s, %s, %s, %s,'
            '%s, %s, %s, %s,'
            '%s, %s, %s,'
            '%s, %s, %s,'
            '%s, %s, %s,'
            '%s, %s, %s,'
            '%s, %s, %s,'
            '%s, %s, %s,'
            '%s, %s, %s,'
            '%s,'
            '%s,'
            '%s,'
            '%s,'
            '%s,'
            '%s,'
            '%s,'
            '%s)',
            [id,
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
            mc_std_ap]
        )
        
        log(f'Inserted user ID {id} into cheat stats database!')

    log('All cheat stats converted!')
    
async def convert_scores():
    for table in ('scores_vn', 'scores_rx', 'scores_ap'):
        scores = await glob.input.fetch(f'SELECT * FROM {table}')
        
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
            
            await glob.output.execute(
                f'INSERT INTO {asahi_table} ('
                'id, md5, score, pp, '
                'acc, combo, mods, n300, '
                'n100, n50, miss, geki, '
                'katu, grade, status, mode, '
                'time, uid, readable_mods, fc'
                ') VALUES ('
                '%s, %s, %s, %s, '
                '%s, %s, %s, %s, '
                '%s, %s, %s, %s, '
                '%s, %s, %s, %s, '
                '%s, %s, %s, %s'
                ')',
                [id, md5, scr, pp,
                acc, combo, mods, n300,
                n100, n50, miss, geki,
                katu, grade, status, mode,
                _time, uid, readable_mods, fc]
            )
            
            log(f'Converted score ID {id} on table {asahi_table}!')

        # fix auto increment
        last_id = int(scores[-1]['id'])
        await glob.output.execute(f"ALTER TABLE {asahi_table} AUTO_INCREMENT={last_id + 1}")
        log(f'Converted all scores on table {asahi_table}!')

async def convert_scores_cheat():
    for table in ('scores_vn_cheat', 'scores_rx_cheat', 'scores_ap_cheat'):
        scores = await glob.input.fetch(f'SELECT * FROM {table}')
        
        asahi_table = table
        
        if table == 'scores_vn_cheat':
            asahi_table = 'scores_cheat'
        
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
            timewarp = score['timewarp']
            
            await glob.output.execute(
                f'INSERT INTO {asahi_table} ('
                'id, md5, score, pp, '
                'acc, combo, mods, n300, '
                'n100, n50, miss, geki, '
                'katu, grade, status, mode, '
                'time, uid, readable_mods, fc, timewarp'
                ') VALUES ('
                '%s, %s, %s, %s, '
                '%s, %s, %s, %s, '
                '%s, %s, %s, %s, '
                '%s, %s, %s, %s, '
                '%s, %s, %s, %s, %s'
                ')',
                [id, md5, scr, pp,
                acc, combo, mods, n300,
                n100, n50, miss, geki,
                katu, grade, status, mode,
                _time, uid, readable_mods, fc, timewarp]
            )
            
            log(f'Converted score ID {id} on table {asahi_table}!')

        # fix auto increment
        last_id = int(scores[-1]['id'])
        await glob.output.execute(f"ALTER TABLE {asahi_table} AUTO_INCREMENT={last_id + 1}")
        log(f'Converted all scores on table {asahi_table}!')

async def convert_maps():
    gulag_maps = await glob.input.fetch('SELECT * FROM maps')
    
    for _map in gulag_maps:
        id = _map['id']
        sid = _map['set_id']
        md5 = _map['md5']
        
        bpm = _map['bpm']
        cs = _map['cs']
        ar = _map['ar']
        od = _map['od']
        hp = _map['hp']
        sr = _map['diff']
        mode = _map['mode']
        
        artist = _map['artist']
        title = _map['title']
        diff = _map['version']
        mapper = _map['creator']
        status = _map['status']
        
        frozen = _map['frozen']
        update = int(_map['last_update'].timestamp())
        nc = _map['last_check'] # not sure if current gulag has this named the same?
        
        plays = _map['plays']
        passes = _map['passes']
        
        await glob.output.execute(
            'INSERT INTO maps ('
            '`id`, sid, md5, '
            'bpm, cs, ar, od, hp, sr, mode, '
            'artist, title, diff, mapper, `status`, '
            '`frozen`, `update`, `nc`, '
            '`plays`, `passes`'
            ') VALUES ('
            '%s, %s, %s, '
            '%s, %s, %s, %s, %s, %s, %s, '
            '%s, %s, %s, %s, %s, '
            '%s, %s, %s, '
            '%s, %s'
            ')',
            [id, sid, md5,
            bpm, cs, ar, od, hp, sr, mode,
            artist, title, diff, mapper, status,
            frozen, update, nc,
            plays, passes]
        )
        
        log(f'Converted {artist} - {title} [{diff}] into maps table!')
        
    log('Converted all maps!')
    
async def convert_client_hashes():
    gulag_hashes = await glob.input.fetch('SELECT * FROM client_hashes')
    
    for entry in gulag_hashes:
        uid = entry['userid']
        mac_address = entry['adapters']
        uninstall_id = entry['uninstall_id']
        disk_serial = entry['disk_serial']
        ip = entry['ip']
        occurrences = entry['occurrences']
        
        try:
            await glob.output.execute(
                'INSERT INTO user_hashes ('
                'uid, mac_address, uninstall_id, disk_serial, ip, occurrences'
                ') VALUES ('
                '%s, %s, %s, %s, %s, %s)',
                [uid, mac_address, uninstall_id, disk_serial, ip, occurrences]
            )
        except Exception:
            continue # already in db, just skip
        
    log('Converted all client hashes!')

async def convert_friends():
    gulag_friends = await glob.input.fetch('SELECT * FROM friendships')
    
    for fr in gulag_friends:
        user1 = fr['user1']
        user2 = fr['user2']

        await glob.output.execute('INSERT INTO friends (user1, user2) VALUES (%s, %s)', [user1, user2])
        
    log('Converted all friendships!')
    
async def convert_achs():
    gulag_achs = await glob.input.fetch('SELECT * FROM user_achievements')
    
    for a in gulag_achs:
        uid = a['userid']
        ach = a['achid']
        
        await glob.output.execute('INSERT INTO user_achievements (uid, ach) VALUES (%s, %s)', [uid, ach])
        
    log('Converted all user achievements!')

async def convert_achs_cheat():
    gulag_achs = await glob.input.fetch('SELECT * FROM user_achievements_cheat')
    
    for a in gulag_achs:
        uid = a['userid']
        ach = a['achid']
        
        await glob.output.execute('INSERT IGNORE INTO user_achievements_cheat (uid, ach) VALUES (%s, %s)', [uid, ach])
        
    log('Converted all cheat user achievements!')

async def convert_clans():
    gulag_clans = await glob.input.fetch('SELECT * FROM clans')

    for clan in gulag_clans:
        await glob.output.execute(
            'INSERT INTO clans (`id`, `name`, `tag`, `owner`) VALUES ('
            '%s, %s, %s, %s)',
            [clan['id'], clan['name'], clan['tag'], clan['owner']]
        )

    log('Converted all clans!')

async def convert_favourites():
    gulag_favs = await glob.input.fetch('SELECT * FROM favourites')

    for fav in gulag_favs:
        await glob.output.execute('INSERT INTO favourites (uid, sid) VALUES (%s, %s)', [fav['userid'], fav['setid']])

    log('Converted all favourites!')

async def convert_ratings():
    gulag_rs = await glob.input.fetch('SELECT * FROM ratings')

    for r in gulag_rs:
        await glob.output.execute(
            'INSERT INTO ratings (uid, md5, rating) VALUES ('
            '%s, %s, %s)',
            [
                r['userid'], r['map_md5'], r['rating']
            ]
        )

async def migrate_data():
    os.system(f'mkdir {glob.config.new_path}/resources')
    f = f'{glob.config.new_path}/resources'

    old_replays = f'{glob.config.old_path}/.data/osr'
    for _mode in ('', '_rx', '_ap'): os.system(f'mkdir {f}/replays{_mode} && mv {old_replays}{_mode} {f}/replays{_mode}')
    log('Moved all replays!')

    os.system(f'mkdir {f}/screenshots && mv {glob.config.old_path}/.data/ss {f}/screenshots')
    log('Moved all screenshots!')

    os.system(f'mkdir {f}/maps && mv {glob.config.old_path}/.data/osu {f}/maps')
    log('Moved all maps!')

    os.system(f'mkdir {f}/avatars && mv {glob.config.old_path}/.data/avatars {f}/avatars')
    log('Moved all avatars!')

    os.system(f'mkdir {f}/banners && mv {glob.config.old_path}/.data/banners {f}/banners')
    log('Moved all banners!')

async def migrate_data_cheat():
    old_replays = f'{glob.config.old_path_cheat}/.data/osr'
    for _mode in ('', '_rx', '_ap'): os.system(f'mkdir {f}/replays{_mode} && mv {old_replays}{_mode} {f}/replays{_mode}_cheat')
    log('Moved all replays!')

    os.system(f'mkdir {f}/screenshots && mv {glob.config.old_path_cheat}/.data/ss {f}/screenshots')
    log('Moved all screenshots!')

    os.system(f'mkdir {f}/maps && mv {glob.config.old_path_cheat}/.data/osu {f}/maps')
    log('Moved all maps!')

    os.system(f'mkdir {f}/avatars && mv {glob.config.old_path_cheat}/.data/avatars {f}/avatars')
    log('Moved all avatars!')

    os.system(f'mkdir {f}/banners && mv {glob.config.old_path_cheat}/.data/banners {f}/banners')
    log('Moved all banners!')
