# -*- coding: utf-8 -*-
# @Time : 2022/7/26
# @Author : wmj
# @Email : wmj142326@163.com
# @File : video_compare.py
# @Note : 视频拼接对比展示,对比视频时长应一致

# ---------------------------------------------------
# +-----+-----+-----+       +-----+-----+
# |  1  |  2  |  3  |       |  1  |  2  |
# +-----+-----+-----+       +-----+-----+
# |  4  |  5  |  6  |       |  3  |  4  |
# +-----+-----+-----+       +-----+-----+
# |  7  |  8  |  9  |       |  5  |  6  |
# +-----+-----+-----+       +-----+-----+
# ---------------------------------------------------

import os
import cv2
import shutil
import os.path as osp

import numpy as np
from vid_img_trasform import images_to_video


def create_folder(folder):
    """ Create a folder."""
    if os.path.exists(folder):
        pass
    else:
        os.makedirs(folder)
    return folder


def video_compare(video_arr, video_label, out_name, label_color=(0, 0, 255)):
    assert len(np.shape(video_arr)) == 2, "请使用[[]],而不是[],且确保列数相等"
    h, w = np.shape(video_arr)[0], np.shape(video_arr)[1]
    cap_video = cv2.VideoCapture(video_arr[0][0])
    ret, frame = cap_video.read()
    size = (int(cap_video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap_video.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    img_screen = np.zeros([size[1] * h, size[0] * w, 3])

    for i in range(h):
        for j in range(w):
            print("[{0}][{1}]".format(i, j), "video:", video_arr[i][j], "  label:", video_label[i][j])
            exec('cap_video_{}_{}=cv2.VideoCapture(video_arr[i][j])'.format(i, j))
            exec('ret_{0}_{1}, frame_{0}_{1} = cap_video_{0}_{1}.read()'.format(i, j))

    tmp_img_folder = create_folder("tmp_img_folder")
    frame_id = 0
    while ret:
        print("\r", "frame_id: ---", frame_id, "---", end="", flush=True)
        ret, frame = cap_video.read()
        frame_id += 1
        for i in range(h):
            for j in range(w):
                exec('ret_{0}_{1}, frame_{0}_{1} = cap_video_{0}_{1}.read()'.format(i, j))
                exec('vid_name_{}_{} = video_label[i][j]'.format(i, j))
                exec('cv2.putText(frame_{0}_{1}, vid_name_{0}_{1}, \
                                    (50, 100), cv2.FONT_HERSHEY_COMPLEX, 1.5, label_color, 3)'.format(i, j))
                exec('img_screen[size[1] * {0}:size[1] * {1}, size[0] * {2}:size[0] * {3}]=frame_{0}_{2}'.format(
                    i, i + 1, j, j + 1))

        cv2.imwrite(osp.join(tmp_img_folder, f'{frame_id:06d}.jpg'), img_screen)
    images_to_video(tmp_img_folder, out_name)
    shutil.rmtree(tmp_img_folder)


def main():
    # 视频序列路径和label
    vid_1 = "/home/wmj/Downloads/vis_results/multi_vibe.mp4"
    label_1 = "multi_vibe"

    vid_2 = "/home/wmj/Downloads/vis_results/multi_vibe_smooth.mp4"
    label_2 = "multi_vibe_smooth"

    vid_3 = "/home/wmj/Downloads/vis_results/multi_vibe_smooth_deciwatch.mp4"
    label_3 = "multi_vibe_smooth_deciwatch"

    vid_4 = "/home/wmj/Downloads/vis_results/multi_vibe_deciwatch.mp4"
    label_4 = "multi_vibe_deciwatch"

    vid_5 = "/home/wmj/Downloads/vis_results/multi.mp4"
    label_5 = "multi"

    vid_6 = "/home/wmj/Downloads/vis_results/multi/123.mp4"
    label_6 = "multi_result"



    # 排列方式1
    # video_list = [[vid_1, vid_2, vid_3, vid_4, vid_5, vid_6]]
    # video_label = [[label_1, label_2, label_3, label_4, label_5, label_6]]

    # 排列方式2
    video_list = [[vid_5, vid_6],
                  [vid_1, vid_2],
                  [vid_3, vid_4]]

    video_label = [[label_5, label_6],
                   [label_1, label_2],
                   [label_3, label_4]]

    # 排列方式3
    # video_list = [[vid_1, vid_2, vid_3],
    #               [vid_4, vid_5, vid_6],
    #               [vid_1, vid_2, vid_3],
    #               [vid_1, vid_2, vid_3]]
    # video_label = [[label_1, label_2, label_3],
    #                [label_4, label_5, label_6],
    #                [label_1, label_2, label_3],
    #                [label_1, label_2, label_3]]
    # 输出文件名
    out_video_name = "/home/wmj/Downloads/vis_results/multi_compare.mp4"
    video_compare(video_list, video_label, out_video_name)


if __name__ == "__main__":
    print("========START========")
    main()
    print("========END========")
