import datetime


class BaseModel:
    def __init__(self):
        self.__id = None

    @property
    def id_(self):
        return self.__id

    @id_.setter
    def id_(self, value):
        if not self.__id:
            self.__id = value

    @id_.deleter
    def id_(self):
        self.__id = None


class Item(BaseModel):
    def __init__(self, name='', create_date=datetime.datetime.now(), value=0, to_date=datetime.datetime.now(),
                 prise=0, provider=''):
        self.name = name
        self.create_date = create_date
        self.value = value
        self.to_date = to_date
        self.prise = prise
        self.provider = provider
        super(Item, self).__init__()


class Menu(BaseModel):
    def __init__(self, name='', time=datetime.time(hour=1, minute=0, second=0)):
        self.name = name
        self.time = time
        self.__items = []
        super(Menu, self).__init__()

    @property
    def items(self):
        return self.items

    @items.setter
    def items(self, value=None, value_list=None):
        # TODO: Протестировать проверку типа
        if value & isinstance(value, Item):
            self.__items.append(value)
        elif value_list:
            self.__items = value_list

    @items.deleter
    def items(self, value=None):
        if value in self.__items:
            try:
                self.__items.remove(value)
            except ValueError:
                # TODO: Перенести вывод сообщения в views
                print('Данного значания не существует')
        else:
            self.__items = []


class Staff(BaseModel):
    def __init__(self, full_name='', age=0, gender='', address='', pass_data=''):
        self.full_name = full_name
        self.age = age
        self.gender = gender
        self.address = address
        self.pass_data = pass_data
        self.__func = []
        super(Staff, self).__init__()

    @property
    def func(self):
        return self.__func

    @func.setter
    def func(self, value=None, value_list=None):
        # TODO: Протестировать проверку типа
        if value & isinstance(value, StaffFunc):
            self.__func.append(value)
        elif value_list:
            self.__func = value_list

    @func.deleter
    def func(self, value=None):
        if value in self.__func:
            try:
                self.__func.remove(value)
            except ValueError:
                # TODO: перенести вывод сообщения в views
                print('Данного значания не существует')
        else:
            self.__func = []


class StaffFunc(BaseModel):
    def __init__(self, name='', prise=0, duties='', requirements=''):
        self.name = name
        self.prise = prise
        self.duties = duties
        self.requirements = requirements
        super(StaffFunc, self).__init__()


class Order(BaseModel):
    def __init__(self, date=datetime.datetime.now(), client_full_name='', number='', is_success=False):
        self.date = date
        self.client_full_name = client_full_name
        self.number = number
        self.is_success = is_success
        self.__staff = []
        self.__menus = []
        super(Order, self).__init__()

    @property
    def staff(self):
        return self.__staff

    @staff.setter
    def staff(self, value=None, value_list=None):
        # TODO: Протестировать проверку типа
        if value & isinstance(value, Staff):
            self.__staff.append(value)
        elif value_list:
            self.__staff = value_list

    @staff.deleter
    def staff(self, value=None):
        if value in self.__staff:
            try:
                self.__staff.remove(value)
            except ValueError:
                # TODO: перенести вывод сообщения в views
                print('Данного значания не существует')
        else:
            self.__staff = []

    @property
    def menus(self):
        return self.__menus

    @menus.setter
    def menus(self, value=None, value_list=None):
        # TODO: Протестировать проверку типа
        if value & isinstance(value, Menu):
            self.__menus.append(value)
        elif value_list:
            self.__menus = value_list

    @menus.deleter
    def menus(self, value=None):
        if value in self.__menus:
            try:
                self.__menus.remove(value)
            except ValueError:
                # TODO: перенести вывод сообщения в views
                print('Данного значания не существует')
        else:
            self.__menus = []
