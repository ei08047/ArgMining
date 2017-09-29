import nltk
from nltk.corpus.reader import XMLCorpusReader,XMLCorpusView
import os
from nltk.tokenize import sent_tokenize,word_tokenize,wordpunct_tokenize
from nltk.corpus import brown
from nltk.corpus.reader.util import ConcatenatedCorpusView
from gensim.models import Word2Vec

import xml.etree.ElementTree




class Corpus:
    def __init__(self,dataPath,corpusPath):
        self.dataPath = dataPath
        self.corpusPath=corpusPath
        path = str(self.dataPath + '/' + self.corpusPath)
        print('exists ', os.path.exists(path))

        self.xmlCorpusReader = XMLCorpusReader(path, self.corpusPath)

        self.xmlCorpusView = XMLCorpusView(path ,'.*/text')

        self.ccv = ConcatenatedCorpusView(self.xmlCorpusView)
        b = Word2Vec(self.ccv)

        #b.most_similar('god')


        print(type(self.xmlCorpusView), type(brown.sents()), type(self.ccv))





    def readCorpus(self):
        self.xml = self.xmlCorpusReader.xml( self.dataPath + self.corpusPath)
        self.raw = self.xmlCorpusReader.raw(self.dataPath + self.corpusPath)
        self.num_chars = len(self.raw)
        self.words = self.xmlCorpusReader.words(self.dataPath + self.corpusPath)
        self.num_words = len(self.words)

    def view(self):
        print('raw',type(self.raw), 'xml', type(self.xml), 'xml corpus reader:',type(self.xmlCorpusReader))
        print('num_chars', self.num_chars , 'num_words', self.num_words,'lexical_diversity', self.lexical_diversity(self.words) )

    def lexical_diversity(self,text):
        print('     set', len(set(text)), 'all', len(text))
        return len(set(text)) / len(text)






##sents(): list of (list of str)
##paras(): list of (list of (list of str))
##tagged_words(): list of (str,str) tuple
##tagged_sents(): list of (list of (str,str))
##tagged_paras(): list of (list of (list of (str,str)))
##chunked_sents(): list of (Tree w/ (str,str) leaves)
##parsed_sents(): list of (Tree with str leaves)
##parsed_paras(): list of (list of (Tree with str leaves))