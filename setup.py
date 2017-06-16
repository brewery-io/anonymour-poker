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

            create_db                   - create database
            setup_db                    - setup tables in database
            nuke_db                     - drop tables from database
            drop_db                     - drop database

            create_room <name>          - create room
                        <buyin>
                        <seats>
                        <type>
            close_room <name>           - close room
            open_room <name>            - open room

    '''
    sys.exit(1)

cmd = sys.argv[1]

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
        cur.execute('DROP TABLE %s;' % fname[:-4])

    con.commit()
    con.close()

elif cmd == 'drop_db':

    con = psycopg2.connect(dbname='postgres', user=config.DB.user, host=config.DB.host, password=config.DB.pw)
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    cur.execute('DROP DATABASE %s;' % config.DB.db)
    con.close()

elif cmd == 'create_room':

    name = sys.argv[2]
    buyin = sys.argv[3]
    seats = sys.argv[4]
    t = sys.argv[5]

    con = psycopg2.connect(dbname=config.DB.db, user=config.DB.user, host=config.DB.host, password=config.DB.pw)
    con.set_isolation_level(ISOLATION_LEVEL_DEFAULT)
    cur = con.cursor()

    cur.execute("INSERT INTO rooms (name, status, buyin, seats, type) VALUES ('%s', 'open', %s, %s, '%s')" % (name, buyin, seats, t))

    con.commit()
    con.close()

elif cmd == 'close_room':

    name = sys.argv[2]

    con = psycopg2.connect(dbname=config.DB.db, user=config.DB.user, host=config.DB.host, password=config.DB.pw)
    con.set_isolation_level(ISOLATION_LEVEL_DEFAULT)
    cur = con.cursor()

    cur.execute("UPDATE rooms SET status = 'closed' WHERE name = '%s' " % name)

    con.commit()
    con.close()

elif cmd == 'open_room':

    name = sys.argv[2]

    con = psycopg2.connect(dbname=config.DB.db, user=config.DB.user, host=config.DB.host, password=config.DB.pw)
    con.set_isolation_level(ISOLATION_LEVEL_DEFAULT)
    cur = con.cursor()

    cur.execute("UPDATE rooms SET status = 'open' WHERE name = '%s' " % name)

    con.commit()
    con.close()

else:
    usage()
