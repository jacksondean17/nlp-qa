from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet as wn
import nltk
from nltk.wsd import lesk
import pprint
import numpy as np

import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()


def tag(sentence):
    words = word_tokenize(sentence)
    words = pos_tag(words)
    return words


def paraphraseable(tag):
    return tag.startswith('NN') or tag == 'VB' or tag.startswith('JJ')


def pos(tag):
    if tag.startswith('NN'):
        return wn.NOUN
    elif tag.startswith('V'):
        return wn.VERB


def synonyms(word, tag):
    lemma_lists = [ss.lemmas() for ss in wn.synsets(word, pos(tag))]
    lemmas = [lemma.name() for lemma in sum(lemma_lists, [])]
    return set(lemmas)


def synonymIfExists(sentence):
    for (word, t) in tag(sentence):
        if paraphraseable(t):
            syns = synonyms(word, t)
            if syns:
                if len(syns) > 1:
                    yield [word, list(syns)]
                    continue
        yield [word, []]


def paraphrase(sentence):
    return [x for x in synonymIfExists(sentence)]


def ner(sentence):
    tagged = tag(sentence)
    return nltk.ne_chunk(tagged, binary=False)

def get_sense(sentence, word):
    return lesk(sentence, word)


# p = paraphrase("The quick brown fox jumps over the lazy dog")
# print(p)

print('NLTK')
print(tag("European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices"))
n = ner("European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices.")
print(n)

print('Spacy')
doc = nlp("European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices.")
print(doc.ents)
