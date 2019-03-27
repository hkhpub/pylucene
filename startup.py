# -*- coding: utf-8 -*-
# Created by hkh at 2019-02-19
import lucene
from java.io import StringReader
from org.apache.lucene.analysis.standard import StandardAnalyzer, StandardTokenizer
from org.apache.lucene.analysis.tokenattributes import CharTermAttribute

lucene.initVM(vmargs=['-Djava.awt.headless=true'])

# Basic tokenizer example.
test = "This is how we do it."
tokenizer = StandardTokenizer()
tokenizer.setReader(StringReader(test))

charTermAttrib = tokenizer.getAttribute(CharTermAttribute.class_)
tokenizer.reset()

tokens = []
while tokenizer.incrementToken():
    tokens.append(charTermAttrib.toString())

print(tokens)

# StandardAnalyzer example.
analyzer = StandardAnalyzer()
stream = analyzer.tokenStream("", StringReader(test))
stream.reset()
tokens = []
while stream.incrementToken():
    tokens.append(stream.getAttribute(CharTermAttribute.class_).toString())
print(tokens)
