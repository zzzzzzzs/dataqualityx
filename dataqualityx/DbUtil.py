import pymysql


# 查询数据库
def query(cur, sql):
    cur.execute(sql)
    datas = cur.fetchall()
    return datas

def mysql():
    pass


def doris(db_info):
    host = db_info['host']
    port = db_info['port']
    user = db_info['user']
    pw = db_info['pw']
    db = db_info['db']
    conn = pymysql.connect(host=host, user=user, password=pw, db=db, port=port)
    return conn.cursor()


def db(db_info):
    if db_info['type'] == 'mysql':
        pass
    elif db_info['type'] == 'doris':
        return doris(db_info)
    else:
        raise Exception(f'不支持 {db_info["type"]}')
