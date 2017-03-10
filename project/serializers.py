import settings
import sqlite3


class Serializer:
    def __init__(self):
        self.db_name = settings.DATABASE
        self.__change_list = []

    def __str__(self):
        return self.__class__.__name__.lower()

    @property
    def change_list(self):
        # TODO: Проверить, нужно ли делать change_list статиком
        return self.__change_list

    @change_list.setter
    def change_list(self, value):
        self.__change_list.append(value)

    @change_list.deleter
    def change_list(self):
            self.__change_list = []

    def create(self, **kwargs):
        query = 'insert into %s (' % self
        values = '( '
        for k, v in kwargs.items():
            query += '%s, ' % k
            values += "'%s', " % v
        self.change_list.append(query[:-2]+') VALUES '+values[:-2]+');')

    def get(self, id_=None):
        # TODO: Протестировать коректность возврата коммита
        result = self.execute('select * from %s where id = %s; ' % (self, id_))
        if result:
            return result[0]

    def all(self):
        # TODO: Протестировать коректность возврата коммита
        result = self.execute('select * from %s;' % self)
        # TODO: проверить как работает
        if result:
            return result

    def update(self, id_=None, **kwargs):
        if id_:
            query = "UPDATE %s SET id='%s', " % (self, id_)
            for k, v in kwargs.items():
                query += "%s='%s', " % (k, v)
            self.change_list.append(query[:-2]+";")

    def delete(self, id_):
        self.change_list.append("DELETE FROM %s WHERE id='%s'" % (self, id_))

    def commit(self):
        # TODO: Протестировать работу коммита
        return self.execute(self.__change_list)

    def rollback(self):
        del self.change_list

    def execute(self, query_list):
        # TODO: Протестировать коректность возврата
        # TODO: Перенести вывод ошибки в views
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            response = [cursor.execute(i).fetchall() for i in query_list]
            conn.commit()
            conn.close()
            return response[0]
        except sqlite3.Error as e:
            print(e)
            return None

if __name__ == '__main__':
    print('Тест работы serializer.py:\n')
    s = Serializer()
    s.update(id_=10, name='name', date='22-04-2016 20:40', mail='lubchenko@wdc.org.ua')
    s.delete(10)
