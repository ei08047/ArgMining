
ComArg -- Corpus of Online User Comments with Arguments

Provided by: 
Text Analysis and Knowledge Engineering Lab, FER, University of Zagreb
http://takelab.fer.hr

Version: 1.0
Release date: June 26, 2014

1 Description

ComArg is a dataset of online user comments manually annotated with
comment-argument pairs. The dataset is created for the argument recognition
task: identifying what arguments, from a predefined set of arguments, have been
used in users’ comments, and how. The task and the dataset are described in:

  Filip Boltužić and Jan Šnajder (2014). Back up your Stance: Recognizing
  Arguments in Online Discussions. In Proceedings of the First Workshop on
  Argumentation Mining, Baltimore, Maryland. Association for Computational
  Linguistics, 49-58.
  http://www.aclweb.org/anthology/W/W14/W14-2107.pdf

If you use the ComArg dataset for your own work, please cite the above paper.
The BibTeX citation is:

  @InProceedings{boltuzic2014back,
    author    = {Boltu\v{z}i\'{c}, Filip  and  \v{S}najder, Jan},
    title     = {Back up your Stance: Recognizing Arguments in Online
                 Discussions},
    booktitle = {Proceedings of the First Workshop on Argumentation Mining},
    month     = {June},
    year      = {2014},
    address   = {Baltimore, Maryland},
    publisher = {Association for Computational Linguistics},
    pages     = {49--58},
    url       = {http://www.aclweb.org/anthology/W14-2107}
  }

2 Dataset

The dataset is available from here: comarg.v1.tar.gz. The archive contains two
files:

  GM.xml
  UGIP.xml

The files contain comments from two on-line discussions, Gay Marriages (GM) and
Under God in pledge (UGIP), containing 1285 and 1013 comment-argument pairs,
respectively, each classified into one of five classes (see paper for details).
The format is as follows:

  <unit id="...">
    <comment>
      <text>...</text>
      <stance>...</stance>
    </comment>
    <argument>
      <text>...</text>
      <stance>...</stance>
    </argument>
    <label>...</label>
  </unit>

3 License

This work is licensed under a Creative Commons
Attribution-NonCommercial-ShareAlike 3.0 Unported License.

