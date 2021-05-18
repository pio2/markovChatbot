# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 18:35:17 2021

@author: keigo
"""
import json
import random


class Analyzer:
    #
    # 質問文を解析して連想を行う
    #
    association_dic = {}

    def __init__(self):
        try:
            with open("./Association_data.json", "r", encoding="utf-8") as myjson:
                self.association_dic = json.load(myjson)
        except Exception as e:
            print('***** json file load error*****')
            print(e)
            print('**********************************')

    def save_dic(self):
        with open("./Association_data.json", "w", encoding="utf-8") as myjson:
            json.dump(self.association_dic, myjson, ensure_ascii=False, indent=2)

    def judgment(self, text) -> bool:
        if "?" in text or "？" in text:
            return True
        return False

    def association(self, word: str, max_dip: int = 2, dep: int = 0) -> str:
        if dep >= max_dip:
            return word
        if word not in self.association_dic.keys():
            return word
        synapse = self.association_dic[word]
        association_word = random.choice(synapse)
        return self.association(association_word, max_dip, dep + 1)
