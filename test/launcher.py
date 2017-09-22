import Config
import Corpus
import ComArg

config = Config.Config(['comArg'])
config.run()


corpus = Corpus.Corpus(config.data_path, config.getCorpusPath(config.corpusList[0]))
corpus.readCorpus()
corpus.view()

comArg = ComArg.ComArg(corpus.xml)


##comArg.generatePairs()
comArg.getAllItems()
comArg.view()



