#!/usr/bin/env python3

import argparse
import mysql.connector
from mysql.connector import errorcode


DB = {
  'user': '',
  'password': '',
  'host': '',
  'database': '',
  'raise_on_warnings': True
}
SHOW_TABLES = 'SHOW TABLES;'
DESCRIBE_TABLE = 'DESCRIBE {};'


def cli_setup():
    parser = argparse.ArgumentParser()
    parser.add_argument('user')
    parser.add_argument('password')
    parser.add_argument('host')
    parser.add_argument('dbname')
    args = parser.parse_args()
    for arg in vars(args):
        if not is_valid_argument(arg):
            return False
    DB['user'] = args.user
    DB['password'] = args.password
    DB['host'] = args.host
    DB['database'] = args.dbname
    return True


def is_valid_argument(arg):
    if arg == '' or arg == None:
        return False
    return True


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


def execute_query(cursor, query):
    try:
        cursor.execute(query)
    except mysql.connector.Error as err:
        print("Failed running query: {}".format(err))


def backup(conn):
    print('Running backup')
    cursor = conn.cursor()
    execute_query(cursor, SHOW_TABLES)
    tables = [table_info[0] for table_info in cursor.fetchall()]
    cursor.close()
    print('Found the following tables: {}'.format(tables))
    for table in tables:
        cursor = conn.cursor()
        execute_query(cursor, DESCRIBE_TABLE.format(table))
        metadata = cursor.fetchall()
        print(metadata)
        cursor.close()
    
    conn.close()


if __name__ == '__main__':
    success = cli_setup()
    if not success:
        print('Invalid db config info. Please provide correct positional arguments. Run --help for help.')
        exit()
    print('Squirelling away...')
    conn = getconnection(DB)
    backup(conn)   