# -*- coding: utf-8 -*-
# @Time : 2022/11/25
# @Author : wmj
# @Email : wmj142326@163.com
# @File : image_compare.py
# @Note : 上一次视频九宫格，这一次图像对比，图像拼接
# ---------------------------
import os
import cv2
from tqdm import tqdm
import numpy as np


def create_folder(folder):
    """ Create a folder."""
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder


def pic_stitch(imgA, imgB,  # 图片路径
               stack='h',  # 拼接方式
               img_A_show_name=None, img_B_show_name=None,  # 显示名称
               out_name='pic_stitch.jpg'):  # 输出文件名
    """
        水平合成图片A、B
    """
    img_array_A = cv2.imread(imgA)
    cv2.putText(img_array_A, img_A_show_name, (50, 100), cv2.FONT_HERSHEY_COMPLEX, 1.5, (300, 200, 100), 3)
    img_array_B = cv2.imread(imgB)
    cv2.putText(img_array_B, img_B_show_name, (50, 100), cv2.FONT_HERSHEY_COMPLEX, 1.5, (300, 200, 100), 3)
    if stack == "h":
        img_array_AB = np.hstack((img_array_A, img_array_B))
    if stack == 'v':
        img_array_AB = np.vstack((img_array_A, img_array_B))
    cv2.imwrite(out_name, img_array_AB)


def main():
    img_1 = "./img_1"
    img_2 = "./img_2"
    img_out = create_folder("./img_out")
    for img in tqdm(os.listdir(img_1)):
        img_name = img
        img_A = os.path.join(img_1, img_name)
        img_B = os.path.join(img_2, img_name)
        out_name = os.path.join(img_out, img_name)

        pic_stitch(img_A, img_B,
                   stack='v',
                   img_A_show_name=img_name + "_input",
                   img_B_show_name=img_name + "_out",
                   out_name=out_name)


if __name__ == "__main__":
    print("------------------------START------------------------")
    main()
    print("-------------------------END-------------------------")
