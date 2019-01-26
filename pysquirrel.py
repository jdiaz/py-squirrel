#!/usr/bin/env python3

import mysql.connector
from mysql.connector import errorcode


DB = {
  'user': 'u',
  'password': 'p',
  'host': '127.0.0.1',
  'database': 'mydb',
  'raise_on_warnings': True
}

SHOW_TABLES = 'SHOW TABLES;'
DESCRIBE_TABLE = 'DESCRIBE TABLE %s;'


def getconnection(config):
    try:
        return mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        conn.close()
        return None


def is_valid_config():
    for key in DB:
        if DB[key] == '' or DB[key] == None:
            return False
    return True


def execute_query(cursor, query):
    try:
        cursor.execute(query)
    except mysql.connector.Error as err:
        print("Failed running query: {}".format(err))


def backup(conn):
    print('Running backup')
    cursor = conn.cursor()
    execute_query(cursor, SHOW_TABLES)
    tables = [table_name[0] for table_name in cursor]
    print('Found the following tables: {}'.format(tables))


if __name__ == '__main__':
    print('Squirelling away...')
    if not is_valid_config():
        print('Invalid db config info. Please update DB dictionary.')
        exit()
    conn = getconnection(DB)
    backup(conn)   