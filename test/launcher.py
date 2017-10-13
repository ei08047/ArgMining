import Config
import Corpus
import ComArg
import random
import pickle
import os.path
import nltk.metrics


import logging

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

gm_identifier='GM'
ugip_identifier = 'UGIP'

print('1:config step..')
config = Config.Config([gm_identifier,ugip_identifier])
config.run()


if(not os.path.exists("data/ComArg/GM.obj")):


    print('2:reading corpus')
    gm_corpus = Corpus.Corpus_xml(config.data_path, config.getCorpusPath(config.corpusList[0]))
    gm_corpus.readCorpus()
    gm_corpus.view()

    print('3:parsing info')
    gm = ComArg.ComArg(gm_corpus.xml)
    gm.getAllItems()
    all = gm.getAllItems()
    gm.aggregateItems(all)
    gm.create_sents()

    print('4:saving to file')
    saveToFile(gm, 'GM')
else:
    print('load GM from file')
    gm=loadFromFile('GM')


if(not os.path.exists("data/ComArg/UGIP.obj")):
    print('2:reading corpus')
    ugip_corpus = Corpus.Corpus_xml(config.data_path, config.getCorpusPath(config.corpusList[1]))
    ugip_corpus.readCorpus()
    ugip_corpus.view()
    print('3:parsing info')
    ugip = ComArg.ComArg(ugip_corpus.xml)
    ugip.getAllItems()
    all = ugip.getAllItems()
    ugip.aggregateItems(all)

    print('4:saving to file')
    saveToFile(ugip, 'UGIP')
else:
    print('load UGIP from file')
    ugip=loadFromFile('UGIP')

gm.view()
ugip.view()

if(False):
    print('4:building stance classifier')
    comments = gm.comments
    labeled_comments = [(com.id,com.stance) for com in comments]
    random.shuffle(labeled_comments)

    train_comments = labeled_comments[50:]
    devtest_comments = labeled_comments[25:50]
    test_comments = labeled_comments[:25]


    train_set = [(gm.getCommentById(id).test_features(), stance) for (id, stance) in train_comments]
    devtest_set = [(gm.getCommentById(id).test_features(), stance) for (id, stance) in devtest_comments]
    test_set = [(gm.getCommentById(id).test_features(), stance) for (id, stance) in test_comments]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print('     accuracy::',nltk.classify.accuracy(classifier, devtest_set))

    print(classifier.most_informative_features(5))

    errors = []
    for(id,stance) in devtest_comments:
        guess = classifier.classify(gm.getCommentById(id).test_features())
        if (guess != stance):
            errors.append((stance,guess,id) )

    for(stance, guess, id) in sorted(errors):
        print('correct={:<8} guess={:<8s} id={:<30}'.format(stance, guess, id))






