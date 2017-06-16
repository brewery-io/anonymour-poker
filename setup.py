import sys
from config import config
import os
from os import listdir
from os.path import isfile, join
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT, ISOLATION_LEVEL_DEFAULT

def usage():

    print '''

        setup.py <cmd>

        cmd:

            create_db
            setup_db
            nuke_db
            drop_db

    '''
    sys.exit(1)

cmd = sys.argv[1]

if len(sys.argv) > 2:
    usage()

if cmd == 'create_db':

    con = psycopg2.connect(dbname='postgres', user=config.DB.user, host=config.DB.host, password=config.DB.pw)
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    cur.execute('CREATE DATABASE %s;' % config.DB.db)
    con.close()

elif cmd == 'setup_db':

    config_db = 'config/db'

    con = psycopg2.connect(dbname=config.DB.db, user=config.DB.user, host=config.DB.host, password=config.DB.pw)
    con.set_isolation_level(ISOLATION_LEVEL_DEFAULT)
    cur = con.cursor()

    fnames = [fname for fname in listdir(config_db)]

    for fname in fnames:
        with open(os.path.join(config_db, fname), 'r') as f:
            cur.execute(f.read())

    con.commit()
    con.close()

elif cmd == 'nuke_db':

    config_db = 'config/db'

    con = psycopg2.connect(dbname=config.DB.db, user=config.DB.user, host=config.DB.host, password=config.DB.pw)
    con.set_isolation_level(ISOLATION_LEVEL_DEFAULT)
    cur = con.cursor()

    fnames = [fname for fname in listdir(config_db)]

    for fname in fnames:
        cur.execute('DROP TABLE %s;' % fname)

    con.commit()
    con.close()

elif cmd == 'drop_db':

    con = psycopg2.connect(dbname='postgres', user=config.DB.user, host=config.DB.host, password=config.DB.pw)
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    cur.execute('DROP DATABASE %s;' % config.DB.db)
    con.close()

else:
    usage()
