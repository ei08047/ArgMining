import itertools
from nltk import word_tokenize, wordpunct_tokenize
class Word(object):
    newid = itertools.count()
    def __init__(self,word,sentenceId, subjective ):
        self.id = next(Word.newid)
        self.word = word
        self.sentenceId = sentenceId
        self.subjective = subjective

class Annotation(object):
    def __init__(self,annotation):
        stripped_annotation = annotation.split(',')
        self.begin = stripped_annotation[0]
        self.end = stripped_annotation[1]
        self.label = stripped_annotation[2]

    def inRange(self,index):
        if(index in range(self.begin, self.end)):
            return True
        else:
            return False

    def getLabel(self):
        return self.label

class Sentence(object):
    newid = itertools.count()
    def __init__(self,text,claim,annotations):
        self.id = next(Sentence.newid)
        self.text = text.pop()
        self.tokens = word_tokenize(self.text)
        self.no_punct_tokens = [w.lower() for w in self.tokens if w.isalpha()]
        self.claim = claim
        self.annotations = annotations

    def claim_features(self):
        features = {}
        features['text_len'] = len(self.text)
        return features
    def view(self):
        print(self.text , '##' , self.claim, '##', self.annotations)

class Claim_data(object):
    def __init__(self,name,texts,claims,annotations):
        self.name = name
        self.sent_list = []
        for t,c,a in zip(texts,claims,annotations):
            s = Sentence(t,c,a)
            self.sent_list.append(s)
        self.num_claims = len([sent for sent in self.sent_list if sent.claim == 1 ])
        self.num_non_claims = len([sent for sent in self.sent_list if sent.claim == 0])

    def getCommentById(self,id):
        for s in self.sent_list:
            if(s.id == id):
                return s

    def view(self):
        print('Info on:', self.name)
        print('sent_list:', len(self.sent_list))
        print('claims:', self.num_claims, '|| non-claims:', self.num_non_claims)

