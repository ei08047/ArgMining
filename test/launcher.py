import Config
import Corpus
import ComArg
import nltk
import random

print('1:config step..')
config = Config.Config(['comArg'])
config.run()

print('2:reading corpus')
corpus = Corpus.Corpus(config.data_path, config.getCorpusPath(config.corpusList[0]))
corpus.readCorpus()
corpus.view()

print('3:parsing info')
comArg = ComArg.ComArg(corpus.xml)
comArg.getAllItems()
all = comArg.getAllItems()
comArg.aggregateItems(all)
comArg.view()

print('4:building stance classifier')
comments = comArg.comments

labeled_comments = [(com.id,com.stance) for com in comments]
random.shuffle(labeled_comments)

train_comments = labeled_comments[600:]
devtest_comments = labeled_comments[685:985]
test_comments = labeled_comments[:300]


featuresets = [ (comArg.getCommentById(id).test_features(), stance) for (id,stance) in labeled_comments]

train_set = [ (comArg.getCommentById(id).test_features(), stance) for (id,stance) in train_comments]
devtest_set = [ (comArg.getCommentById(id).test_features(), stance) for (id,stance) in devtest_comments]
test_set = [ (comArg.getCommentById(id).test_features(), stance) for (id,stance) in test_comments]

print('     len train_set::', len(train_set), '|| len test_set::',len(test_set),'|| len devtest_set::',len(devtest_set),)
classifier = nltk.NaiveBayesClassifier.train(train_set)


print('     accuracy::',nltk.classify.accuracy(classifier, devtest_set))


errors = []
for(id,stance) in devtest_comments:
    guess = classifier.classify(comArg.getCommentById(id).test_features())
    if (guess != stance):
        errors.append((stance,guess,id) )

for (stance, guess, id) in sorted(errors):
    print('correct={:<8} guess={:<8s} id={:<30}'.format(stance, guess, id))






