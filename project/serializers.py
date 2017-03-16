import project.settings as settings
import sqlite3

# TODO: продумать многопоточность в екзекьюте


class Serializer:
    def __init__(self):
        self.db_name = settings.DATABASE
        self.__change_list = []

    def __str__(self):
        return self.__class__.__name__.lower()

    @property
    def change_list(self):
        return self.__change_list

    # TODO сделать статиком
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
        query = query[:-2]+') VALUES '+values[:-2]+');'
        self.change_list.append(query)

    def get(self, id_):
        result = self.execute(("select * from %s where id='%s'; " % (self, id_),))
        if result:
            return result[0][0]

    def all(self):
        # TODO: Протестировать коректность возврата коммита
        result = self.execute(('select * from %s;' % self,))
        # TODO: проверить как работает
        if result:
            return result[0]

    def update(self, id_=None, **kwargs):
        if id_:
            query = "UPDATE %s SET " % (self)
            for k, v in kwargs.items():
                query += "%s='%s', " % (k, v)
            self.change_list.append(query[:-2]+" WHERE id='%s';" % id_)

    def delete(self, id_):
        self.change_list.append("DELETE FROM %s WHERE id='%s'" % (self, id_))

    def commit(self):
        # TODO: Протестировать работу коммита
        return self.execute(self.__change_list)

    def rollback(self):
        del self.change_list

    def execute(self, request):
        # TODO: Протестировать коректность возврата
        # TODO: Перенести вывод ошибки в views
        try:
            conn = sqlite3.connect(self.db_name)
            response = [conn.execute(i).fetchall() for i in request]
            conn.commit()
            conn.close()
            return response
        except sqlite3.Error as e:
            print(e)
