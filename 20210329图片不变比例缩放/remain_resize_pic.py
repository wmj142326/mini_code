# -*- coding = utf-8 -*-
# @time:2021/3/29 8:46
# Author:wmj
# @File:remain_resize_pic.py
# @Software:PyCharm
# @Function:不改变长宽比缩放图片
# 参考链接：https://blog.csdn.net/jizhidexiaoming/article/details/109141625

import cv2
import numpy as np


# 缩放
def letterbox_image(img, input_dim):
    """
    resize image with unchanged aspect ratio using padding
    让原图的高宽乘以同一个数，这样就不会改变比例，而这个数就是min( 高缩放的比例，宽缩放的比例)，然后padding周围区域使得缩放到指定大小。
    缩小： (2000, 4000) -> (200,200), min(200/4000, 200/2000) = 1/20, 2000 * 1/20 = 100， 4000 * 1/20 = 200
    新的尺度(100, 200)，再padding
    放大： (50, 100) -> (200, 200), min(4, 2) = 2, 50 * 2 = 100, 100 * 2 = 200
    新的尺度(100, 200)，再padding
    :param img: 原始图片
    :param input_dim: (w, h). 缩放后的尺度
    :return:
    """
    orig_w, orig_h = img.shape[1], img.shape[0]
    input_w, input_h = input_dim  # 缩放(orig_w, orig_h) -> (input_w, input_h)

    # 1，根据缩放前后的尺度，获取有效的新的尺度(new_w, new_h)
    min_ratio = min(input_w / orig_w, input_h / orig_h)
    new_w = int(orig_w * min_ratio)  # （new_w, new_h）是高宽比不变的新的尺度
    new_h = int(orig_h * min_ratio)
    resized_image = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_CUBIC)

    # 定义画布canvas，然后把有效区域resized_image填充进去
    canvas = np.full((input_dim[1], input_dim[0], 3), 128, np.uint8)  # 定义画布，大小是（200,200）

    # 画布_h - 高宽不变_new_h
    start_h = (input_h - new_h) // 2  # 开始插入的高度位置, 也是上下需要padding的大小
    start_w = (input_w - new_w) // 2  # 开始插入的宽度位置
    canvas[start_h:start_h + new_h, start_w:start_w + new_w, :] = resized_image

    return canvas


# 反缩放
def de_letterbox_image(output_canvas, orig_dim):
    """
    去除padding部分，获取原始尺寸对应的区域数据
    :param output_canvas: 含有padding区域的结果图，是缩放后的结果图
    :param orig_dim: (w, h)，原始图片的尺度
    :return:
    """
    orig_w, orig_h = orig_dim[0], orig_dim[1]
    # 缩放(orig_w, orig_h) -> (input_w, input_h)
    input_w, input_h = output_canvas.shape[1], output_canvas.shape[0]  # 画布的尺度，缩放后的尺度，也是输入网络中的尺度

    # 1，根据缩放前后的尺度，获取有效的新的尺度(new_w, new_h)
    min_ratio = min(input_w / orig_w, input_h / orig_h)
    new_w = int(orig_w * min_ratio)  # （new_w, new_h）是高宽比不变的新的尺度
    new_h = int(orig_h * min_ratio)

    # 2，从画布中，截取有效区域
    start_h = (input_h - new_h) // 2
    start_w = (input_w - new_w) // 2
    real_output = output_canvas[start_h:start_h + new_h, start_w:start_w + new_w, :]
    return real_output


if __name__ == '__main__':
    img_path = '0.jpg'
    orig_img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    cv2.namedWindow('orig_img', cv2.WINDOW_NORMAL), cv2.imshow('orig_img', orig_img), cv2.waitKey()
    cv2.imwrite('orig_img.jpg', orig_img)
    # 1，缩放到同一个尺度
    input_img = letterbox_image(orig_img, (1000, 1000))
    cv2.namedWindow('input_img', cv2.WINDOW_NORMAL), cv2.imshow('input_img', input_img), cv2.waitKey()
    cv2.imwrite('input_img.jpg', input_img)
    # 2，网络前向，输出结果图
    output_img = input_img

    # 3，去除padding部分，获取有效部分
    real_output = de_letterbox_image(output_canvas=output_img, orig_dim=(orig_img.shape[1], orig_img.shape[0]))
    cv2.namedWindow('real_output', cv2.WINDOW_NORMAL), cv2.imshow('real_output', real_output), cv2.waitKey()
    cv2.imwrite('real_output.jpg', real_output)

