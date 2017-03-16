import unittest
import datetime
import sqlite3
from project.models import Item
import project.settings


class SerializerTest(unittest.TestCase):
    def test_create(self):
        s = Item()
        conn = sqlite3.connect(project.settings.DATABASE)
        s.create(
            name='aaa',
            create_date=datetime.datetime.now(),
            value=50,
            to_date=datetime.datetime.now(),
            prise=150,
            provider='OOO "TRADE MASTER"')
        r = s.commit()
        self.assertEqual(s.get(s.all().pop()[0])[0], conn.execute('SELECT max(id) from item;').fetchone()[0])

    def test_get(self):
        s = Item().get(1)
        self.assertEqual(s, (1, '3', '2017-03-07 10:56:39', 3.0, '2017-03-07 10:56:39', 4.0, '5'))

    def test_all(self):
        conn = sqlite3.connect(project.settings.DATABASE)
        s = Item().all()
        self.assertEqual(s, conn.execute("select * from item;").fetchall())

    def test_update(self):
        conn = sqlite3.connect(project.settings.DATABASE)
        s = Item()
        s.update(id_=conn.execute('SELECT max(id) from item;').fetchone()[0], name='3')
        s.commit()
        self.assertEqual(s.get(conn.execute('SELECT max(id) from item;').fetchone()[0]),
                         conn.execute(
                             'SELECT * from item WHERE id = %s;' % conn.execute('SELECT max(id) from item;')
                             .fetchone()[0]).fetchone())

    def test_delete(self):
        conn = sqlite3.connect(project.settings.DATABASE)
        s = Item()
        max_id = conn.execute('SELECT max(id) from item;').fetchone()[0]
        s.delete(max_id)
        s.commit()
        self.assertLess(conn.execute('SELECT max(id) from item;').fetchone()[0], max_id)
