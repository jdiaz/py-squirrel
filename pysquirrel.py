#!/usr/bin/env python3

DB = {
    'port': 3600,
    'host': 'localhost',
    'dbname': '',
    'username': '',
}

def validdb():
    for key in DB:
        if DB[key] == '':
            return False
    return True

def backup():
    print('Running backup')

if __name__ == '__main__':
    print('pysquirrel...')
    if not validdb():
        print('Invalid db connection info. Please update DB object')
        exit()
    backup()   