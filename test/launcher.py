import Config
import Corpus
import ComArg
import nltk
import random
import pickle
import os.path

def saveToFile(obj,name):
    filehandler = open("data/ComArg/"+name+".obj", "wb")
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

    print('3:parsing info')
    GM = ComArg.ComArg(gm_corpus.xml)
    GM.getAllItems()
    all = GM.getAllItems()
    GM.aggregateItems(all)
    #GM.view()
    print('4:saving to file')
    saveToFile(GM,'GM')
else:
    print('2:load GM from file')
    GM=loadFromFile('GM')


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

print('4:building stance classifier')
comments = GM.comments

labeled_comments = [(com.id,com.stance) for com in comments]
random.shuffle(labeled_comments)

train_comments = labeled_comments[600:]
devtest_comments = labeled_comments[685:985]
test_comments = labeled_comments[:300]


train_set = [(GM.getCommentById(id).test_features(), stance) for (id, stance) in train_comments]
devtest_set = [(GM.getCommentById(id).test_features(), stance) for (id, stance) in devtest_comments]
test_set = [(GM.getCommentById(id).test_features(), stance) for (id, stance) in test_comments]

print('     len train_set::', len(train_set), '|| len test_set::',len(test_set),'|| len devtest_set::',len(devtest_set),)
classifier = nltk.NaiveBayesClassifier.train(train_set)

print('     accuracy::',nltk.classify.accuracy(classifier, devtest_set))


errors = []
for(id,stance) in devtest_comments:
    guess = classifier.classify(GM.getCommentById(id).test_features())
    if (guess != stance):
        errors.append((stance,guess,id) )

for (stance, guess, id) in sorted(errors):
    print('correct={:<8} guess={:<8s} id={:<30}'.format(stance, guess, id))






