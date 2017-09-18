from nltk.corpus.reader import XMLCorpusReader
from nltk.corpus.reader.xmldocs import XMLCorpusView

from Comarg import Comarg

import os,os.path
corpus_path = os.path.expanduser('~/nltk_data')

if(not os.path.exists(corpus_path)):
    os.mkdir(corpus_path)
    print(os.path.exists(corpus_path))

##nltk.download()
##raw = nltk.data.load('comarg/GM.xml',format='text',verbose=True)

comarg= corpus_path+'/comarg/GM.xml'

#help(XMLCorpusReader)
XMLCorpusReader = XMLCorpusReader(corpus_path,'/comarg/GM.xml')

raw = XMLCorpusReader.raw(comarg)
xml = XMLCorpusReader.xml(comarg)
print(type(raw),type(xml))
print(xml)
words= XMLCorpusReader.words(comarg)
##sentences = gutenberg.sents(fileid)

num_chars = len(raw)
num_words = len(words)
##num_sents = len()
##num_vocab = len(set(w.lower() for w in gutenberg.words(fileid)))
print('num_chars',num_chars ,'|| num_words',num_words)


##sents(): list of (list of str)
##paras(): list of (list of (list of str))
##tagged_words(): list of (str,str) tuple
##tagged_sents(): list of (list of (str,str))
##tagged_paras(): list of (list of (list of (str,str)))
##chunked_sents(): list of (Tree w/ (str,str) leaves)
##parsed_sents(): list of (Tree with str leaves)
##parsed_paras(): list of (list of (Tree with str leaves))

#help(XMLCorpusView)
XMLCorpusView = XMLCorpusView(comarg,'document/unit/comment/text')



unitList = []
itemList = []

print(type(xml),xml.tag)
for unit in xml:
    #print('enter unit',type(unit),unit.tag, unit.attrib)
    unitList.append(unit)
    for item in unit:
        print('enter item',item.tag, item.attrib)
        itemList.append(item)


Comarg = Comarg(unitList)

print('numUnits',len(unitList), 'numItems',len(itemList))



