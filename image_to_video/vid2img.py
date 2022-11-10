# -*- coding:utf-8 -*-
# 视频中按序列提取帧，获得训练数据
import cv2
import os

video_src_path = "video"
video_save_path = "img"
frame_gap = 10  # 间隔为10帧，每隔10帧抽取一帧

videos_list = os.listdir(video_src_path)
videos = filter(lambda x: x.endswith("mp4"), videos_list)

for each_video_idx, each_video in enumerate(videos):
    print(videos)
    each_video_name, _ = each_video.split('.')
    m = video_save_path + '/' + each_video_name

    if (os.path.exists(m) == False):
        os.mkdir(m)
    each_video_save_full_path = video_save_path + '/' + each_video_name + '/'

    each_video_full_path = video_src_path + '/' + each_video
    cap = cv2.VideoCapture(each_video_full_path)

    if False == cap.isOpened():
        print('open video failed')
    else:
        print('open video succeeded')

    count = 0  # 统计帧数
    success = True
    i = 0
    # 每隔10帧读取一帧
    while (success):
        success, frame = cap.read()
        i = i + 1
        if (i == frame_gap):  # 每个10帧读取第10帧
            print("[{}/{}]".format(each_video_idx + 1, len(videos_list)),
                  each_video, success, count)
            # print 'Read a new frame:' , success
            params = []
            params.append(int(cv2.IMWRITE_JPEG_QUALITY))
            params.append(95)
            cv2.imwrite(each_video_save_full_path + each_video_name + '_%d.jpg' % count, frame, params)
            count = count + 1
            i = 0

    cap.release()
print('OK！')
