from nltk.corpus.reader import XMLCorpusReader
from nltk.corpus.reader.xmldocs import XMLCorpusView

from ComArg import ComArg




##sentences = gutenberg.sents(fileid)

num_chars = len(raw)
num_words = len(words)
##num_sents = len()
##num_vocab = len(set(w.lower() for w in gutenberg.words(fileid)))
print('num_chars',num_chars ,'|| num_words',num_words)




#help(XMLCorpusView)
XMLCorpusView = XMLCorpusView(comarg,'document/unit/comment/text')



print(type(xml),xml.tag)

Comarg = ComArg(xml)
Comarg.test()
##Comarg.divideComments()









