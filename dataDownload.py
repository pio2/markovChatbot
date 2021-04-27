# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 10:57:34 2021

@author: keigo
"""
import urllib.request as request
import zipfile
import os

def data_download(url):
    try:
        if os.path.exists("./text_data/conversation_data.zip"):
            return
        request.urlretrieve(url, "./text_data/conversation_data.zip")
    except:
        print("Data Download Failed")
        
def open_zipfile(path):
    data_download("https://mmsrv.ninjal.ac.jp/nucc/nucc.zip")
    try:
        texts = ""
        with zipfile.ZipFile(path) as myzip:
            for file_path in myzip.namelist():
                if ".txt" not in file_path:
                    continue
                with myzip.open(file_path, "r") as f:
                    text = f.read().decode().split("\n")
                    new_text = ""
                    for i in text:
                        if "＠" not in i and "％" not in i:
                            if "：" in i:
                                i = i.split("：")[1]
                            new_text += i
                    texts += new_text
        return texts
    except FileNotFoundError:
        print("File Not Found")
        

    















