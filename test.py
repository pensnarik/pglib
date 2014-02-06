#!/usr/bin/env python3

import psycopg2

from pglib import Function
from pglib import Table

conn = psycopg2.connect("dbname=comagic_y host=devbase.uiscom.ru user=postgres")

f = Function(conn)
t = Table(conn)

name = t.customer[232]['name']

print (name)