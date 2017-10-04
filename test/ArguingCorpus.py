from nltk.corpus.reader import PlaintextCorpusReader
from nltk.corpus import reader
import os
import Config
from Corpus import Corpus


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
arguing_corpus.read()





#config.run()
#a = ArguingCorpus(config)
#a.read()