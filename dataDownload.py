# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 10:57:34 2021

@author: keigo
"""
import urllib.request
import zipfile
import os


def data_download(url, dst_path="./text_data/conversation_data.zip"):
    """
    if learning data is none, get data.
    Parameters
    ----------
    url : str
        DESCRIPTION. learning data url
    dst_path : str
        DESCRIPTION. save dir.The default is "./text_data/conversation_data.zip".

    Returns
    -------
    None.

    """
    try:
        # get dir (dst_dir = "./text_data")
        dst_dir = os.path.dirname(dst_path)

        # case1: no dir no file,case2:exist dir no file
        # if dir is none,make dir
        if not os.path.isdir(dst_dir):
            os.mkdir(dst_dir)
        # if file not found,download and save file
        if not os.path.exists(dst_path):
            print("学習データがないのでダウンロード中")
            with urllib.request.urlopen(url) as web_file, open(dst_path, 'wb') as local_file:
                local_file.write(web_file.read())
            print("学習データダウンロード完了")

    except Exception as e:
        print('***** 学習データダウンロードエラー *****')
        print(e)
        print('**********************************')


def open_zipfile(path):
    """
    union learning data

    Parameters
    ----------
    path : str
        DESCRIPTION.learning data path

    Returns
    -------
    texts : str
        DESCRIPTION.unioned learning data

    """
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

    















