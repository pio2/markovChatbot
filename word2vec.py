# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 19:29:51 2021

@author: keigo
"""
#import spacy
from difflib import SequenceMatcher

def get_trust(user: str, com: list) -> str:
    ratio = {}
    for i in com:
        s = SequenceMatcher(None, user, i)
        ratio[s.ratio()] = i
    return ratio[max(list(ratio.keys()))]

#nlp = spacy.load("ja_ginza")

"""
def get_similar_word(word) -> str:
    return nlp("ラーメン屋はおいしい").similarity(nlp("ラーメンはおいしくない"))

print(get_similar_word("日本"))
doc = nlp('今年の夏休みは北海道に行きました。とても寒かったです。僕の名前は豊島圭吾です。')
for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)
    #print(ent)
"""