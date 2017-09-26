from nltk.tokenize import sent_tokenize
import nltk


class Item(object):
    def __init__(self,id,type,stance,text):
        self.id = id
        self.type = type ## comment/argument
        self.stance = stance ## Pro / Con
        self.text = text
    def view(self):
        print(self.id, self.type,self.stance, self.text)

        self.tokenize_list = sent_tokenize(self.text) ##this only makes sence IF
        self.pos_tag = nltk.pos_tag(self.text)
        self.view()
    def view(self):
        print(self.id, self.type,self.stance,len(self.tokenize_list))
        ##print('original::',self.text)
        print('token list::', self.tokenize_list)
        ##print('pos tagged original text::',self.pos_tag)
        fdist = nltk.FreqDist(self.pos_tag)
        print(fdist.items())

class Unit(object):
    def __init__(self,id):
        self.id = id
        self.itemList = []
    def getId(self):
        return self.id
    def addItem(self,item):
        self.itemList.append(item)
    def getArgItem(self):
        for i in self.itemList:
            if i.type == 'argument':
                return i
                break
    def getComItem(self):
        for i in self.itemList:
            if i.type == 'comment':
                return i
                break
    def view(self):
        print('Unit:', self.getId(),'of',len(self.itemList))

class ComArg(object):
    def __init__(self,document):
        self.unitList = []
        self.document = document
        for unit in self.document:  ##unit id
            ##print('0::tag:',unit.tag,'|| attrib:',unit.attrib['id'])
            tempUnit = Unit(unit.attrib['id'])
            for item in unit:  ## argument/comment
                if item.tag == 'label':
                    continue
                textNode = item.find('text')
                stanceNode = item.find('stance')
                TempItem = Item(tempUnit.getId(), item.tag, stanceNode.text, textNode.text)
                tempUnit.addItem(TempItem)
            self.unitList.append(tempUnit)
        print(type(self.unitList), len(self.unitList), 'units')
    def getAllItems(self):
        allItems = []
        for unit in self.unitList:
            for item in unit.itemList:
                allItems.append(item)
        print('all items::',len(allItems))
        print('all items::',len(allItems))
        return allItems
    def aggregateItems(self,allItems):
        self.comments = [item for item in allItems if item.type == 'comment']
        self.arguments = [item for item in allItems if item.type == 'argument']
        self.proComments = [comment for comment in self.comments if comment.stance == 'Pro']
        self.conComments = [comment for comment in self.comments if comment.stance == 'Con']
        self.proArguments = [argument for argument in self.arguments if argument.stance == 'Pro']
        self.conArguments = [argument for argument in self.arguments if argument.stance == 'Con']
    def view(self):
        print('ComArg info:::')
        print('num units:', len(self.unitList))
        print('num pro || con || arguments' ,len(self.proArguments), len(self.conArguments), len(self.arguments)  )
        print('num pro || con || comments' ,len(self.proComments), len(self.conComments), len(self.comments) )
















