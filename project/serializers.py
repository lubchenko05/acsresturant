import project.settings as settings
import sqlite3
from project import models


class Serializer:
    DB = settings.DATABASE

    def __init__(self):
        self.__change_list = []

    def __str__(self):
        return self.__class__.__name__.lower()

    @classmethod
    def get(cls, id_):
        result = cls.execute(("PRAGMA table_info(%s);" % cls.__name__.lower(),
                              "select * from %s where id='%s';" % (cls.__name__.lower(), id_)))
        if result[0][1] and result[1]:
            my_cls = cls(id_)
            my_cls.__dict__ = dict(zip([_i[1] for _i in result[0]], [_i for _i in result[1][0]]))
            return my_cls

    @classmethod
    def all(cls):
        class_model = cls(-1)
        result = class_model.execute(("PRAGMA table_info(%s);" % cls.__name__.lower(),
                                      "select * from %s;" % (cls.__name__.lower())))
        if result[0][1] and result[1]:
            cls_list = []
            for _i in result[1]:
                my_cls = cls(_i[0])
                my_cls.__dict__ = dict(list(zip([_i[1] for _i in result[0]], _i)))
                cls_list.append(my_cls)
            return cls_list

    @classmethod
    def create(cls, **kwargs):
        # TODO: Оптимизировать на предмет SQL Запросов
        query = 'insert into %s (' % cls.__name__.lower()
        values = '( '
        for k, v in kwargs.items():
            query += '%s, ' % k
            values += "'%s', " % v
        query = query[:-2] + ') VALUES ' + values[:-2] + ');'
        result = cls.execute((query, 'select seq from sqlite_sequence where name="%s"' % cls.__name__.lower()))
        return cls.get(result[1][0][0])

    def save(self):
        if self.id:
            query = "UPDATE %s SET " % self
            for k, v in self.__dict__.items():
                query += "%s='%s', " % (k, v)
                self.__dict__[k] = v
            self.execute((query[:-2] + " WHERE id='%s';" % self.id,))

    def delete(self):
        if self.get(self.id):
            self.execute(('DELETE FROM %s where id="%s"' % (self, self.id),))
        del self

    @classmethod
    def execute(cls, request):
        # TODO: Перенести вывод ошибки в views
        try:
            conn = sqlite3.connect(cls.DB)
            response = [conn.execute(i).fetchall() for i in request]
            conn.commit()
            conn.close()
            return response
        except sqlite3.Error as e:
            print(e)

if __name__ == '__main__':
    item1 = models.Item.create(name='name', value="200")
    print(item1.__dict__)
    item1.name = 'new_name'
    item1.save()
    item2 = models.Item.get(item1.id)
    print(item2.__dict__)
    item1.delete()
    item2.delete()
