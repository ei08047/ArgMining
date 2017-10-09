import Config
from Corpus import Corpus


doclist_healthcare_train_anti='doclist_healthcare_train_anti.txt'
doclist_healthcare_train_pro='doclist_healthcare_train_pro.txt'
anti_list = []
pro_list = []
class Text(object):
    def __init__(self, name, raw ):
        self.name=name
        self.raw = raw

class ArguingCorpus(object):
    def __init__(self,path):
        self.path = path



print('1:config step..')
config = Config.Config(['arguing_corpus'])
config.run()

print('reading arguing_corpus corpus')
arguing_corpus = Corpus(config.data_path, config.getCorpusPath(config.corpusList[0]), '/training')
arguing_corpus.read_me()

anti_list = arguing_corpus.parse_doc_list('anti')
pro_list = arguing_corpus.parse_doc_list('pro')

print('num pro:',len(pro_list), 'num anti:', len(pro_list))








#config.run()
#a = ArguingCorpus(config)
#a.read()