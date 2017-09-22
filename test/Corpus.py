import nltk
from nltk.corpus.reader import XMLCorpusReader

class Corpus:
    def __init__(self,dataPath,corpusPath):
        self.dataPath = dataPath
        self.corpusPath=corpusPath
        self.xmlCorpusReader = XMLCorpusReader(self.dataPath, self.corpusPath)

    def downloadNltk(self):
        print('download nltk corpus')
        nltk.download()


    def readCorpus(self):
        self.xml = self.xmlCorpusReader.xml( self.dataPath + self.corpusPath)
        self.raw = self.xmlCorpusReader.raw(self.dataPath + self.corpusPath)
        self.num_chars = len(self.raw)
        self.num_words = len(self.xmlCorpusReader.words(self.dataPath + self.corpusPath))

    def view(self):
        print('num_chars', self.num_chars , 'num_words', self.num_words )


##sents(): list of (list of str)
##paras(): list of (list of (list of str))
##tagged_words(): list of (str,str) tuple
##tagged_sents(): list of (list of (str,str))
##tagged_paras(): list of (list of (list of (str,str)))
##chunked_sents(): list of (Tree w/ (str,str) leaves)
##parsed_sents(): list of (Tree with str leaves)
##parsed_paras(): list of (list of (Tree with str leaves))