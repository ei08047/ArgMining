import Config
import Corpus
import ComArg

config = Config.Config(['comArg'])
config.run()

<<<<<<< HEAD

=======
##TODO:ability to select smaller sub-sets of the document.. maybe unit id and create balanced train and test corpus
>>>>>>> 43a2baec1da877126ce2d62d633a83f171175370
corpus = Corpus.Corpus(config.data_path, config.getCorpusPath(config.corpusList[0]))
corpus.readCorpus()
corpus.view()

comArg = ComArg.ComArg(corpus.xml)


##comArg.generatePairs()
<<<<<<< HEAD
comArg.getAllItems()
=======
all = comArg.getAllItems()
comArg.aggregateItems(all)
>>>>>>> 43a2baec1da877126ce2d62d633a83f171175370
comArg.view()



