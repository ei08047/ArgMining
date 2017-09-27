from nltk.tokenize import sent_tokenize
import nltk

class hashabledict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))


class Item(object):
    def __init__(self,id,type,stance,text):
        self.id = id
        temp = self.id.split('arg')
        self.comment_id = temp[0]
        self.argument_id= temp[1]
        self.type = type ## comment/argument
        self.stance = stance ## Pro / Con
        self.text = text
        self.tokens = nltk.word_tokenize(self.text)
        self.tokenize_list = sent_tokenize(self.text)
        self.pos_tag = nltk.pos_tag(self.text)

        #sentence segmenter
        self.segmented_sentences = sent_tokenize(self.text)
        #word tokenizer
        self.tokenized_words = [nltk.word_tokenize(sent) for sent in self.segmented_sentences]
        #self.bigrams = nltk.bigrams(self.tokenized_words)
        #part-pf-speech tagger
        self.tagged_sent = [nltk.pos_tag(sent) for sent in self.tokenized_words]

    def preprocess(self):
        #sentence segmenter
        self.segmented_sentences = sent_tokenize(self.text)
        #word tokenizer
        self.tokenized_words = [nltk.word_tokenize(sent) for sent in self.segmented_sentences]
        #part-pf-speech tagger
        self.tagged_sent = [nltk.pos_tag(sent) for sent in self.tokenized_words]

    def calcUnigrams(self):
        unigrams = {}
        for token in self.tokens:
            if token not in unigrams:
                unigrams[token] = 1
            else:
                unigrams[token] += 1
        return hashabledict(unigrams)

    def view(self):
        print(self.id, self.type,self.stance,len(self.tokenize_list))
        ##print('original::',self.text)
        print('token list::', self.tokenize_list)
        ##print('pos tagged original text::',self.pos_tag)
        fdist = nltk.FreqDist(self.pos_tag)
        print(fdist.items())

    def test_features(self):
        features = {}
        features['text_len'] = len(self.text)
        features['unigrams'] =  self.calcUnigrams()
        features['bigrams'] = nltk.bigrams(self.tokens)
        features['trigrams'] = nltk.trigrams(self.tokens)
        features['pos_tags'] = hashabledict(self.pos_tag)
        return features


class Unit(object):
    def __init__(self,id):
        self.id = id
        self.itemList = []

    def getId(self):
        return self.id

    def addItem(self,item):
        self.itemList.append(item)

    def view(self):
        print('Unit:', self.getId())


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
                ##pre process
                TempItem.preprocess()

                tempUnit.addItem(TempItem)
            self.unitList.append(tempUnit)

    def getAllItems(self):
        allItems = []
        for unit in self.unitList:
            for item in unit.itemList:
                allItems.append(item)
        return allItems

    def getCommentById(self,id):
        for com in self.comments:
            if(com.id == id):
                return com

    def aggregateItems(self,allItems):
        #self.comments = [item for item in allItems if item.type == 'comment']

        used_ids= []
        temp_comments = []
        for item in allItems:
            if(item.type == 'comment'):
                if(item.comment_id in used_ids):
                    pass
                else:
                    used_ids.append(item.comment_id)
                    temp_comments.append(item)

        print('len comments:' , len(temp_comments), ' || expected 198 ')
        self.comments = temp_comments


        #self.arguments = [item for item in allItems if item.type == 'argument']
        #self.proComments = [comment for comment in self.comments if comment.stance == 'Pro']
        #self.conComments = [comment for comment in self.comments if comment.stance == 'Con']
        #self.proArguments = [argument for argument in self.arguments if argument.stance == 'Pro']
        #self.conArguments = [argument for argument in self.arguments if argument.stance == 'Con']


    def view(self):
        print('     ComArg info:::','num units:', len(self.unitList))
        print('    Arguments', len(self.arguments),'|| pro',len(self.proArguments), '|| con:',len(self.conArguments) )
        print('    Comments', len(self.comments), '|| pro', len(self.proComments), '|| con:', len(self.conComments))
















