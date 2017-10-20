from Config import Config
from nltk.corpus.reader import PlaintextCorpusReader
import os, csv
import re


# Each attribute is an attribute_name="attribute_value" pair.
# An annotation may have any number of attributes, including 0
# attributes.  Multiple attributes for an annotation are
# separated by single spaces, and they may be listed in any
# order.  The attributes that an annotation may have depends
# on the type of annotation.
# example
##id span	    anno_type attributes
##58 730,740  agent     nested-source="w,chinarep"
class Annotation():
    def __init__(self, id, span):
        self.id = id
        self.span = span

# http://mpqa.cs.pitt.edu/corpora/mpqa_corpus/mpqa_corpus_3_0/mpqa_3_0_readme.txt
class Agent(Annotation):
    def __init__(self, annotation_id, span, id=None, nested_source=None, agent_uncertain=None):
        #print('called Agent constructor')
        Annotation.__init__(self,annotation_id,span)
        self.id = id
        self.nested_source = nested_source
        self.agent_uncertain = agent_uncertain

# expressive-subjectivity annotation
# es_uncertain
class SE(Annotation):
    def __init__(self, annotation_id, span, id, nested_source, polarity, targetFrame_link,es_uncertain=None, nested_source_uncertain=None, intensity=None):
        #print('called SE constructor')
        Annotation.__init__(self,annotation_id,span)
        self.id = id
        self.nested_source = nested_source
        self.polarity = polarity
        self.targetFrame_link = targetFrame_link
        self.nested_source_uncertain = nested_source_uncertain
        self.intensity = intensity

class TargetFrame(Annotation):
    def __init__(self,annotation_id,span,id,sTarget_link,newETarget_link):
        #print('called TargetFrame constructor')
        Annotation.__init__(self,annotation_id,span)
        self.id = id
        self.sTarget_link = sTarget_link
        self.newETarget_link = newETarget_link

class ETarget(Annotation):
    def __init__(self, annotation_id, span, id ,type, isNegated,isReferredInSpan):
        #print('called ETarget constructor')
        Annotation.__init__(self, annotation_id, span)
        self.id = id
        self.type= type
        self.isNegated = isNegated
        self.isReferredInSpan = isReferredInSpan

class STarget(Annotation):
        def __init__(self, annotation_id, span, id , target_uncertain, eTarget_link):
            #print('called STarget constructor')
            Annotation.__init__(self, annotation_id, span)
            self.id = id
            self.target_uncertain = target_uncertain
            self.eTarget_link = eTarget_link

# direct-subjective annotation
# Marks direct mentions of private states and speech events (spoken or written) expressing private states.
class DS(Annotation):
    def __init__(self,annotation_id,span , id, nested_source, atitude_link, annotation_uncertain=None, implicit=None,
                 subjective_uncertain=None, intensity=None, expression_intensity=None, polarity=None,
                 insubstancial=None):
        print('called DS constructor')
        Annotation.__init__(self,annotation_id,span)
        self.id = id
        self.nested_source = nested_source
        self.atitude_link = atitude_link
        self.annotation_uncertain = annotation_uncertain
        self.implicit = implicit
        self.subjective_uncertain = subjective_uncertain
        self.intensity = intensity
        self.expression_intensity = expression_intensity
        self.polarity = polarity
        self.insubstancial= insubstancial

class Sentence(Annotation):
    def __init__(self,annotation_id,span):
        #print('called Sentence constructor')
        Annotation.__init__(self,annotation_id,span)

# objective-speech-event annotation
# Marks speech events that do not express private states.
class OSE:
    def __init__(self,annotation_id, span, id, nested_source, targetFrame, annotation_uncertain=None, implicit=None,
                 objective_uncertain=None, insubstantial=None):
        #print('called objective-speech-event constructor')
        Annotation.__init__(self,annotation_id,span)
        self.id = id
        self.neste_source = nested_source
        self.targetFrame = targetFrame
        self.annotation_uncertain = annotation_uncertain
        self.implicit = implicit
        self.objective_uncertain = objective_uncertain
        self.insubstantial = insubstantial

# Marks the attitudes that compose the expressed private states.

##Why intensity is here???
## Why negative_intensity is here ??
class Attitude(Annotation):
    def __init__(self,annotation_id,span ,id, attitude_type, targetFrame_link,intensity=None,negative_intensity=None,attitude_uncertain=None, inferred=None):
        #print('called Attitude constructor')
        Annotation.__init__(self,annotation_id,span)
        self.id = id
        self.attitude_type = attitude_type
        self.targetFrame_link=targetFrame_link
        self.intensity = intensity
        self.attitude_uncertain = attitude_uncertain
        self.inferred = inferred

class Meta():
    topic = 'meta_topic'
    title = 'meta_title'
    def __init__(self, topic, title):
        self.topic = topic
        self.title = title

class Document:
    def __init__(self, parent, docleaf):
        self.parent = parent
        self.docleaf = docleaf
        self.annotation_list = []
    def get_doc_leaf(self):
        return self.docleaf
    def getPath(self):
        return str(self.parent + '/' + self.docleaf)
    def addAnnotation(self,anno ):
        self.annotation_list.append(anno)

    def view(self):
        print('parent:',self.parent, '##doc_leaf:', self.docleaf , '##num_anno:', len(self.annotation_list))
        print('num attitudes:',len([att for att in self.annotation_list if type(att).__name__=='Attitude']))
        print('num sub: ', len([ds for ds in self.annotation_list if type(ds).__name__ == 'DS']))
        print('num obj: ', len([ose for ose in self.annotation_list if type(ose).__name__ == 'OSE']))
        print('num expressive-subjectivity: ', len([es for es in self.annotation_list if type(es).__name__ == 'SE']))

class MPQA:
    name = 'mpqa'
    data_path = '/database.mpqa.3.0'
    docs = 'docs'
    meta_anns = 'meta_anns'
    man_anns = 'man_anns'
    doclist = 'doclist'

    def __init__(self, dataPath, corpusPath):

        self.dataPath = dataPath
        self.corpusPath = corpusPath
        self.path = str(self.dataPath + self.corpusPath)

        # parse doc list
        self.doc_list = self.parse_doc_list()

        #parse meta data
        for meta_doc in self.doc_list:
            self.parse_meta(meta_doc)

        #parse annotations
        for anns_doc in self.doc_list:
            self.parse_anns(anns_doc)

        for doc in self.doc_list:
            doc.view()

    def parse_doc_list(self):
        temp = []
        doc_list_path = str(self.path + '/doclist')
        text_file = open(doc_list_path, "r", encoding='utf8')
        with text_file as infile:
            rows = csv.reader(infile, delimiter='\n')
            for row in rows:
                temp.append(row.pop())
        return [Document(doc.split('/')[0], doc.split('/')[1]) for doc in temp]

    def parse_text(self):
        print('parsing text')

    def parse_meta(self, doc):
        doc_path = doc.getPath()
        full_path = self.getFullPath(MPQA.meta_anns, doc_path)
        if (not os.path.exists(full_path)):
            print('full_path: ', full_path, os.path.exists(full_path))
        else:
            try:
                text_file = open(full_path, "r", encoding='utf8')
                with text_file as infile:
                    rows = csv.reader(infile, delimiter='\t')
                    for row in rows:
                        encoded_row = [x.encode('utf-8').decode() for x in row]
                        if ('meta_title' in encoded_row):
                            meta_title =encoded_row[4]
            except UnicodeDecodeError:
                print('?????')

    def parse_anns(self, doc):
        comment_pattern = re.compile("^#")
        doc_path = doc.getPath()
        full_path = self.getFullPath(MPQA.man_anns, doc_path)
        path_to_annotation = str(full_path + '/gateman.mpqa.lre.3.0')
        if (not os.path.exists(path_to_annotation)):
            print('???')
        else:
            #print('full_path: ',full_path)
            annotation_file = open(path_to_annotation, "r", encoding='utf-8')
            with annotation_file as infile:
                rows = csv.reader(infile, delimiter='\n')
                for row in rows:
                    line = row.pop()
                    if(comment_pattern.match(line)):
                        pass
                    else:
                        doc.addAnnotation(self.parse_annotation_line(line))

    def parse_annotation_line(self,line):
        dict = {'attitude': Attitude , 'direct-subjective':DS , 'agent':Agent, 'expressive-subjectivity':SE,'objective-speech-event':OSE ,'sentence':Sentence,'targetFrame':TargetFrame, 'eTarget':ETarget, 'sTarget':STarget}
        annotation_line = line.split('\t')
        id = annotation_line[0]
        span = annotation_line[1]
        anno_type = annotation_line[2]
        kwargs={}
        kwargs['annotation_id']= id
        kwargs['span']= span

        attributes = annotation_line[3]
        attributes = attributes.replace('-','_')

        attributes = attributes.split(' ') # this wont work for some attitude cases
        attributes = attributes[:-1] # to deal with an empty element that was appearing
        for attr in attributes:
            #print('attr',attr)
            if('=' in attr):
                key_val = attr.split('=')
                try:
                    kwargs[key_val[0]] = key_val[1]
                except IndexError:
                    print('anno_type', anno_type)
                    print('attributes', attributes)
                    print('IndexError', key_val)
                    print('attr', attr)
                finally:
                    #print(key_val[0], '=', key_val[1])
                    pass
            else:

                pass
            #print('key_val',key_val)
        try:
            #print(kwargs)
            #print('anno_type',anno_type)
            b = dict[anno_type](**kwargs)
            if(anno_type=='direct-subjective'):
                print(dict[anno_type],kwargs)
            #print(anno_type,dict[anno_type],'kwargs:',kwargs)
            return b
        except KeyError:
            #print('dict error', anno_type)
            #print('annotation_line',annotation_line)
            pass
        except TypeError:
            pass
            #print('TypeError',kwargs)
        finally:
            print('finally',anno_type)
            pass

    def getFullPath(self, doc_type, doc_path):
        return str(self.path + '/' + doc_type + '/' + doc_path)

    def list_files(self, corpus):
        files = corpus.fileids()
        print('listing files: ')
        for f in files:
            print(f)


print('1:config step..')
config = Config([MPQA.name])
config.run()
mpqa = MPQA(config.data_path, config.getCorpusPath(config.corpusList[0]))
