import os.path
import sys

class Config:
    def __init__(self,corpusList):
        self.data_path = os.path.expanduser('~/nltk_data')
        print('init config...',file=sys.stdout)
        self.corpusList = corpusList

    def createDataFolder(self):
        os.mkdir(data_path)
        print('created a DataFolder',file=sys.stdout)
    ##check if nltk_data exists

    def getCorpusPath(self,name):
        if(name == 'comArg'):
            return '/comarg/GM.xml'
        elif(name == 'other'):
            return '/path/file.xml'


    def existsDataFolder(self):
        if(os.path.exists(self.data_path)):
            print('data folder exists', file = sys.stdout)
            return True
        print( 'need to create data folder', file= sys.stdout)
        return False

    def existsCorpus(self,name):
        if( os.path.exists(self.data_path + self.getCorpusPath(name))):
            print(name,'exists')
            return True
        return False


    def run(self):
        if(not self.existsDataFolder()):
            self.createDataFolder()
        else:
            for name in self.corpusList:
                if(not self.existsCorpus(name)):
                    print(name, 'not found!', file=sys.stdout)



















