# -*- coding: utf-8 -*-
# Created by hkh at 2019-02-19

import lucene
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.store import FSDirectory, RAMDirectory
from org.apache.lucene.index import IndexWriter
from org.apache.lucene.index import IndexWriterConfig
from org.apache.lucene.document import Document
from org.apache.lucene.document import Field
from org.apache.lucene.document import TextField
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import ScoreDoc
from org.apache.lucene.search.similarities import BM25Similarity


import nltk
from nltk.tokenize.api import StringTokenizer

nltk.download('gutenberg')
# nltk.corpus.gutenberg.fileids()
# 53,996 sentences - 5400 documents
gutenberg_list = ['austen-emma.txt', 'austen-persuasion.txt', 'austen-sense.txt', 'bible-kjv.txt',
'blake-poems.txt', 'bryant-stories.txt', 'burgess-busterbrown.txt',
'carroll-alice.txt', 'chesterton-ball.txt', 'chesterton-brown.txt',
'chesterton-thursday.txt', 'edgeworth-parents.txt', 'melville-moby_dick.txt',
'milton-paradise.txt', 'shakespeare-caesar.txt', 'shakespeare-hamlet.txt',
'shakespeare-macbeth.txt', 'whitman-leaves.txt']

lucene.initVM(vmargs=['-Djava.awt.headless=true'])
analyzer = StandardAnalyzer()

# store the index in memory
# directory = RAMDirectory()

# # store the index in File System
file = File("/home/hkh/data/gutenbergindex")
directory = FSDirectory.open(file.toPath())

config = IndexWriterConfig(analyzer)
iwriter = IndexWriter(directory, config)

# for txtName in gutenberg_list:
#   words = nltk.corpus.gutenberg.words(txtName)
#   sents = " ".join(words).split(".")
#   print(sents[:100])
# #   print("Indexing ", txtName, "...")
# #   for i in range(0, len(sents), 10):
# #     text = " ".join(sents[i:i+10])
# #     doc = Document()
# #     doc.add(Field("fieldname", text, TextField.TYPE_STORED))
# #     iwriter.addDocument(doc)
# # iwriter.close()


# now search the index
ireader = DirectoryReader.open(directory)
isearcher = IndexSearcher(ireader)

# set similarity method
bm25 = BM25Similarity()
isearcher.setSimilarity(bm25)

# parse a simple query that searches for "text"
parser = QueryParser("fieldname", analyzer)
query = parser.parse("her sister was reading")
hits = isearcher.search(query, 5).scoreDocs
print(len(hits))

for hit in hits:
  result = isearcher.doc(hit.doc)
  print("[%8.4f] %s" % (hit.score, result.get("fieldname")))
