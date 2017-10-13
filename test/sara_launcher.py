import Config
import Corpus
from Claim import Claim_data, Annotation
import random
import pickle
import nltk.metrics

import logging
logging.basicConfig(format='%(asctime)s', level=logging.INFO)

data = {'claim-annotations':'livejournal' ,'claim-annotations':'wikipedia'}

def saveToFile(obj,name):
    if(name=='GM'):
        filehandler = open("data/ComArg/GM.obj", "wb")
    elif(name=='UGIP'):
        filehandler = open("data/ComArg/UGIP.obj", "wb")
    pickle.dump(obj, filehandler)
    filehandler.close()

def loadFromFile(name):
    file = open("data/ComArg/"+name+".obj", 'rb')
    object_file = pickle.load(file)
    return object_file


print('1:config step..')
config = Config.Config(['livejournal','wikipedia'])
config.run()

###############################################################################

print('reading wikipedia corpus')
wikipedia_corpus = Corpus.Corpus_csv(config.data_path, config.getCorpusPath(config.corpusList[1]), config.corpusList[1])
wikipedia_corpus.view()
t = wikipedia_corpus.read_text()
c = wikipedia_corpus.read_claim()
a = wikipedia_corpus.read_annotation()

wikipedia = Claim_data('wikipedia',t,c,a)
wikipedia.view()

print('reading live_journal corpus')
live_journal_corpus = Corpus.Corpus_csv(config.data_path, config.getCorpusPath(config.corpusList[0]), config.corpusList[0])
live_journal_corpus.view()
t = live_journal_corpus.read_text()
c = live_journal_corpus.read_claim()
a = live_journal_corpus.read_annotation()

live_journal = Claim_data('livejournal',t,c,a)
live_journal.view()


if(False):
    print('building claim detection classifier')

    comments = live_journal.sent_list
    labeled_comments = [(com.id, com.claim) for com in comments]
    random.shuffle(labeled_comments)

    train_comments = labeled_comments[500:]
    devtest_comments = labeled_comments[:250]
    test_comments = labeled_comments[250:500]

    train_set = [(live_journal.getCommentById(id).claim_features(), claim) for (id, claim) in train_comments]
    devtest_set = [(live_journal.getCommentById(id).claim_features(), claim) for (id, claim) in devtest_comments]
    test_set = [(live_journal.getCommentById(id).claim_features(), claim) for (id, claim) in test_comments]

    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print('     accuracy::', nltk.classify.accuracy(classifier, devtest_set))

    print('building a objective/subjective classifier')

    all_words = []

    for sent in live_journal.sent_list:
        print('num tokens', len(sent.tokens) ,'annotation', sent.annotations)
        print(sent.tokens)
        for index,word in enumerate(sent.tokens):
            print('index::',index , '||| word:::::',word, '||| sentence Id::', sent.id )
            a = Annotation()












