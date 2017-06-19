import sys
from config import config
import os
from os import listdir
from os.path import join
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT, ISOLATION_LEVEL_DEFAULT
import subprocess
from passlib.hash import pbkdf2_sha256
from routes import routes
from api import api

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
            close_game <name>           - close game websocket server process for room
            close_room <name>           - close room
            open_room <name>            - open room

    '''
    sys.exit(1)

cmd = sys.argv[1]

def create_db():
    con = psycopg2.connect(dbname='postgres', user=config.DB.user, host=config.DB.host, password=config.DB.pw)
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    cur.execute('CREATE DATABASE %s;' % config.DB.db)
    con.close()

def setup_db():
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

def nuke_db():
    config_db = 'config/db'

    con = psycopg2.connect(dbname=config.DB.db, user=config.DB.user, host=config.DB.host, password=config.DB.pw)
    con.set_isolation_level(ISOLATION_LEVEL_DEFAULT)
    cur = con.cursor()

    fnames = [fname for fname in listdir(config_db)]

    for fname in fnames:
        cur.execute('DROP TABLE %s;' % fname[:-4])

    con.commit()
    con.close()

def drop_db():
    con = psycopg2.connect(dbname='postgres', user=config.DB.user, host=config.DB.host, password=config.DB.pw)
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    cur.execute('DROP DATABASE %s;' % config.DB.db)
    con.close()

def create_room(name, buyin, seats, t):

    con = psycopg2.connect(dbname=config.DB.db, user=config.DB.user, host=config.DB.host, password=config.DB.pw)
    con.set_isolation_level(ISOLATION_LEVEL_DEFAULT)
    cur = con.cursor()

    cur.execute("INSERT INTO rooms (name, status, buyin, seats, type) VALUES ('%s', 'closed', %s, %s, '%s')" % (name, buyin, seats, t))

    con.commit()
    con.close()

def close_room(name):
    con = psycopg2.connect(dbname=config.DB.db, user=config.DB.user, host=config.DB.host, password=config.DB.pw)
    con.set_isolation_level(ISOLATION_LEVEL_DEFAULT)
    cur = con.cursor()

    cur.execute("UPDATE rooms SET status = 'closed' WHERE name = '%s' " % name)

    con.commit()
    con.close()

def close_game(name):
    con = psycopg2.connect(dbname=config.DB.db, user=config.DB.user, host=config.DB.host, password=config.DB.pw)
    cur = con.cursor()
    con.set_isolation_level(ISOLATION_LEVEL_DEFAULT)

    cur.execute("SELECT * FROM rooms WHERE name = '%s'" % name)
    room = cur.fetchone()
    room_id = room[0]
    proc_id = room[6]

    subprocess.Popen(['kill', '-9', str(proc_id)])

    cur.execute("UPDATE rooms SET pid = %s WHERE id = %s" % (-1, room_id))
    cur.execute("UPDATE rooms SET port = %s WHERE id = %s" % (-1, room_id))

    con.commit()
    con.close()

def open_room(name):
    con = psycopg2.connect(dbname=config.DB.db, user=config.DB.user, host=config.DB.host, password=config.DB.pw)
    con.set_isolation_level(ISOLATION_LEVEL_DEFAULT)
    cur = con.cursor()

    cur.execute("UPDATE rooms SET status = 'open' WHERE name = '%s' RETURNING id " % name)
    room_id = cur.fetchone()[0]

    port = config.Game.port + room_id

    with open('logs/game.log', 'a') as f:
        proc = subprocess.Popen(['python', 'api/game.py', '--port', str(port)], stdout = f)

    cur.execute("UPDATE rooms SET pid = %s WHERE id = %s" % (proc.pid, room_id))
    cur.execute("UPDATE rooms SET port = %s WHERE id = %s" % (port, room_id))

    con.commit()
    con.close()

def create_user(username, password):

    password = pbkdf2_sha256.hash(password)

    con = psycopg2.connect(dbname=config.DB.db, user=config.DB.user, host=config.DB.host, password=config.DB.pw)
    con.set_isolation_level(ISOLATION_LEVEL_DEFAULT)
    cur = con.cursor()

    cur.execute("INSERT INTO users (username, password) VALUES ('%s', '%s')" % (username, password))

    con.commit()
    con.close()


if cmd == 'create_db':
    create_db()

elif cmd == 'setup_db':
    setup_db()

elif cmd == 'nuke_db':
    nuke_db()

elif cmd == 'drop_db':
    drop_db()

elif cmd == 'create_room':

    name = sys.argv[2]
    buyin = sys.argv[3]
    seats = sys.argv[4]
    t = sys.argv[5]
    create_room(name, buying, seats, t)

elif cmd == 'close_room':

    name = sys.argv[2]
    close_room(name)

elif cmd == 'close_game':

    name = sys.argv[2]
    close_game(name)

elif cmd == 'open_room':

    name = sys.argv[2]
    open_room(name)

elif cmd == 'create_user':

    username = sys.argv[2]
    password = sys.argv[3]
    create_user(username, password)

elif cmd == 'run_routes':
    routes.start()

elif cmd == 'run_api':
    api.start()

elif cmd == 'init':
    drop_db()
    create_db()
    setup_db()
    create_room('Room One', 3, 8, 'Winner Takes All')
    create_room('Room Two', 2, 2, 'Winner Takes All')
    create_user('user', 'pass')
    create_user('user2', 'pass')


else:
    usage()
