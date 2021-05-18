# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 13:06:33 2021

@author: keigo
"""
import MeCab
from collections import deque
import pickle
import random
import dataDownload
import question
import word2vec
import win32com.client as wincl
from numba import jit


# 単語に反応してそれから始まる文を生成しているだけのボット
class markovBot:
    analyzer = question.Analyzer()
    log = {}  # user : bot
    tagger = MeCab.Tagger("おはよう。")
    tagger.parse("")
    voice = wincl.Dispatch("SAPI.SpVoice")
    model = {}

    def speech(self, text):
        self.voice.Speak(text)

    def load_text_data(self, directory_path):
        return dataDownload.open_zipfile("./text_data/conversation_data.zip")

    def wakati(self, text):
        """
        using mecab
        Morphological Analysis("形態素解析")

        Parameters
        ----------
        text : str
            DESCRIPTION.unioned learning data -> str

        Returns
        -------
        res : list
            DESCRIPTION.splited word(Morphological Analysis("形態素解析"))

        """
        res = []
        node = self.tagger.parseToNode(text)
        while node:
            res.append(node.surface)
            node = node.next
        return res

    # 始点を "[BOS]" として終点を "。" とする
    def makeModel(self, text, order=4):
        # word_list = 形態素解析済みdata(list)
        word_list = self.wakati(text)
        # print(word_list)
        if len(word_list) <= order:
            return
        queue = deque([], order)
        queue.append("[BOS]")
        for markov_value in word_list:
            if len(queue) < order:
                queue.append(markov_value)
                continue

            if queue[-1] == "。":
                markov_key = tuple(queue)
                if markov_key not in self.model:
                    self.model[markov_key] = []
                self.model.setdefault(markov_key, []).append("[BOS]")
                queue.append("[BOS]")
            markov_key = tuple(queue)
            self.model.setdefault(markov_key, []).append(markov_value)
            queue.append(markov_value)
        # print(self.model)

    def saveModel(self):
        with open("./markov_model.binaryfile", "wb") as file:
            pickle.dump(self.model, file)

    def loadModel(self, path="./markov_model.binaryfile"):
        try:
            with open(path, "rb") as file:
                self.model = pickle.load(file)
        except FileNotFoundError:
            print("モデルが保存されていないので初期化します")
            self.makeModel(self.load_text_data(""))

    def makeSentence(self, sentence_num=5, seed="[BOS]", max_words=1000):
        sentence_count = 0

        key_candidates = [key for key in self.model if key[0] == seed]
        if not key_candidates:
            print("Not found Keyword")
            return
        markov_key = random.choice(key_candidates)
        queue = deque(list(markov_key), len(list(self.model.keys())[0]))

        sentence = "".join(markov_key)
        for _ in range(max_words):
            markov_key = tuple(queue)
            next_word = random.choice(self.model[markov_key])
            sentence += next_word
            queue.append(next_word)

            if next_word == "。":
                sentence_count += 1
                if sentence_count == sentence_num:
                    break
        return sentence

    def make_response(self, user_text: str) -> list:
        pass

    @jit
    def start_chat(self):
        end_word = ["さようなら", "またね", "ばいばい", "バイバイ"]
        tagger = MeCab.Tagger("")

        while True:
            user_text = input("You -> ")
            # if input is end_word, chat end
            if (user_text in end_word):
                print("Bot -> " + user_text)
                return
            if user_text[-1] != "。":
                user_text += "。"
            self.makeModel(user_text)
            tagger.parse("")
            node = tagger.parseToNode(user_text)
            # ?があるか
            if self.analyzer.judgment(user_text):
                while node:
                    word = node.surface
                    pos = node.feature.split(',')[0]
                    if pos == "名詞":
                        sentence = self.analyzer.association(word)
                        if sentence == word:
                            print("処理未実装")
                        print("Bot -> " + word + "は" + sentence + "です。")
                        self.log[word] = sentence
                        break
                    node = node.next
            else:
                while node:
                    word = node.surface
                    pos = node.feature.split(',')[0]
                    if pos == "感動詞":
                        print("Bot -> " + word)
                        self.log[word] = word
                    elif (pos in ["名詞", "形容詞", "動詞"]):
                        sentences = []
                        for _ in range(10):
                            sentences.append(self.makeSentence(seed=word, sentence_num=1))
                        if None not in sentences:
                            sentence = word2vec.get_trust(user_text, sentences)
                            print("Bot -> " + sentence)
                            self.log[word] = sentence
                        # print(sentences)
                    node = node.next


if __name__ == "__main__":
    bot = markovBot()
    bot.loadModel()
    bot.start_chat()
    bot.saveModel()
    
        
        
