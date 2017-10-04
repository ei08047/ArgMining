import logging
import os.path
import sys

class Config:
    def __init__(self,corpusList):
        self.data_path = os.path.expanduser('~/nltk_data/corpora')
        self.corpusList = corpusList
    def createDataFolder(self):
        os.mkdir(self.data_path)
        print(' created a DataFolder',file=sys.stdout)
    def getCorpusPath(self,name):
        if(name == 'GM'):
            return '/comarg/GM.xml'
        if(name == 'UGIP'):
            return '/comarg/UGIP.xml'
        if(name == 'livejournal' or name == 'wikipedia'):
            return '/sara/claim-annotations/train'
        if(name == 'arguing_corpus'):
            return '/arguing_corpus'
        elif(name):
            return '/path/file.xml'


    def existsDataFolder(self):
        if(os.path.exists(self.data_path)):
            print('data_path::',self.data_path, '     nltk_data folder already exists', file = sys.stdout)
            return True
        print( '        need to create data folder', file= sys.stdout)
        return False

    def existsCorpus(self,name):
        print('name:',name ,'|| corpus list',self.corpusList)
        path_to_corpus = self.data_path + self.getCorpusPath(name)
        print('path_to_corpus',path_to_corpus)
        if( os.path.exists(self.data_path + self.getCorpusPath(name))):
            print(self.getCorpusPath(name) ,name,'exists')
            readme = '/readme.txt'
            path_to_read_me = self.data_path + self.getCorpusPath(name) + readme
            print('has readMe?',os.path.exists(path_to_read_me))
            return True
        return False
    def run(self):
        if(not self.existsDataFolder()):
            self.createDataFolder()
        else:
            for name in self.corpusList:
                print('name:::',name)
                if(not self.existsCorpus(name)):
                    print('     ',name, 'corpus not found!')
                else:
                    print(name, 'exists')