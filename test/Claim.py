import itertools
class Sentence(object):
    newid = itertools.count()
    def __init__(self,text,claim,annotations):
        self.id = next(Sentence.newid)
        self.text = text
        self.claim = claim
        self.annotations = annotations

    def claim_features(self):
        features = {}
        features['text_len'] = len(self.text)
        return features

    def view(self):
        print(self.text , '##' , self.claim, '##', self.annotations)



class Claim_data(object):
    def __init__(self,texts,claims,annotations):
        self.sent_list = []
        for t,c,a in zip(texts,claims,annotations):
            s = Sentence(t,c,a)
            self.sent_list.append(s)

    def getCommentById(self,id):
        for s in self.sent_list:
            if(s.id == id):
                return s



