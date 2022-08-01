# -*- coding: utf-8 -*-
# @Time : 2022/8/1
# @Author : wmj
# @Email : wmj142326@163.com
# @File : img_ext_tras.py.py
# @Note : 
# ---------------------------
import os


def create_folder(folder):
    """ Create a folder."""
    if os.path.exists(folder):
        pass
    else:
        os.makedirs(folder)
    return folder


def main():
    pass


if __name__ == "__main__":
    main()
    print("finished!")
