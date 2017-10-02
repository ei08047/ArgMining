import nltk
import csv
from nltk.corpus.reader import XMLCorpusReader,XMLCorpusView
from nltk.corpus.reader import PlaintextCorpusReader
import os
from nltk.tokenize import sent_tokenize,word_tokenize,wordpunct_tokenize
from nltk.corpus import brown
from nltk.corpus.reader.util import ConcatenatedCorpusView


import xml.etree.ElementTree

class Corpus_csv:
    def __init__(self,dataPath,corpusPath,name):
        self.dataPath = dataPath
        self.corpusPath=corpusPath
        self.path_text = str(self.dataPath + '/' + self.corpusPath + '/'+ name+ '_text.csv')
        self.path_claim = str(self.dataPath + '/' + self.corpusPath + '/'+ name + '_claim.csv')
        self.path_annotation = str(self.dataPath + '/' + self.corpusPath + '/'+ name + '_annotation.csv')

    def read_text(self):
        text_list = []
        print('entered test')
        text_file = open(self.path_text, "r", encoding='utf8')
        with text_file as infile:
            rows = csv.reader(infile, delimiter='\n')
            for row in rows:
                row = row[:len(row)-1]
                text_list.append(row)
        return text_list

    def read_claim(self):
        claim =0
        claim_list = []
        claim_file = open(self.path_claim, "r", encoding='utf8')
        with claim_file as infile:
            rows = csv.reader(infile, delimiter='\n')
            for row in rows :
                if(row[0] == 'N'):
                    claim = 0
                else:
                    claim = 1
                claim_list.append(claim)
        return claim_list

    def read_annotation(self):
        annotation_list = []
        annotation_file = open(self.path_annotation,"r", encoding='utf8')
        with annotation_file as f:
            data = f.read()
        new_data = data.replace('"', '')
        for row in csv.reader(new_data.splitlines(), delimiter='|'):
            row = row[:len(row)-1]
            annotation_list.append(row)
        return annotation_list













class Corpus:
    def __init__(self,dataPath,corpusPath):
        self.dataPath = dataPath
        self.corpusPath=corpusPath
        path = str(self.dataPath + '/' + self.corpusPath)
        print('exists ', os.path.exists(path))

        self.xmlCorpusReader = XMLCorpusReader(path, self.corpusPath)

        self.xmlCorpusView = XMLCorpusView(path ,'.*/text')

        self.ccv = ConcatenatedCorpusView(self.xmlCorpusView)
        ##b = Word2Vec(self.ccv)

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