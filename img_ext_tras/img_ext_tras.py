# -*- coding: utf-8 -*-
# @Time : 2022/8/1
# @Author : wmj
# @Email : wmj142326@163.com
# @File : img_ext_tras.py.py
# @Note : 
# ---------------------------
import os
import shutil
import numpy as np
from PIL import Image
import random
import cv2


def create_folder(folder):
    """ Create a folder."""
    if os.path.exists(folder):
        pass
    else:
        os.makedirs(folder)
    return folder


# 获取路径下所有相同后缀名文件
def Re_file(input_path, out_list, end_with='.jpg'):
    """
    :param input_path: files root path.
    :param out_list: [].
    :param end_with: file extension.
    :return: out list of file path.
    """
    for i in os.listdir(input_path):
        i = os.path.join(input_path, i)
        if os.path.isfile(i):
            if os.path.splitext(i)[1] == end_with:
                out_list.append(i)
        else:
            Re_file(i,out_list, end_with)
    return out_list


def rename_file(inpath, outpath, ext_input=".png", ext_output=".jpg"):
    out_list = []
    out_list = Re_file(inpath, out_list, end_with=ext_input)
    for i in range(len(out_list)):
        img_path = out_list[i]
        target_path = os.path.join(outpath, os.path.splitext(img_path.split("/")[-1])[0] + ext_output)
        shutil.copy(img_path, target_path)
        print("[{}/{}]".format(i, len(out_list)), img_path, "-->", target_path)
    return None


def img_to_jpg(inpath, outpath, ext_input=".png", ext_output=".txt"):
    out_list = []
    out_list = Re_file(inpath, out_list, end_with=ext_input)
    for i in range(len(out_list)):
        im = Image.open(out_list[i])
        im = im.convert('RGB')
        target_path = os.path.splitext(out_list[i].split("/")[-1])[0] + ext_output
        im.save(os.path.join(outpath, target_path), quality=100)
        print("[{}/{}]".format(i, len(out_list)), out_list[i], "-->", os.path.join(outpath, target_path))

    return None


def main():
    inpath = "images_input"
    outpath = "images_output"

    out_list = []
    file_list = Re_file(inpath, out_list, end_with='.jpg')
    print(file_list)

    # 任意格式转换为jpg
    img_to_jpg(inpath, outpath, ext_input=".jpg", ext_output=".png")


if __name__ == "__main__":
    main()
    print("finished!")
