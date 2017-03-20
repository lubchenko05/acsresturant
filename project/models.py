from project.serializers import BaseModel


class Item(BaseModel):
    def __init__(self, *args):
        super(Item, self).__init__()


class Menu(BaseModel):
    def __init__(self, *args):
        super(Menu, self).__init__()


class Staff(BaseModel):
    def __init__(self, *args):
        super(Staff, self).__init__()


class StaffFunc(BaseModel):
    def __init__(self, *args):
        super(StaffFunc, self).__init__()


class Orders(BaseModel):
    def __init__(self, *args):
        super(Orders, self).__init__()


class Order_To_Menu(BaseModel):
    def __init__(self, *args):
        super(Order_To_Menu, self).__init__()


class Menu_To_Item(BaseModel):
    def __init__(self, *args):
        super(Menu_To_Item, self).__init__()