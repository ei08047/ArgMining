import Config
import Corpus
import ComArg
import nltk
import random
import pickle
import os.path
import nltk.metrics


import logging
from gensim import  corpora,models,similarities
from gensim.models import Word2Vec

logging.basicConfig(format='%(asctime)s', level=logging.INFO)

data = {'GM' : 'ComArg', 'UGIP':'ComArg'}

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
config = Config.Config(['GM','UGIP'])
config.run()

if(not os.path.exists("data/ComArg/GM.obj")):
    print('2:reading corpus')
    gm_corpus = Corpus.Corpus(config.data_path, config.getCorpusPath(config.corpusList[0]))
    gm_corpus.readCorpus()
    #gm_corpus.view()
    gm_corpus.view()


    print('3:parsing info')
    gm = ComArg.ComArg(gm_corpus.xml)
    gm.getAllItems()
    all = gm.getAllItems()
    gm.aggregateItems(all)
    gm.create_sents()

    #GM.view()
    print('4:saving to file')
    saveToFile(gm, 'GM')
else:
    print('load GM from file')
    gm=loadFromFile('GM')
    print(len(gm.sents))
    #b = Word2Vec(gm.sents())

if(False):
    if(not os.path.exists("data/ComArg/UGIP.obj")):
        print('2:reading corpus')
        ugip_corpus = Corpus.Corpus(config.data_path, config.getCorpusPath(config.corpusList[1]))
        ugip_corpus.readCorpus()
        #ugip_corpus.view()

        print('3:parsing info')
        UGIP = ComArg.ComArg(ugip_corpus.xml)
        UGIP.getAllItems()
        all = UGIP.getAllItems()
        UGIP.aggregateItems(all)
        #UGIP.view()
        print('4:saving to file')
        saveToFile(UGIP,'UGIP')
    else:
        print('load UGIP from file')
        UGIP=loadFromFile('UGIP')

##res
gm.view()


if(False):
    print('4:building stance classifier')
    comments = gm.comments

    labeled_comments = [(com.id,com.stance) for com in comments]
    random.shuffle(labeled_comments)

    ## gm: 198 comments
    train_comments = labeled_comments[50:]
    devtest_comments = labeled_comments[25:50]
    test_comments = labeled_comments[:25]


    train_set = [(gm.getCommentById(id).test_features(), stance) for (id, stance) in train_comments]
    devtest_set = [(gm.getCommentById(id).test_features(), stance) for (id, stance) in devtest_comments]
    test_set = [(gm.getCommentById(id).test_features(), stance) for (id, stance) in test_comments]

    print('     len train_set::', len(train_set), '|| len test_set::',len(test_set),'|| len devtest_set::',len(devtest_set),)
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print('     accuracy::',nltk.classify.accuracy(classifier, devtest_set))

    #classifier.show_most_informative_features(5)
    print(classifier.most_informative_features(5))

    errors = []
    for(id,stance) in devtest_comments:
        guess = classifier.classify(gm.getCommentById(id).test_features())
        if (guess != stance):
            errors.append((stance,guess,id) )

    for (stance, guess, id) in sorted(errors):
        print('correct={:<8} guess={:<8s} id={:<30}'.format(stance, guess, id))






