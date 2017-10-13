from Config import Config
from nltk.corpus.reader import PlaintextCorpusReader,XMLCorpusReader,XMLCorpusView
import os,csv

#http://mpqa.cs.pitt.edu/corpora/mpqa_corpus/mpqa_corpus_3_0/mpqa_3_0_readme.txt
class Agent():
    def __init__(self,id=None,nested_source=None,agent_uncertain=None):
        self.id=id
        self.nested_source = nested_source
        self.agent_uncertain=agent_uncertain

#expressive-subjectivity annotation
class SE():
    def __init__(self,id,nested_source,polarity,targetFrame,nested_source_uncertain=None,intensity=None  ):
        self.id = id
        self.nested_source=nested_source
        self.polarity= polarity
        self.targetFrame = targetFrame
        self.nested_source_uncertain= nested_source_uncertain
        self.intensity = intensity


# direct-subjective annotation
#Marks direct mentions of private states and speech events (spoken or written) expressing private states.
class DS:
    def __init__(self,id, nested_source,atitude_link,annotation_uncertain=None, implicit=None, subjective_uncertain=None, intensity =None, expression_intensity=None, polarity=None,insubstancial=None):
        self.id=id
# objective-speech-event annotation
# Marks speech events that do not express private states.
class OSE:
    def __init__(self,id,nested_source,targetFrame,annotation_uncertain=None, implicit='None', objective_uncertain=None, insubstantial = None  ):
        self.id=id

        #Marks the attitudes that compose the expressed private states.
class Attitude:
    def __init__(self,id,attitude_type,targetFrame,attitude_uncertain=None,inferred=None ):
        self.id=id


class Meta():
    topic = 'meta_topic'
    title = 'meta_title'
    def __init__(self,topic,title):
        self.topic=topic
        self.title = title


class Gate():
    root='GateDocument'
    inner_root = 'TextWithNodes'
    leaf = 'Node'


#Each attribute is an attribute_name="attribute_value" pair.
#An annotation may have any number of attributes, including 0
#attributes.  Multiple attributes for an annotation are
#separated by single spaces, and they may be listed in any
#order.  The attributes that an annotation may have depends
#on the type of annotation.
#example
##id span	    anno_type attributes
##58 730,740  agent     nested-source="w,chinarep"
class Man():
    def __init__(self, id,span,anno_type,attributes):
        self.id=id
        self.span=span
        self.anno_type=anno_type
        self.attributes = attributes





class Document:
    def __init__(self,parent,docleaf):
        self.parent = parent
        self.docleaf = docleaf
    def get_doc_leaf(self):
        return self.docleaf
    def getPath(self):
        return str(self.parent + '/' + self.docleaf)

class MPQA:
    name = 'mpqa'
    data_path = '/database.mpqa.3.0'
    docs = 'docs'
    meta_anns = 'meta_anns'
    man_anns = 'man_anns'
    doclist='doclist'

    def __init__(self,dataPath,corpusPath):
        self.dataPath = dataPath
        self.corpusPath=corpusPath
        self.path = str(self.dataPath + self.corpusPath)


        self.docs = PlaintextCorpusReader(self.path, MPQA.docs+"/\d{8}.*" )
        self.man_anns = PlaintextCorpusReader(self.path, MPQA.man_anns+"/\d{8}.*")

        #parse doc list
        temp=[]
        doc_list_path = str(self.path+'/doclist' )
        text_file = open(doc_list_path, "r", encoding='utf8')
        with text_file as infile:
            rows = csv.reader(infile, delimiter='\n')
            for row in rows:
                temp.append(row.pop())
        self.doc_list = [Document(doc.split('/')[0],doc.split('/')[1]) for doc in temp]

        self.parse_meta()
        ##self.parse_anns()








    def parse_meta(self):
        for meta_doc in self.doc_list:
            doc_path = meta_doc.getPath()
            full_path = self.getFullPath(MPQA.meta_anns, doc_path)
            if(not os.path.exists(full_path)):
                print('full_path: ', full_path, os.path.exists(full_path))
            else:
                try:
                    text_file = open(full_path, "r", encoding='utf8')
                    with text_file as infile:
                        rows = csv.reader(infile, delimiter='\t')
                        for row in rows:
                            encoded_row = [x.encode('utf-8').decode() for x in row]
                            if ('meta_title' in encoded_row):
                                print(encoded_row[4])
                except UnicodeDecodeError:
                    print('?????')

            #for meta in self.meta_anns:
             #   m = Meta(meta)

    def parse_anns(self):
        ##man_anns
        for anns_doc in self.doc_list:
            doc_path = anns_doc.getPath()
            leaf= anns_doc.get_doc_leaf()
            alt1 = str('non_fbis/'+ leaf)
            alt2 = str('temp_fbis/' + leaf)
            full_path = self.getFullPath(MPQA.man_anns, doc_path)
            if(not os.path.exists(full_path)):
                full_path = self.getFullPath(MPQA.man_anns, alt1)
                if(not os.path.exists(full_path)):
                    full_path = self.getFullPath(MPQA.man_anns, alt2)
                    if (not os.path.exists(full_path)):
                        pass
            else:
                print(full_path,'  has annotaion')

    def parse_docs(self):
        ##docs
        files = self.docs.fileids()
        temp=[]
        for f in files:
            d = f.split('/')
            parent = d[1]
            docleaf = d[2]
            doc = Document(parent,docleaf)
            temp.append(doc)
        self.docs = temp



    def getFullPath(self,doc_type,doc_path):
        return str(self.path + '/' + doc_type + '/' + doc_path)

    def view(self):

        print('docs:',len(self.docs),'##meta_anns: ' ,len(self.meta_anns),'##man_anns: ' ,len(self.man_anns))



    def list_files(self,corpus):
        files = corpus.fileids()
        print('listing files: ')
        for f in files:
            print(f)





print('1:config step..')
config = Config([MPQA.name])
config.run()

mpqa = MPQA(config.data_path, config.getCorpusPath(config.corpusList[0]))





