class Item(object):
    def __init__(self,value):
        self.value = value
        print('creating item',self,self.value)

class Unit(object):
    def __init__(self,unit):
        self.unit = unit
        print(self.unit)

    def setId(self,id):
        self.id = id

    def view(self):
        print(type(self),self.id)

    def setItems(self,comment,com_stance,argument,arg_stance):
        self.coment= comment
        self.com_stance = com_stance
        self.argument = argument
        self.arg_stance = arg_stance

class Comarg(object):
    units=[]
    def __init__(self,units):
        self.units = units
        print('creating',type(units),self.units)
        for unit in self.units:
            print('tag:',unit.tag,'|| attrib:',unit.attrib,unit.attrib['id'])
            temp = Unit(unit.attrib['id'])
            for element in unit:
                print('tag:',element.tag,'|| attrib:',element.attrib)






