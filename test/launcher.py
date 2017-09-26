from test import Config
from test import Corpus
from test import ComArg

config = Config.Config(['comArg'])
config.run()




##TODO:ability to select smaller sub-sets of the document.. maybe unit id and create balanced train and test corpus

corpus = Corpus.Corpus(config.data_path, config.getCorpusPath(config.corpusList[0]))
corpus.readCorpus()
corpus.view()

comArg = ComArg.ComArg(corpus.xml)

comArg.getAllItems()
all = comArg.getAllItems()
comArg.aggregateItems(all)

comArg.view()



