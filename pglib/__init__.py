import re
import sys
import psycopg2
import psycopg2.extras

def sql_execute(conn, query, args=[], limit=0):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(query, args)
    res = cursor.fetchall()
    cursor.close()

    if limit == 1:
        if res:
            if len(res[0]) == 1:
                return res[0][0]
            else:
                return dict(res[0])
        else:
            return None
    return res

class Function:
    def __init__(self, conn, name=None):
        self.conn = conn
        self.name = name

    def __call__(self, *args, **kwargs):
        q = 'select * from %s(%s) as result' % (self.name, ', '.join(['%s'] * len(args) ) )

        return sql_execute(self.conn, q, args)

    def __getattr__(self, name):
        return Function(self.conn, self.name + '.' + name if self.name else name)

class Table:
    def __init__(self, conn, name=None):
        self.conn = conn
        self.name = name

    def __getitem__(self, id):
        return sql_execute(self.conn, 'select * from %s where id = %s' %  (self.name, id), 1)

    def __setitem__(self, id, values):
        vals = ','.join(['%s=$%s%s' % (k, i+2, type_indexes.get(values[k].__class__))
                         for i, k in enumerate(values.keys())])
        return sql_execute(self.conn, 'update %s set %s where id = $1i' %
                           (self.name, vals), [id] + values.values())

    def __getattr__(self, name):
        return Table(self.conn, self.name + '.' + name if self.name else name)

class Tables:
    def __getattr__(self, name):
        return Table(name)