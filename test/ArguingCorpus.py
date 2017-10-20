import Config
from Corpus import Corpus
import re
import os
import shutil
from nltk.corpus.reader import XMLCorpusReader,XMLCorpusView


doclist_healthcare_train_anti='doclist_healthcare_train_anti.txt'
doclist_healthcare_train_pro='doclist_healthcare_train_pro.txt'
anti_list = []
pro_list = []
class Text(object):
    def __init__(self, name, raw ):
        self.name=name
        self.raw = raw

class ArguingCorpus(object):
    def __init__(self,path):
        self.path = path



print('1:config step..')
config = Config.Config(['arguing_corpus'])
config.run()

print('reading arguing_corpus corpus')
corpus_path = config.getCorpusPath(config.corpusList[0])
arguing_corpus = Corpus(config.data_path,corpus_path , '/training')
##arguing_corpus.view()

##prepare file structure to feed opinion finder
if(False):
    a_c = 'arguing_corpus'
    a_c_d = a_c + '/doc_list'

    doc_list = []
    if (os.path.exists(a_c) and os.path.exists(os.path.exists(a_c))):
        print('arguing_corpus and doc list exists')
        print(os.path.exists(arguing_corpus.path))
        for doc in arguing_corpus.all_list:
            if(os.path.exists( arguing_corpus.path + '/'+doc)):
                folder_name = doc.split('/')[1].replace('.txt','')
                doc_list.append(folder_name)
                print(folder_name, ' file exists')
                os.mkdir('arguing_corpus'+'/'+folder_name)
                #copy for
                shutil.copy(arguing_corpus.path + '/'+doc, 'arguing_corpus'+'/'+folder_name)
            else:
                print('not found',doc)
        with open(a_c_d,'a') as file:
            for doc in doc_list:
                file.write('database/docs/arguing_corpus/'+doc + '/' + doc + '.txt' +'\n')
    else:
        print('no')


## read arguing corpus annotations
    ##span start end
        ## <Annotation Id="13" Type="arg" StartNode="55" EndNode="104">
xmlCorpusReader = XMLCorpusReader(arguing_corpus.path,  'training/.*xml')
OC_docs = xmlCorpusReader.fileids()


arg_annotations = {}  ## key = documentId : value = [Arg_Span]

class Span:
    def __init__(self,start,end):
        self.start=start
        self.end=end
    def match(self,other):
        if(self.start < other.start and self.end < other.start):
            return -1
        elif (self.start > other.start and other.end < self.start):
            return -1
        else:
            return 1



class Arg(Span):
    def __init__(self,id,span):
        self.id=id
        super(Arg,self).__init__(span.start,span.end)

class Sub(Span):
    def __init__(self,span):
        super(Sub,self).__init__(span.start,span.end)
class Obj(Span):
    def __init__(self,span):
        super(Obj,self).__init__(span.start,span.end)

#read arg annotations
all_arg_dict={}
for id_doc in OC_docs:
    argList = []
    x = XMLCorpusView(arguing_corpus.path+'/'+id_doc,'GateDocument/AnnotationSet/Annotation.*')
    args = [a for a in x if a.attrib['Type']== 'arg']
    arg_annotations[id_doc] = args
    for ann in args:
        a = Arg(ann.attrib['Id'],Span(int(ann.attrib['StartNode']),int(ann.attrib['EndNode'])))
        argList.append(a)

    p = re.compile('training/(.{5}).xml$')
    id=p.match(id_doc).group(1)

    all_arg_dict[id] = argList

print(all_arg_dict)

## read opinion finder output
    ## sentence label(obj/sub) start end
    ## hc084_hc084.txt_1725_1825	obj
results_dict = {}
sub_obj_dict = {'obj':Obj , 'subj':Sub}
for id_doc in OC_docs:
    p = re.compile('training/(.{5}).xml$')
    id=p.match(id_doc).group(1)
    opinion_finder_result = 'opinionfinderv2.0/database/docs/arguing_corpus/' +id + '/' + id + '.txt_auto_anns/sent_subj.txt'
    line_pattern = re.compile('.{5}_.{5}.txt_(.{1,5})_(.{1,5})..(obj|subj)\n')
    ann_list=[]
    with open(opinion_finder_result) as file:
        content = file.readlines()
        for x in content:
            try:
                #print(line_pattern.findall(x).pop())
                (start,end,sub_obj) = line_pattern.findall(x).pop()
                ann = sub_obj_dict[sub_obj](Span(int(start),int(end)))
                ann_list.append(ann)
            except ValueError:
                print('ValueError', x)
            except IndexError:
                print('IndexError', x)
            finally:
                #print(start,end,sub_obj)
                pass
        #line_pattern.match(x).group(1)
    results_dict[id]= ann_list
print(results_dict)

sub_results_dict={}
obj_results_dict={}
for id in results_dict.keys():
    anns = results_dict[id]
    sub_results_dict[id] = [sub_anns for sub_anns in anns if type(sub_anns).__name__=='Sub' ]
    obj_results_dict[id] = [obj_anns for obj_anns in anns if type(obj_anns).__name__=='Obj' ]
    #print(id, 'sub:',len(sub_results_dict[id]),'obj:',len(obj_results_dict[id]))

num_sub_matches=0
num_obj_matches=0
num_sub=0
num_obj=0
num_arg=0

for id in all_arg_dict:
    num_sub_matches_per_document = 0
    num_obj_matches_per_document = 0
    sub_nodes = sub_results_dict[id]
    obj_nodes = obj_results_dict[id]
    arg_nodes = all_arg_dict[id]
    for arg in arg_nodes:
        for sub in sub_nodes:
            if(arg.match(sub)!= -1 ):
                num_sub_matches_per_document = num_sub_matches_per_document + 1
    for arg in arg_nodes:
        for obj in obj_nodes:
            if(arg.match(obj)!= -1 ):
                num_obj_matches_per_document = num_obj_matches_per_document + 1


    num_sub_sentences_per_document = len(sub_nodes)
    num_obj_sentences_per_document = len(obj_nodes)
    num_arg_spans_per_document = len(arg_nodes)

    num_sub_matches = num_sub_matches + num_sub_matches_per_document
    num_obj_matches = num_obj_matches + num_obj_matches_per_document
    num_arg = num_arg + num_arg_spans_per_document
    num_sub = num_sub + num_sub_sentences_per_document
    num_obj = num_obj + num_obj_sentences_per_document

    print('docId:', id, ' ##num Sentences:', num_sub_sentences_per_document + num_obj_sentences_per_document, ' ##num Args:', num_arg_spans_per_document)
    print(' ##       num Sub Matches', num_sub_matches_per_document, '##num Sub Sentences:', num_sub_sentences_per_document)
    print(' ##       num Obj Matches', num_obj_matches_per_document, '##num Obj Sentences:', num_obj_sentences_per_document)
    print('#ObjArg/#Obj : ', round (float(num_obj_matches_per_document / num_obj_sentences_per_document), 4), '#SubArg/#Sub : ', round(float(num_sub_matches_per_document / num_sub_sentences_per_document), 4))

print('\n\n\n', 'Totals: \n')

print(' ##num Sentences:', num_sub + num_obj,
      ' ##num Args:', num_arg)
print(' ##       num Sub Matches', num_sub_matches, '##num Sub Sentences:', num_sub)
print(' ##       num Obj Matches', num_obj_matches, '##num Obj Sentences:', num_obj)
print('#ObjArg/#Obj : ', round(float(num_obj_matches / num_obj), 4),
      '#SubArg/#Sub : ', round(float(num_sub_matches / num_sub), 4))

