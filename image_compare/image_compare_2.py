# -*- coding: utf-8 -*-
# @Time : 2022/11/29
# @Author : wmj
# @Email : wmj142326@163.com
# @File : image_compare.py
# @Note : 图像拼接的一个新函数：from torchvision.utils import make_grid
# ---------------------------
import os
import cv2
import torchvision.utils
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm
from torchvision.utils import make_grid
import torchvision.transforms as transforms


def create_folder(folder):
    """ Create a folder."""
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder


def get_img_list(img_folder):
    img_path_list = os.listdir(img_folder)
    img_path_list.sort(key=lambda i: int(i.split('.')[0]))  # 排序

    img_list = []

    for img in tqdm(img_path_list):
        img_path = os.path.join(img_folder, img)
        image = cv2.imread(img_path)
        cv2.putText(image, img, (50, 100), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  # cv转PIL
        trans = transforms.ToTensor()  # PIL转Tensor
        image = trans(image)

        img_list.append(image)
    return img_list


def main():
    img_1 = "./img_1"
    img_list = get_img_list(img_1)
    img_out = make_grid(img_list, nrow=3, padding=10, pad_value=1)
    torchvision.utils.save_image(img_out, "out.jpg")


if __name__ == "__main__":
    print("------------------------START------------------------")
    main()
    print("-------------------------END-------------------------")
