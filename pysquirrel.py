#!/usr/bin/env python3

import argparse
import datetime
import mysql.connector
from mysql.connector import errorcode


DB = {
  'raise_on_warnings': True
}
SHOW_TABLES = 'SHOW TABLES;'
DESCRIBE_TABLE = 'DESCRIBE {}'
SELECT_ALL_FROM_TABLE = 'SELECT * FROM {};'


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
            print('Something is wrong with your user name or password')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('Database does not exist')
        else:
            print(err)
    else:
        conn.close()
        return None


def execute_query(cursor, query):
    try:
        cursor.execute(query)
    except mysql.connector.Error as err:
        print("Failed running query: {}" % err)


def backup(conn):
    print('Creating SQL backup')
    cursor = conn.cursor()
    execute_query(cursor, SHOW_TABLES)
    tables = [table_info[0] for table_info in cursor.fetchall()]
    cursor.close()

    print('=================================================')
    print('========= Found the following TABLES ============')
    print('=================================================')
    print(f'\t{tables}')

    table_column_map = dict()
    table_metadata_map = dict()
    for table in tables:
        cursor = conn.cursor()
        execute_query(cursor, DESCRIBE_TABLE.format(table))
        metadata = cursor.fetchall()
        table_metadata_map[table] = metadata
        columns = [column[0] for column in metadata]
        table_column_map[table] = columns
        cursor.close()

    print('=================================================')
    print('==== Now creating DROP and CREATE statements ====')
    print('=================================================')

    f = open('{}_backup_{}.sql'.format(DB['database'], datetime.datetime.now().strftime('%s')), 'w+')
    for table in table_metadata_map:
        create_table = create_sql_create_table_statement(table, table_metadata_map[table])
        drop_table = create_sql_drop_table_statement(table)
        f.write('{}\n'.format(drop_table))
        f.write('{}\n'.format(create_table))
        print(f'\t{drop_table}')
        print(f'\t{create_table}')

    print('=================================================')
    print('======== Now creating INSERT statements =========')
    print('=================================================')
    for table in tables:
        print('\tQuerying: {}\n'.format(table))
        cursor = conn.cursor()
        execute_query(cursor, SELECT_ALL_FROM_TABLE.format(table))
        for row in cursor:
            columns = table_column_map[table]
            insert_record = create_sql_insert_statement(table, columns, row)
            f.write('{}\n'.format(insert_record))
            print(f'\t{insert_record}')
        cursor.close()

    conn.close()
    f.close()


def create_sql_create_table_statement(table, table_metada):
    statement_parts = ['CREATE TABLE {} (\n'.format(table)]
    n = len(table_metada) 
    for i in range(n):
        column_metadata = table_metada[i]
        statement_parts.append('\t{} {}'.format(column_metadata[0], column_metadata[1]))
        if i != n - 1:
            statement_parts.append(',\n')
    statement_parts.append('\n);')
    return ''.join(statement_parts)


def create_sql_drop_table_statement(table):
    return 'DROP TABLE {};'.format(table)


def create_sql_insert_statement(table, columns, row):
    statement_parts = ['INSERT INTO {} VALUES ('.format(table)]
    n = len(columns)
    for i in range(n):
        placeholder = '{}'
        if type(row[i]) == str:
            placeholder = "'{}'"
        statement_parts.append(placeholder.format(row[i]))
        if i != n - 1:
            statement_parts.append(', ')
    statement_parts.append(');')
    return ''.join(statement_parts)


if __name__ == '__main__':
    success = cli_setup()
    if not success:
        print('Invalid db config info. Please provide correct positional arguments: <user> <pw> <host> <dbname>')
        exit(1)
    print('Pysquirrel running...')
    conn = getconnection(DB)
    backup(conn)
    print('Completed')
    exit(0)
