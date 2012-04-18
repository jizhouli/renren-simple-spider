#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' mysql handle, use unicode.
'''

import os
import sys
import types
import time

try:
    import MySQLdb
    from _mysql_exceptions import OperationalError, ProgrammingError
except Exception, e:
    print >>sys.stderr, str(e)
    print >>sys.stderr, 'try python-mysqldb, for debian/ubuntu: sudo apt-get install python-mysqldb'

class Mysql:
    def __init__(self, host, user, password, db, charset = 'utf8', port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset
        self.port = port
        self.conn = None
        self.reconnect = False
        self.connect()

    def show(self):
        print 'connect database %s: mysql://%s:%s@%s/%s' % (self.db, self.user, self.password, self.host, self.db)
        print "mysql -h %s -u%s -p'%s' %s -P %d" % (self.host, self.user, self.password, self.db, self.port)
        return

    def get_fields(self, table):
        sql = 'desc %s' % table
        a = self.get_all_dict(sql)
        ret = [i['Field'] for i in a]
        return ret

    def connect(self):
        ret = True
        try:
            self.conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.db, charset=self.charset, port=self.port)
            self.cursor = self.conn.cursor()
            self.cursor.execute('SET NAMES %s' % self.charset)
            self.cursor.execute('SET CHARACTER_SET_CLIENT=%s' % self.charset)
            self.cursor.execute('SET CHARACTER_SET_RESULTS=%s' % self.charset)
            self.conn.commit()  # commit any pending transactions to the database
        except MySQLdb.Error, e:
            print >>sys.stderr, 'umysql connect error %s: %s' % (__file__, str(e))
            ret = False
        return ret

    def execute(self, sql, args=None):
        if type(sql) is not types.UnicodeType:
            sql = sql.decode(self.charset, 'ignore')
        if not self.reconnect:
            self.cursor.execute(sql, args)
            self.conn.commit()
        else:
            while True:
                try:
                    self.cursor.execute(sql, args)
                    self.conn.commit()
                except Exception, e:
                #except OperationalError, e:
                    print >>sys.stderr, 'OperationalError:', str(e)
                    if True:
                        print >>sys.stderr, '[python-mysqldb] reconnect ...'
                        self.connect()
                    else:
                        continue
                break
        return

    def execute_many(self, sql, args=None, step=128):
        if not args: return
        if type(sql) is not types.UnicodeType:
            sql = sql.decode(self.charset, 'ignore')
        index = 0
        while index < len(args):
            self.cursor.execute_many(sql, args[index:index+step])
            index += step
        self.conn.commit()

    def get_one(self, sql, args=None):
        ret = None
        self.execute(sql, args)
        rs = self.cursor.fetchone()
        if rs:
            ret = rs[0]
        return ret

    def get_one_dict(self, sql, args=None):
        result = None
        self.execute(sql, args)
        rs = self.cursor.fetchone()
        fields = [i[0] for i in self.cursor.description]
        if rs and len(rs) == len(fields):
            result = dict(zip(fields, rs))
        return result

    def fetch_one(self, sql, args=None):
        self.execute(sql, args)
        rs = self.cursor.fetchone()
        return rs

    def get_all(self, sql, args=None):
        ret = []
        self.execute(sql, args)
        rs = self.cursor.fetchall()
        for row in rs:
            ret.append(row[0])
        return ret

    def get_all_dict(self, sql, args=None):
        ret = []
        self.execute(sql, args)
        rs = self.cursor.fetchall()
        fields = [i[0] for i in self.cursor.description]
        for row in rs:
            j = 0
            temp = {}
            for item in row:
                temp[fields[j]] = item
                j += 1
            if temp:
                ret.append(temp)
        return ret

    def close(self):
        self.conn.close()
        self.conn = None

    def __del__(self):
        if self.conn != None:
            self.close()

def main():
    print 'test ...'
    m = Mysql(host='192.168.0.24', user='hotel_data', password='kooxoo', db='dujia', port=3307)
    m.show()
    #ret = m.get_one('SELECT * FROM t_low_price limit 10;')
    #print type(ret), repr(ret), ret
    ret = m.get_all_dict('SELECT * FROM dujia_src_info limit 10;')
    print type(ret), repr(ret), ret
    
if __name__ == '__main__':
    main()
