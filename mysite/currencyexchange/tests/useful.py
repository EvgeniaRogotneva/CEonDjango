import psycopg2
import base64
from datetime import datetime

IVAN_KEY = "SXZhbkl2YW5vdg=="
SUPER_KEY = 'QmlnQm9zcw=='


db = {'currencyexchange_featureflagrawsql': 'currencyexchange_featureflagrawsql',
      'currencyexchange_key': 'currencyexchange_key',
      'currencyexchange_permission': 'currencyexchange_permission',
      'auth_group': 'auth_group',
      'auth_group_permissions': 'auth_group_permissions',
      'auth_permission': 'auth_permission',
      'auth_user': 'auth_user',
      'auth_user_groups': 'auth_user_groups',
      'auth_user_user_permissions': 'auth_user_user_permissions',
      'currencyexchange_timeandcourse': 'currencyexchange_timeandcourse',
      }


def clear_tables():
    conn = psycopg2.connect(host='127.0.0.1', database='currencyexchange', user='postgres', password='root')
    conn.autocommit = True
    for table in db:
        s = 'delete from {} *'.format(table)
        cur = conn.cursor()
        cur.execute(s)


def add_feature_flag(user):
    with psycopg2.connect(host='127.0.0.1', database='currencyexchange', user='postgres', password='root') as conn:
        conn.autocommit = True
        s = "insert into currencyexchange_featureflagrawsql (user_id) values ('{}')".format(user)
        cur = conn.cursor()
        cur.execute(s)


def get_feature_flag(user):
    with psycopg2.connect(host='127.0.0.1', database='currencyexchange', user='postgres', password='root') as conn:
        conn.autocommit = True
        s = "select * currencyexchange_featureflagrawsql  where user_id = '{}'".format(user)
        conn.cursor().execute(s)
        return conn.cursor().fetchone()


def add_courses_to_bd(info):
    conn = psycopg2.connect(host='127.0.0.1', database='currencyexchange', user='postgres', password='root')
    conn.autocommit = True
    for code, time, rate in info:
        s = "insert into currencyexchange_timeandcourse (currency_code, time, rate) values ('{}', '{}', '{}')".format(
            code, time, rate
        )
        cur = conn.cursor()
        cur.execute(s)


def add_key_to_bd(username, id):
    conn = psycopg2.connect(host='127.0.0.1', database='currencyexchange', user='postgres', password='root')
    conn.autocommit = True
    s = "insert into currencyexchange_key (user_id, key) values ('{}', '{}');".format(
        id, base64.b64encode(username.encode()).decode('ascii'))
    cur = conn.cursor()
    cur.execute(s)


def add_user_and_key_to_bd(username, first_name, last_name, password, email, is_superuser=False, is_staff=False,
                           is_active=True, date_joined=datetime.date):
    conn = psycopg2.connect(host='127.0.0.1', database='currencyexchange', user='postgres', password='root')
    conn.autocommit = True
    s = "insert into auth_user (username, first_name, last_name, password, email, is_superuser, is_staff, " \
        "is_active, date_joined) values ('{}', '{}', '{}', '{}', '{}', {}, {}, {}, '{}') returning id;" \
        .format(username, first_name, last_name, password, email, is_superuser, is_staff, is_active, date_joined)
    cur = conn.cursor()
    cur.execute(s)
    id = cur.fetchone()
    add_key_to_bd(username, id[0])
    return id


def add_permission(id, access, resource):
    conn = psycopg2.connect(host='127.0.0.1', database='currencyexchange', user='postgres', password='root')
    conn.autocommit = True
    s = "insert into currencyexchange_permission (access, resource, user_id) values ('{}', '{}', '{}');" \
        .format(access, resource, id[0])
    cur = conn.cursor()
    cur.execute(s)
