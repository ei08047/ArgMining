import nltk



class Item(object):
    def __init__(self,id):
        self.id = id
    def setStanceText(self,comarg,stancetext,text):
        self.comarg = comarg ## comment/argument
        self.stancetext = stancetext ## text / stance
        if(self.stancetext == 'stance'):
            self.stance = text ## raw
        if(self.stancetext == 'text'):
            self.text = text
        ##self.tokens = nltk.word_tokenize(self.text)
        ##self.tagged = nltk.pos_tag(self.tokens)
        ##self.entities = nltk.chunk.ne_chunk(self.tagged)
    def view(self):
        print(self.id, self.comarg, self.stancetext)


    def getText(self):
        return self.text

class Pair(Item):
    def __init__(self,Argument,Comment):
        self.argument = Argument
        self.comment = Comment






class Unit(object):
    itemList = []
    def __init__(self,id):
        self.id = id
    def getId(self):
        return self.id
    def setId(self,id):
        self.id = id
    def addItem(self,item):
        self.itemList.append(item)
    def getComStance(self):
        for item in self.itemList:
            if(item.isComment() and item.isStance()):
                return item
    def getComText(self):
        for item in self.itemList:
            if(item.isComment() and not item.isStance()):
                return item
    def getArgStance(self):
        for item in self.itemList:
            if(item.isStance() and item.isArgument()):
                return item
    def getArgText(self):
        for item in self.itemList:
            if(not item.isStance() and item.isArgument()):
                return item
    def getPair(self):
        return self.itemList


class ComArg(object):
    unitList = []
    proComments = []
    conComments = []
    proArguments = []
    conArguments = []
    def __init__(self,document):
        self.document = document
        for unit in self.document:  ##unit id
            ##print('0::tag:',unit.tag,'|| attrib:',unit.attrib['id'])
            tempUnit = Unit(unit.attrib['id'])
            for item in unit:  ## argument/comment
                ##create new Item
                TempItem = Item(tempUnit.getId())
                ##print('1::tag:',element.tag,'|| attrib:',element.attrib)

                for comArg in item:  ##text / stance
                    #print('2::tag:', comArg.tag, '||Value:', comArg.text)
                    ##item = Item(item.tag, comArg.tag, comArg.text)
                    TempItem.setStanceText(item.tag, comArg.tag, comArg.text)
                    tempUnit.addItem(TempItem)
            self.unitList.append(tempUnit)

        for item in self.unitList[0].getPair():
            print(item.view())


    def test(self):
        print('numUnits',len(self.unitList))


    def divideComments(self):
        if False:
            for unit in self.unitList:
                if(unit.getComStance().getText() == 'Pro'):
                    self.proComments.append(unit.getComText())
                elif(unit.getComStance().getText() == 'Con'):
                    self.conComments.append(unit.getComText())
                if (unit.getArgStance().getText() == 'Pro'):
                    self.proArguments.append(unit.getArgText())
                elif (unit.getArgStance().getText() == 'Con'):
                    self.conArguments.append(unit.getArgText())
        print( 'pro:', len(self.proComments), '|| cons:', len(self.conComments))
        print( 'pro:', len(self.proArguments), '|| cons:', len(self.conArguments))

















